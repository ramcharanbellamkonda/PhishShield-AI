from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import os
import re
from urllib.parse import urlparse

from features import extract_features

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(MODEL_PATH)

TRUSTED_DOMAINS = [
    "google.com",
    "github.com",
    "facebook.com",
    "instagram.com",
    "whatsapp.com",
    "linkedin.com",
    "x.com",
    "twitter.com",
    "youtube.com",
    "reddit.com",
    "amazon.com",
    "amazon.in",
    "flipkart.com",
    "apple.com",
    "microsoft.com",
    "openai.com",
    "netflix.com",
    "wikipedia.org"
]

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "paypal",
    "password",
    "confirm"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    url = data.get("url", "").strip()

    if url == "":
        return jsonify({"error": "Enter URL"}), 400

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    features = extract_features(url)

    pred = model.predict([features])[0]
    prob = model.predict_proba([features])[0]

    if pred == 1:
        prediction = "Phishing"
        confidence = round(prob[1] * 100, 2)
    else:
        prediction = "Legitimate"
        confidence = round(prob[0] * 100, 2)

    parsed = urlparse(url)

    domain = parsed.netloc.lower().replace("www.", "")

    protocol = parsed.scheme.upper()

    subdomain = "None"

    parts = domain.split(".")

    if len(parts) > 2:
        subdomain = parts[0]

    analysis = []

    if parsed.scheme == "https":
        analysis.append("HTTPS Enabled")
    else:
        analysis.append("Uses HTTP")

    ip = bool(re.search(r"\d+\.\d+\.\d+\.\d+", domain))

    if ip:
        analysis.append("Uses IP Address")
    else:
        analysis.append("No IP Address")

    words = [w for w in SUSPICIOUS_WORDS if w in url.lower()]

    if words:
        analysis.append("Suspicious Words : " + ", ".join(words))
    else:
        analysis.append("No Suspicious Keywords")

    trusted = False

    for d in TRUSTED_DOMAINS:
        if domain == d or domain.endswith("." + d):
            trusted = True
            break

    if trusted:
        prediction = "Legitimate"
        confidence = max(confidence, 98)
        risk = "Low"
        analysis.append("Trusted Domain")
    else:
        risk = "High" if prediction == "Phishing" else "Medium"

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "risk": risk,
        "analysis": analysis,
        "url_info": {
            "protocol": protocol,
            "domain": domain,
            "subdomain": subdomain,
            "length": len(url)
        }
    })


if __name__ == "__main__":
    app.run(debug=True)