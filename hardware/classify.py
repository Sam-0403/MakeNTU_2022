# Import necessary packages.
import numpy as np
import torchvision
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import os

# "ConcatDataset" and "Subset" are possibly useful when doing semi-supervised learning.


class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        # torch.nn.MaxPool2d(kernel_size, stride, padding)
        # input 維度 [3, 128, 128]
        self.resnet = torchvision.models.resnet18(pretrained = False)

        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, 3, 1, 1),  # [64, 128, 128]
            nn.BatchNorm2d(64),
            nn.Dropout(0.1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [64, 64, 64]

            nn.Conv2d(64, 128, 3, 1, 1), # [128, 64, 64]
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [128, 32, 32]

            nn.Conv2d(128, 256, 3, 1, 1), # [256, 32, 32]
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [256, 16, 16]

            nn.Conv2d(256, 512, 3, 1, 1), # [512, 16, 16]
            nn.BatchNorm2d(512),
            nn.Dropout(0.1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 8, 8]
            
            nn.Conv2d(512, 512, 3, 1, 1), # [512, 8, 8]
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 4, 4]

            nn.Conv2d(512, 1024, 3, 1, 1), # [1024, 4, 4]
            nn.BatchNorm2d(1024),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [1024, 2, 2]
            
        )

        self.fc = nn.Sequential(
            nn.Linear(1024*2*2, 1024),
            nn.Dropout(0.25),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.Dropout(0.25),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.Dropout(0.25),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.Dropout(0.25),
            nn.ReLU(),
            nn.Linear(32, 4)
        )
    def forward(self, x):
        #return self.resnet(x)
        out = self.cnn(x)
        out = out.view(out.size()[0], -1)
        return self.fc(out)
    

class Decide():
    def __init__(self, weight_file):
        self.test_tfm = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.RandomRotation(20),])
        self.device = "cpu"
        self.model =Classifier().to(self.device)  
        self.model.load_state_dict(torch.load( weight_file ,map_location=torch.device('cpu')),strict = False)
        self.model.eval()
        
    def image_loader(self,image_name):
        """load image, returns cuda tensor"""
        image = Image.open(image_name)
        image = self.test_tfm(image).float()
        image = image.unsqueeze(0) 
        image = image.to(self.device)
        logits = self.model.forward(image)
        ps = torch.exp(logits)
        _, predTest = torch.max(ps,1)
        a = int(predTest[0])
        if(a == 0):
            print("glass")
        if(a == 1):
            print("metal")
        if(a == 2):
            print("paper")
        if(a == 3):
            print("plastic")

        return a
    

# dd = Decide("/0319_best.pth")
# dd.image_loader("/S_10313763.jpg")

if __name__ == "__main__":
    dd = Decide("0319_best.pth")
    # dd.image_loader("S__10313763.jpg")
    dd.image_loader(os.path.abspath('/media/pi/_s_W_Ma_/example.jpg'))