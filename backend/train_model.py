import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

from features import extract_features

print("Loading dataset...")

data = pd.read_csv("../dataset/final_dataset.csv")

# Sample only 100000 URLs
data = data.sample(n=100000, random_state=42)
print(data.head())

# -------------------------------
# Feature Extraction
# -------------------------------

print("\nExtracting URL features...")

X = data["url"].apply(extract_features).tolist()
y = data["label"]

# -------------------------------
# Train Test Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("\nModel Trained Successfully")

# -------------------------------
# Evaluation
# -------------------------------

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print("\nAccuracy")

print(acc)

print("\nConfusion Matrix")

print(confusion_matrix(y_test, pred))

print("\nClassification Report")

print(classification_report(y_test, pred))

# -------------------------------
# Save Model
# -------------------------------

joblib.dump(model, "model/model.pkl")

print("\nModel Saved Successfully!")