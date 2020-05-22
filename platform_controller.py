import argparse
import sys
from cross_layer_controller.brute_force import BruteForceAgent
import os
import docker

version = '0.0.1'
z = 0
agent_list =[]
devices_cfg={}
args = None

def remove_all_containers(client):
    for container in client.containers.list():
        container.kill()

def destroy_and_construct_snipersim():
    client = docker.from_env()
    remove_all_containers(client)
    container = client.containers.create('sniper', command='/bin/bash', tty=True, detach=True, privileged=True)
    container.start() 

    # re-copy the configs file to each containers
    cmd ="docker cp system_configurations/devices/"+ devices_cfg['edge']+" "+container.id+":/usr/local/src/sniper/sniper-7.2/"
    os.system(cmd)
    cmd ="docker cp system_configurations/devices/"+ devices_cfg['fog']+" "+container.id+":/usr/local/src/sniper/sniper-7.2/"
    os.system(cmd)    
    cmd ="docker cp system_configurations/devices/"+ devices_cfg['cloud']+" "+container.id+":/usr/local/src/sniper/sniper-7.2/"    
    os.system(cmd)

    return client.containers.list()[0]    


def get_MIPS_from_result(time, instructions):
    ins = instructions.decode('utf-8').split('|')[1]
    ns = time.decode('utf-8').split('|')[1]
    i = float(ins[:-1])
    t = float(ns[:-1])
    devices_cfg['ins'].append(i/1000000)
    return (i/1000000)/(t/1000000000) 

def run_snipersim(container, cfg):
    global args
    if args.workload == 'FallDetection':
        if cfg.split('.')[0] == 'edge':
            cmd = './run-sniper --fast-forward -c '+ cfg + ' --power -sdvfs:0:0:400 -- python3 edge2.py '+ devices_cfg['window_size']
        else:
            cmd = './run-sniper --fast-forward -c '+ cfg + ' --power -- python3 fog2.py '+ devices_cfg['window_size']
    else:
        cmd = './run-sniper --fast-forward -c '+ cfg + ' -- ./xcsf/build/xcsf/main mp 5'
    (exit_code, output) = container.exec_run(cmd=cmd)
    (exit_code, instructions) = container.exec_run(cmd='grep "Instructions" sim.out')
    (exit_code, time) = container.exec_run(cmd='grep "Time" sim.out')
    MIPS = get_MIPS_from_result(time, instructions)
    return MIPS

def get_two_layer_MIPS_from_snipersim(container):
    global devices_cfg
    
    devices_cfg['ins'] = []
    edge_MIPS = run_snipersim(container, devices_cfg['edge'])
    fog_MIPS = run_snipersim(container, devices_cfg['fog'])

#    container.stop()
#    container.remove()
    return edge_MIPS, fog_MIPS


def get_three_layer_MIPS_from_snipersim(container):
    global args, devices_cfg
    
    devices_cfg['ins'] = []
    edge_MIPS = run_snipersim(container, devices_cfg['edge'])
    fog_MIPS = run_snipersim(container, devices_cfg['fog'])
    cloud_MIPS = run_snipersim(container, devices_cfg['cloud'])
#    container.stop()
#    container.remove()
    return edge_MIPS, fog_MIPS, cloud_MIPS

def init_params():
    global args, devices_cfg
    parser = argparse.ArgumentParser(description='dynamic ifogsim')
    parser.add_argument('agent', metavar='[agent]',
                        help='xcs/brute_force')
    parser.add_argument('devices_configuration', metavar='[devices configuration]',
                        help='devices configuration')
    parser.add_argument('workload', metavar='[workload name]',
                        help='FallDetection/3layerCalculation')
    args = parser.parse_args()

    with open(args.devices_configuration, 'r') as f:
        lines = f.readlines()
        for line in lines:
            datas = line.split("=")
            devices_cfg[datas[0]] = datas[1][:-1]
    for k,v in devices_cfg.items():
        print(k,v)

# check whether input_agent is possible to support or not 
def check_agent_available(input_agent):
    global args, devices_cfg,z
    if input_agent not in agent_list:
        print("not supported agent")
        sys.exit(1)
    else:
        if input_agent == "brute_force":
            z+=1
            return BruteForceAgent(int(devices_cfg['number_of_edge']), devices_cfg)

# get agents list from data file
def read_agent_list():
    global agent_list
    with open('cross_layer_controller/agent_list.dat','r') as f:
        for line in f.readlines():
            agent_list.append(line[:-1])

def _main():
    global args, devices_cfg

    init_params()
    
    print("start to get the MIPS of workload from virtual devices with snipersim")
    devices_cfg['workload']=args.workload    
    if args.workload == 'FallDetection':
        read_agent_list()
        for x in range(1,50,2):
            devices_cfg['window_size'] = str(x)
            edge_MIPS, fog_MIPS = get_two_layer_MIPS_from_snipersim(destroy_and_construct_snipersim())
            print(str(x)+","+str(edge_MIPS)+","+str(fog_MIPS)+","+str(devices_cfg['ins'][0])+","+str(devices_cfg['ins'][1]))
            devices_cfg['edge_MIPS'] = edge_MIPS
            devices_cfg['fog_MIPS'] = fog_MIPS
            agent = check_agent_available(args.agent)
            agent.getFallDetectionResult(int(devices_cfg['number_of_edge']))
    else:
        edge_MIPS, fog_MIPS, cloud_MIPS = get_three_layer_MIPS_from_snipersim(destroy_and_construct_snipersim())        
        devices_cfg['edge_MIPS']=edge_MIPS
        devices_cfg['fog_MIPS']=fog_MIPS
        devices_cfg['cloud_MIPS']=cloud_MIPS
        devices_cfg['FOG_APP_MIPS']='0'

        print("finish to get the MIPS")

        read_agent_list()    
        print("start "+args.agent + " agent")
        agent = check_agent_available(args.agent)
        agent.findAllClassesOptimal(int(devices_cfg['number_of_edge']))
        agent.showCompare(4,int(devices_cfg['number_of_edge']))


if __name__ == '__main__':
    _main()
