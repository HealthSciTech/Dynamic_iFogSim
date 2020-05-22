import os
import sys
import subprocess
from typing import List
import pickle
import os.path

class BruteForceAgent:
	root_path=os.getcwd()
	jar_file_path=root_path+"/ifogsim/ifogsim.jar"
	two_jar_file_path=root_path+"/ifogsim/ifogsim_two_layer.jar"
	config_folder=root_path+"/system_configurations/ifogsim/"
	map_file_path=root_path+"/ifogsim/map.dat"
	data_dic = {}
	optimal_response_time_map={}
	optimal_energy_map={}

	def __init__(self, max_number_of_apps:int, device_cfgs:dict):
		self.device_cfgs = device_cfgs
		self.max_number_of_apps = max_number_of_apps
		#TODO: fix below lines 
		if self.device_cfgs['workload'] == 'FallDetection':	
			class_num = 5
			for number_of_apps in range(1,max_number_of_apps+1):
				for cloud_network_type in [0,1,2]:
					for packet_loss in range(0,15,2):
						processing = 0
						policies = [0,0,0]
						k = str(class_num)+"_"+str(number_of_apps)+ \
							"_"+str(0)+ \
							"_"+str(cloud_network_type)+ \
							"_"+str(packet_loss)+ \
							"_"+str(policies[0])+ \
							"_"+str(policies[1])+ \
							"_"+str(policies[2])
						self.data_dic[k] = self.runIFogSim(class_num,packet_loss,processing,number_of_apps,cloud_network_type,policies)
		else:
			class_num = 4		
			for number_of_apps in range(1,max_number_of_apps+1):
				for cloud_network_type in [0,1,2]:
					for processing in [0,1,2]:
						for packet_loss in range(0,15,2):
							for policies in self.makeCandidates(number_of_apps):
								k = str(class_num)+"_"+str(number_of_apps)+ \
									"_"+str(processing)+ \
									"_"+str(cloud_network_type)+ \
									"_"+str(packet_loss)+ \
									"_"+str(policies[0])+ \
									"_"+str(policies[1])+ \
									"_"+str(policies[2])
								if k not in self.data_dic:
									self.data_dic[k] = self.runIFogSim(class_num,packet_loss,processing,number_of_apps,cloud_network_type,policies)
								else:
									continue

#		with open(pickle_path,"wb") as fw:
#			pickle.dump(self.data_dic, fw)
#		fw.close()

	def makeConfigFile(self, class_num:int, packet_loss:int, processing:int, number_of_apps:int, cloud_network_type:int, policies:List[int]):
		if(class_num != 5):
			run_cmd = ["/bin/bash", self.root_path+"/ifogsim/make_input_for_agent.sh",str(number_of_apps),str(processing),self.config_folder,\
				str(cloud_network_type),str(packet_loss),str(class_num),
				str(policies[0]),str(policies[1]),str(policies[2]),
				str(sum(self.device_cfgs['ins'])/len(self.device_cfgs['ins'])),
				str(self.device_cfgs['edge_MIPS']), str(self.device_cfgs['fog_MIPS']), str(self.device_cfgs['cloud_MIPS']),
				str(self.device_cfgs['FOG_APP_MIPS'])]
		else:
			run_cmd = ["/bin/bash", self.root_path+"/ifogsim/make_input_for_agent.sh",str(number_of_apps),str(processing),self.config_folder,\
				str(cloud_network_type),str(packet_loss),str(class_num),
				str(policies[0]),str(policies[1]),str(policies[2]),
				str(self.device_cfgs['ins'][0]),
				str(self.device_cfgs['edge_MIPS']), str(self.device_cfgs['fog_MIPS']), str(0),
				str(self.device_cfgs['ins'][1])]
		output = subprocess.Popen(run_cmd,
							stdout=subprocess.PIPE,
							stderr=subprocess.STDOUT)
		stdout,stderr = output.communicate()
		result = stdout.decode("utf-8").split("\n")

		if stderr is not None:
			print(stderr)
			sys.exit(1)	

	def runIFogSim(self, class_num:int, packet_loss:int, processing:int, number_of_apps:int, cloud_network_type:int, policies:List[int]) -> List[float]: 
		self.makeConfigFile(class_num, packet_loss, processing, number_of_apps, cloud_network_type, policies)
		config_file_path = self.config_folder+"/"+str(class_num)+"_"+str(number_of_apps)+"_"+str(processing)+"_"+str(cloud_network_type)+"_"+str(packet_loss)+"_"+str(policies[0])+"_"+str(policies[1])+"_"+str(policies[2])+".config"
		if class_num != 5:
			run_cmd = ["java","-jar",self.jar_file_path,config_file_path,self.map_file_path]
			output = subprocess.Popen(run_cmd,
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT)
			stdout,stderr = output.communicate()
			result = stdout.decode("utf-8").split("\n")
			result = result[-6:]
			response_time = float(result[0])
			edge_power_consumption = float(result[3])
			
			if stderr is not None:
				print(stderr)
				sys.exit(1)	
			os.remove(config_file_path)
			return [response_time,edge_power_consumption]
		else:
			run_cmd = ["java","-jar",self.two_jar_file_path,config_file_path,self.map_file_path]
			output = subprocess.Popen(run_cmd,
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT)
			stdout,stderr = output.communicate()
			result = stdout.decode("utf-8").split("\n")
			result = result[-5:]
			response_time = float(result[0])
			edge_power_consumption = float(result[2])
			
			if stderr is not None:
				print(stderr)
				sys.exit(1)	
			os.remove(config_file_path)
			return [response_time,edge_power_consumption]

	def findOptimalResponseTime(self, class_num:int, number_of_apps:int):
		#self.optimal_response_time_map
		for number_of_apps in range(1,number_of_apps+1):
			for cloud_network_type in [0,1,2]:
				for processing in [0,1,2]:
					for packet_loss in range(0,15,2):
						for policies in self.makeCandidates(number_of_apps):	
							k = str(class_num)+"_"+str(number_of_apps)+"_"+str(processing)+"_"+str(cloud_network_type)+"_"+str(packet_loss)+"_"+str(policies[0])+"_"+str(policies[1])+"_"+str(policies[2])
							n_k = str(class_num)+"_"+str(number_of_apps)+"_"+str(cloud_network_type)+"_"+str(packet_loss)
							if n_k not in self.optimal_response_time_map:
								print(self.data_dic)
								self.optimal_response_time_map[n_k] = [self.data_dic[k][0],policies]
							else:
								if self.optimal_response_time_map[n_k][0] > self.data_dic[k][0]:
									self.optimal_response_time_map[n_k] = [self.data_dic[k][0],policies]

	def findOptimalEnergy(self, class_num:int, number_of_apps:int):
		for number_of_apps in range(1,number_of_apps+1):
			for cloud_network_type in [0,1,2]:
				for processing in [0,1,2]:
					for packet_loss in range(0,15,2):
						for policies in self.makeCandidates(number_of_apps):
							k = str(class_num)+"_"+str(number_of_apps)+"_"+str(processing)+"_"+str(cloud_network_type)+"_"+str(packet_loss)+"_"+str(policies[0])+"_"+str(policies[1])+"_"+str(policies[2])
							n_k = str(class_num)+"_"+str(number_of_apps)+"_"+str(cloud_network_type)+"_"+str(packet_loss)
							if n_k not in self.optimal_energy_map:
								self.optimal_energy_map[n_k] = [self.data_dic[k][1],policies]
							else:
								if self.optimal_energy_map[n_k][0] > self.data_dic[k][1]:
									self.optimal_energy_map[n_k] = [self.data_dic[k][1],policies]
	
	def getFallDetectionResult(self, number_of_app:int):
		class_num = 5
		for number_of_apps in range(1,self.max_number_of_apps+1):
			for packet_loss in range(0,15,2):
				cloud_network_type=0
				processing = 0
				policies = [0,0,0]
				k = str(class_num)+"_"+str(number_of_apps)+ \
					"_"+str(0)+ \
					"_"+str(cloud_network_type)+ \
					"_"+str(packet_loss)+ \
					"_"+str(policies[0])+ \
					"_"+str(policies[1])+ \
					"_"+str(policies[2])
				print(self.data_dic[k],end=' ')
			print()
	def findAllClassesOptimal(self, number_of_apps:int):
		self.findOptimalResponseTime(4, number_of_apps)
		self.findOptimalEnergy(4, number_of_apps)

	def getOnlySpecificComputingResponseResult(self, class_num:int, number_of_apps:int, processing:int, cloud_network_type:int) -> List[List[int]]:
		policy = []
		num = -1
		result = []
		print(result)
		for number_of_app in range(1, number_of_apps+1):
			result.append([])
			num = number_of_app
			for packet_loss in range(0,15,2):
				if processing == 0:
					policy = [num,0,0]
				elif processing == 1:
					policy = [0,num,0]
				else:
					policy = [0,0,num]
				k = str(class_num)+"_"+str(number_of_app)+"_"+str(processing)+"_"+str(cloud_network_type)+"_"+str(packet_loss)+"_"+str(policy[0])+"_"+str(policy[1])+"_"+str(policy[2])
				result[number_of_app-1].append(self.data_dic[k][0])
		return result

	def getEdgeComputingResponseResult(self, class_num:int, number_of_apps:int) -> List[List[int]]:
		return self.getOnlySpecificComputingResponseResult(class_num, number_of_apps, 0, 0)

	def getFogComputingResponseResult(self, class_num:int, number_of_apps:int) -> List[List[int]]:
		return self.getOnlySpecificComputingResponseResult(class_num, number_of_apps, 1, 0)

	def getCloudComputingWIFIResponseResult(self, class_num:int, number_of_apps:int) -> List[List[int]]:
		return self.getOnlySpecificComputingResponseResult(class_num, number_of_apps, 2, 0)

	def getCloudComputing4GResponseResult(self, class_num:int, number_of_apps:int) -> List[List[int]]:
		return self.getOnlySpecificComputingResponseResult(class_num, number_of_apps, 2, 1)

	def getCloudComputing3GResponseResult(self, class_num:int, number_of_apps:int) -> List[List[int]]:
		return self.getOnlySpecificComputingResponseResult(class_num, number_of_apps, 2, 2)

	def getOffloadingResponseResult(self, class_num:int, number_of_apps:int) -> List[List[List[float]]]:
		cloud_network_type = 0
		packet_loss = 0
		result = []
		for number_of_apps in range(1, number_of_apps+1):
			result.append([])
			for packet_loss in range(0,15,2):
				n_k = str(class_num)+"_"+str(number_of_apps)+"_"+str(cloud_network_type)+"_"+str(packet_loss)
				#result[number_of_apps-1].append([self.optimal_response_time_map[n_k][0], self.optimal_response_time_map[n_k][1]])
				result[number_of_apps-1].append(self.optimal_response_time_map[n_k][1])
		return result

	def getOffloadingEnergyResult(self, class_num:int, number_of_apps:int) -> List[List[List[float]]]:
		cloud_network_type = 0
		packet_loss = 0
		result = []
		for number_of_apps in range(1, number_of_apps+1):
			result.append([])
			for packet_loss in range(0,15,2):
				n_k = str(class_num)+"_"+str(number_of_apps)+"_"+str(cloud_network_type)+"_"+str(packet_loss)
				#result[number_of_apps-1].append([self.optimal_response_time_map[n_k][0], self.optimal_response_time_map[n_k][1]])
				result[number_of_apps-1].append(self.optimal_energy_map[n_k][1])
		return result


	def printData(self, data):
		r = ""
		for x in data:
			for t in x:
				r+=str(t)+","
			r=r[:-1]+"\n"
		print(r[:-1])
		print()
		r = ""


	def showCompare(self, class_num:int, number_of_apps:int):
		print(" only edge computing response time")
		self.printData(self.getEdgeComputingResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" only fog computing response time")
		self.printData(self.getFogComputingResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" only cloud with 3g network computing response time")
		self.printData(self.getCloudComputing3GResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" only cloud with 4g network computing response time")
		self.printData(self.getCloudComputing4GResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" only cloud with wifi network computing response time")
		self.printData(self.getCloudComputingWIFIResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" offloading response based map ")
		self.printData(self.getOffloadingResponseResult(class_num, number_of_apps))
		print("======================================================================")
		print(" offloading energy based map ")
		self.printData(self.getOffloadingEnergyResult(class_num, number_of_apps))
	
	def getSpecifiedEnergyConsumption(self, class_num:int, number_of_apps:int, processing:int, cloud_network_type:int) -> List[List[int]]:
		result = []
		for number_of_apps in range(1, number_of_apps+1):
			result.append([])
			for packet_loss in range(0,15,2):
				k = str(class_num)+"_"+str(number_of_apps)+"_"+str(processing)+"_"+str(cloud_network_type)+"_"+str(packet_loss)
				result[number_of_apps-1].append(self.data_dic[k][1]/1000)
		return result

	def makeCandidates(self, number_of_apps):
		result_set = set()
		for x in range(number_of_apps+1):
			for y in range(number_of_apps+1):
				for z in range(number_of_apps+1):
					if x+y+z == number_of_apps:
						result_set.add((x,y,z))
		result = []
		
		for x in result_set:
			result.append(list(x))
		
		return result
