import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import os
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from torchvision.transforms import transforms

device = "mps" if torch.mps.is_available() else "cpu"

image_path = []
labels = []

dir_path = "/Users/jay/Jupyter Projects/Pico"

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

for i in listdir_nohidden(f"{dir_path}/Data"):
    for label in listdir_nohidden(f"{dir_path}/Data/{i}"):
        for image in listdir_nohidden(f"{dir_path}/Data/{i}"):
            image_path.append(f"{dir_path}/Data/{i}/{image}")
            labels.append(i)

df = pd.DataFrame(zip(image_path, labels), columns = ["image_path", "labels"])
df = df.drop_duplicates().reset_index(drop=True)


class Net(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(3, 32, kernel_size = 3, padding = 1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size = 3, padding = 1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size = 3, padding = 1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size = 3, padding = 1)

        self.pooling = nn.MaxPool2d(2, 2)
        self.relu = nn.ReLU()

        self.flatten = nn.Flatten()
        self.linear = nn.Linear((256*8*8), 256)

        self.output = nn.Linear(256, len(df["labels"].unique()))

    def forward(self, x):
        x = self.conv1(x) #(32, 128, 128)
        x = self.pooling(x) #(32, 64, 64)
        x = self.relu(x)

        x = self.conv2(x) #(64, 64, 64)
        x = self.pooling(x) #(64, 32, 32)
        x = self.relu(x)

        x = self.conv3(x) #(128, 32, 32)
        x = self.pooling(x) #(128, 16, 16)
        x = self.relu(x)

        x = self.conv4(x) #(256, 16, 16)
        x = self.pooling(x) #(256, 8, 8) same as number in self.linear
        x = self.relu(x)

        x = self.flatten(x)
        x = self.linear(x)
        x = self.output(x)
        return x


path = f"{dir_path}/Pico.pth"

loaded_model = Net().to(device)
loaded_model.load_state_dict(torch.load(path))
loaded_model.eval()

le = LabelEncoder()
le.fit(df["labels"])

transform = transforms.Compose([
    transforms.Resize([128, 128]),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    transforms.ConvertImageDtype(torch.float)
])


def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).to(device)
    
    model_prediction = loaded_model(image.unsqueeze(0))
    model_prediction = torch.argmax(model_prediction, axis=1).item()
    
    return le.inverse_transform([model_prediction])[0]

