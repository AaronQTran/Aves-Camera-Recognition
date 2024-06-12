# import torch

# # Check if GPU is available
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(f'Using {device} device')

# # Create a tensor
# x = torch.tensor([1.0, 2.0, 3.0])
# print(x)

# # Move tensor to the GPU if available
# x = x.to(device)

# # Create another tensor
# y = torch.tensor([4.0, 5.0, 6.0]).to(device)
# print(y)

# # Perform element-wise addition
# z = x + y
# print(z)

import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple neural network
class SimpleNN(nn.Module): #nn.module is the base class for all pytorch nn moduels 
    def __init__(self):
        super(SimpleNN, self).__init__() #nn.module is parent class, simpleNN is child class, super() is reusing parents class constructor, passing in simpleNN declares method res order
        self.fc1 = nn.Linear(3, 3) # class instance variable 

    def forward(self, x): #function to apply linear trans to a parameter x
        x = self.fc1(x)
        return x

# Create a model instance and move it to the appropriate device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SimpleNN().to(device)

# Create a random input tensor
input_tensor = torch.tensor([1.0, 2.0, 3.0]).to(device)

# Pass the input tensor through the model
output = model(input_tensor) # runs input_tensor through forward()
print(output)
