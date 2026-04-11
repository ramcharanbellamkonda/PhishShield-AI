from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

app = Flask(__name__)
CORS(app)  # allow extension to access API

# Load trained model
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "model", "model.pkl")

model = joblib.load(model_path)


# Feature extraction (basic version)
def extract_features(url):
    return [
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,  # IP address
        len(url),                                          # URL length
        1 if '-' in url else 0,                            # prefix-suffix
        1 if '@' in url else 0,                            # @ symbol
        url.count('.')                                     # number of dots
    ]


# Home route
@app.route("/")
def home():
    return "API is running"


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data.get("url", "")
    print("Received URL:", url) 

    # Extract features
    features = extract_features(url)

    # Match model input size (30 features)
    features = features + [0] * (30 - len(features))

    # Prediction
    try:
        prediction = model.predict([features])[0]
        proba = model.predict_proba([features])[0][1]
    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": str(e)
        })

    result = "Phishing" if prediction == 1 else "Safe"
    risk = round(proba * 100, 2)

    # Explanation logic
    reasons = []
    if "@" in url:
        reasons.append("Contains @ symbol")
    if "-" in url:
        reasons.append("Contains hyphen")
    if len(url) > 75:
        reasons.append("URL is too long")
    if url.count('.') > 3:
        reasons.append("Too many subdomains")

    reason_text = ", ".join(reasons) if reasons else "No obvious risk detected"

    return jsonify({
        "url": url,
        "result": result,
        "risk": risk,
        "reason": reason_text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)