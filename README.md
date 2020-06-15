## Dynamic_iFogSim : A Framework for Full-Stack Simulation of Dynamic Resource Management in IoT Systems

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Features

1. Adding TCP latency model to iFogSim simulator (https://github.com/DongDongJu/iFogSim)

2. This tools can analyzing the system in a holistic manner considering device hardware layer to platform layer.

## understanding of this tool

This tool can help to re-configure iFogsim and simulate the MIPS for iFogSim from virtual full-system simulator. It means that dynamically testing the fog system. platform_controller.py can help to user for that by using lots of configurations and libs. lets check the below folder description.

### cross_layer_controller folder

This folder includes a brute force agent example. Users can modify or add their own policies like this example.

### configs folder

This folder includes each device configurations that we want to simulate with snipersim and also includes fog system's layer configuration.

### ifogsim folder

This folder includes a re-configuration script and an exported executable jar file from extended ifogsim. If a user wants to simulate their own fog system then the user has to make their workflow by using extended ifogsim.

### snipersim folder 

snipersim(http://snipersim.org/w/The_Sniper_Multi-Core_Simulator) is full-system simulator. It's hard to install dependencies for that. Also, for simulating MIPS with snipersim, we have a problem that installing lots of popular framework like OpenCV, pytorch. So, we provide some useful Dockerfile for that. If user want to install another library for applications then have to check Dockerfile.

## requirements
0. Understanding of iFogSim (https://github.com/Cloudslab/iFogSim)
1. Prepare your ifogsim workflow example with extended ifogsim(extended ifogsim folder).
2. Install docker-engine (https://docs.docker.com/install/)

## how to start simulation?

1. prepare a system layers by using configurations

&nbsp;&nbsp;&nbsp;&nbsp;1-1. if you want to make a more complicated system layers then you have to make your jar file.  
&nbsp;&nbsp;&nbsp;&nbsp;please check the extended ifogsim folder

2. prepare virtual device's specification for configuration.

3. prepare application what you want to run on the virtual device with snipersim. you can test it with docker container before run the simulation.

4. prepare your own cross_layer_controller. this repo have a sample cross_layer_controller with brute force policy. if you want to run with other policy then you can add to the cross_layer folder.

5. run the simulation

### Running example

- clone this repository
```
git clone https://github.com/HealthSciTech/Dynamic_iFogSim
```
- build sniper docker image
```
cd snipersim
docker build -t sniper .
cd ..
```
- running brute force agent with example configs  
```
python3 platform_controller.py brute_force system_configurations/devices/device_setting.cfg FallDetection
```

### Citation
If you find this work useful for your research, please cite our paper:
```
@article{seodynamic,
  title={Dynamic iFogSim: A Framework for Full-Stack Simulation of Dynamic Resource Management in IoT Systems},
  author={Seo, Dongjoo and Shahhosseini, Sina and Mehrabadi, Milad Asgari and Donyanavard, Bryan and Lim, Song-Soo and Rahmani, Amir M and Dutt, Nikil}
}
```

For any questions, contact me at commisori28@gmail.com
