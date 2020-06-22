from utils import PATH_LABEL
from utils import PATH_DATA_FOLDER
import pickle
import torch
import torch.nn as nn
import torch.utils.data as dat

class ResBlock(nn.Module):
	def __init__(self, inChannels, outChannels):
		super(ResBlock, self).__init__()
		
		self.matchDimension = None
		if inChannels != outChannels:
			self.matchDimension = nn.Conv2d(inChannels, outChannels, 1, stride = 1, bias = False)
		
		self.conv1 = nn.Conv2d(inChannels, outChannels, 3, stride = 1, padding = 1, bias = False)
		self.bn1 = nn.BatchNorm2d(outChannels)
		self.conv2 = nn.Conv2d(outChannels, outChannels, 3, stride = 1, padding = 1, bias = False)
		self.bn2 = nn.BatchNorm2d(outChannels)
	
	def forward(self, x):
		out = self.conv1(x)
		out = self.bn1(out)
		out = nn.functional.relu(out)
		out = self.conv2(out)
		out = self.bn2(out)
		if self.matchDimension == None:
			out += x
		else:
			out += self.matchDimension(x)
		out = nn.functional.relu(out)
		return out

class ResNet(nn.Module):
	def __init__(self):
		super(ResNet, self).__init__()
		self.conv = nn.Conv2d(4, 32, 3, stride = 1, padding = 1, bias = False)
		self.bn = nn.BatchNorm2d(32)
		
		blockList = [ResBlock(32, 32) for i in range(5)]
		self.res = nn.Sequential(*blockList)
		self.pool = nn.AvgPool2d(5)
		self.fc = nn.Linear(128, 1)
	
	def forward(self, x):
		x = self.conv(x)
		x = self.bn(x)
		x = nn.functional.relu(x)
		x = self.res(x)
		x = self.pool(x)
		x = x.view(x.size()[0], -1)
		x = self.fc(x)
		x = torch.tanh(x)
		return x

class Dataset(dat.Dataset):
	def __init__(self):
		with open(PATH_LABEL, "rb") as f:
			self.labelList = pickle.load(f)
	
	def __getitem__(self, index):
		with open(PATH_DATA_FOLDER + str(index) + ".dat", "rb") as f:
			data = torch.FloatTensor(pickle.load(f))
		label = torch.FloatTensor([self.labelList[index]])
		return data, label
	
	def __len__(self):
		return len(self.labelList)
