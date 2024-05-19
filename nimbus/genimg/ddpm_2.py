import io
import torch
import torch.nn as nn
from matplotlib import pyplot as plt
from tqdm import tqdm
from torch import optim
from .utils import *
from .modules import UNet
import json
from .models import Image_Binary
from PIL import Image

class Diffusion:
    def __init__(self, noise_steps=1000, beta_start=1e-4, beta_end=0.02, img_size=256, device="cuda"):
        self.noise_steps = noise_steps
        self.beta_start = beta_start
        self.beta_end = beta_end
        self.img_size = img_size
        self.device = device

        self.beta = self.prepare_noise_schedule().to(device)
        self.alpha = 1. - self.beta
        self.alpha_hat = torch.cumprod(self.alpha, dim=0)

    def prepare_noise_schedule(self):
        return torch.linspace(self.beta_start, self.beta_end, self.noise_steps)

    def noise_images(self, x, t):
        sqrt_alpha_hat = torch.sqrt(self.alpha_hat[t])[:, None, None, None]
        sqrt_one_minus_alpha_hat = torch.sqrt(1 - self.alpha_hat[t])[:, None, None, None]
        Ɛ = torch.randn_like(x)
        return sqrt_alpha_hat * x + sqrt_one_minus_alpha_hat * Ɛ, Ɛ

    def sample_timesteps(self, n):
        return torch.randint(low=1, high=self.noise_steps, size=(n,))

    def sample(self, model, n):
        model.eval()
        with torch.no_grad():
            x = torch.randn((n, 3, self.img_size, self.img_size)).to(self.device)
            for i in tqdm(reversed(range(1, self.noise_steps)), position=0):
                t = (torch.ones(n) * i).long().to(self.device)
                predicted_noise = model(x, t)
                alpha = self.alpha[t][:, None, None, None]
                alpha_hat = self.alpha_hat[t][:, None, None, None]
                beta = self.beta[t][:, None, None, None]
                if i > 1:
                    noise = torch.randn_like(x)
                else:
                    noise = torch.zeros_like(x)
                x = 1 / torch.sqrt(alpha) * (x - ((1 - alpha) / (torch.sqrt(1 - alpha_hat))) * predicted_noise) + torch.sqrt(beta) * noise
        model.train()
        x = (x.clamp(-1, 1) + 1) / 2
        x = (x * 255).type(torch.uint8)
        return x

def generate_image():
    device = "cuda"
    model = UNet().to(device)
    ckpt = torch.load(r"C:\Users\Prince Savsaviya\Desktop\8th Sem Website\nimbus\genimg\unconditional_ckpt.pt")
    model.load_state_dict(ckpt)
    diffusion = Diffusion(img_size=64, device=device,noise_steps=1000)
    x = diffusion.sample(model, 1)
    
    grid = torchvision.utils.make_grid(x)
    ndarr = grid.permute(1, 2, 0).to('cpu').numpy()
    im = Image.fromarray(ndarr)
    
    with io.BytesIO() as output:
        im.save(output, format='JPEG')
        image_binary = output.getvalue()

    # Create an instance of your Image model and save the binary data to the database
    image_instance = Image_Binary.objects.create(image_data=image_binary)
    image_instance.save()
    
    
    # Save tensor data as JSON
    #with open(r"C:\Users\Prince Savsaviya\Desktop\8th Sem Website\nimbus\static\json\tensor_data.json", "w") as json_file:
    #    json.dump(tensor_data, json_file)
    #print("Tensor data saved as JSON.")