#/bin/bash

./test_dcgan.py
./test_resnet18.py
./test_shufflenet_v2.py
./test_mobilenet_v2.py
./test_resnet34.py
./test_squeezenet.py
./test_resnet101.py
./test_roberta.py
./test_unet_for_brain_MRI.py

python3 edge.py 10
python3 fog.py 10
