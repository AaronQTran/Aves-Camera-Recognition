import torch

# Check if GPU is available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')

# Create a tensor
x = torch.tensor([1.0, 2.0, 3.0])
print(x)

# Move tensor to the GPU if available
x = x.to(device)
print(x)
