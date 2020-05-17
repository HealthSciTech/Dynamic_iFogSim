#!/usr/bin/env python3
import torch
from PIL import Image
import torchvision
import matplotlib.pyplot as plt
use_gpu = True if torch.cuda.is_available() else False

model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub', 'DCGAN', pretrained=True, useGPU=use_gpu)
num_images = 64
noise, _ = model.buildNoiseData(num_images)
with torch.no_grad():
    generated_images = model.test(noise)

# let's plot these images using torchvision and matplotlib
print(plt.imshow(torchvision.utils.make_grid(generated_images).permute(1, 2, 0).cpu().numpy()))
# plt.show()
