from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd
from features import extract_features

app = Flask(__name__)
CORS(app)

# Load model
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "model", "model.pkl")
model = joblib.load(model_path)

# Feature names (30)
feature_names = [
    'having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service',
    'having_At_Symbol', 'double_slash_redirecting',
    'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
    'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token',
    'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH',
    'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover',
    'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
    'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index',
    'Links_pointing_to_page', 'Statistical_report'
]

@app.route("/")
def home():
    return "API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data.get("url", "")

    try:
        features = extract_features(url)
        features = features + [0] * (30 - len(features))

        df = pd.DataFrame([features], columns=feature_names)

        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]

        result = "Phishing" if prediction == 1 else "Safe"
        risk = round(proba * 100, 2)

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

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)