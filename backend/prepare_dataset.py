import pandas as pd

# Load dataset
data = pd.read_csv("../dataset/dataset.csv")

print("Original Dataset")
print(data["type"].value_counts())

# Convert into binary labels
data["label"] = data["type"].apply(
    lambda x: 0 if x == "benign" else 1
)

# Keep only required columns
data = data[["url", "label"]]

print("\nBinary Dataset")
print(data["label"].value_counts())

# Save
data.to_csv("../dataset/final_dataset.csv", index=False)

print("\nSaved as dataset/final_dataset.csv")