import pickle

with open('train/data/data.out', 'rb') as f:
    data = pickle.load(f)

for x in data : 
    print(x)