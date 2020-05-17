## Dynamic_iFogSim : A Framework for Full-Stack Simulation of Dynamic Resource Management in IoT Systems

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Features

1. Adding TCP latency model to iFogSim simulator (https://github.com/DongDongJu/iFogSim)

2. This tools can analyzing the system in a holistic manner considering device hardware layer to platform layer.

## requirements
0. Understanding of iFogSim (https://github.com/Cloudslab/iFogSim)
1. Prepare your ifogsim workflow example with modified ifogsim(https://github.com/DongDongJu/iFogSim).
2. Install docker-engine (https://docs.docker.com/install/)

### Running example

- clone this repository
```
clone https://github.com/DongDongJu/Dynamic_iFogSim
```
- build sniper docker image
```
cd snipersim
docker build -t sniper .
cd ..
```
- running brute force agent with example configs  
```
python3 platform_controller.py brute_force configs/devices/device_setting.cfg FallDetection
```


For any questions, contact me at commisori28@gmail.com
