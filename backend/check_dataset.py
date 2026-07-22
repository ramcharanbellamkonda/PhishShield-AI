import pandas as pd

data = pd.read_csv("../dataset/dataset.csv")

print(data.head())

print("\nColumns:")
print(data.columns)

print("\nDataset Shape:")
print(data.shape)

print("\nLabel Counts:")
print(data["type"].value_counts())