# 🛡️ PhishShield AI

An AI-powered phishing website detection system that analyzes URLs using Machine Learning and identifies whether a website is **Legitimate** or **Phishing** in real time.

## 🚀 Features

- 🔍 Detects phishing websites using Machine Learning
- 🤖 Random Forest Classification Model
- 🌐 Flask REST API
- 🧩 Chrome Extension for real-time detection
- 📊 Displays confidence score
- ⚡ Fast predictions
- 🎨 Modern responsive UI
- 📄 Download scan reports

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Scikit-learn
- Pandas
- NumPy

### Machine Learning
- Random Forest
- Feature Engineering
- URL Analysis

### Frontend
- HTML
- CSS
- JavaScript

### Browser Extension
- Chrome Extension API

---

## 📂 Project Structure

```
PhishShield-AI/
│
├── backend/
│   ├── app.py
│   ├── features.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── model/
│   ├── static/
│   └── templates/
│
├── extension/
│
├── dataset/
│
├── screenshots/
│
├── README.md
│
└── LICENSE
```

---

## 🧠 Machine Learning

The model extracts multiple URL-based features including:

- URL Length
- Domain Length
- HTTPS Usage
- HTTP Usage
- Number of Digits
- Number of Subdomains
- Special Characters
- Entropy
- Suspicious Keywords
- Suspicious TLD
- IP Address Detection
- URL Shortener Detection
- Path Depth
- Query Parameters
- Uppercase Ratio

The extracted features are classified using a Random Forest model.

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/ramcharanbellamkonda/PhishShield-AI.git
```

Go into backend

```bash
cd PhishShield-AI/backend
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

---

## 🌍 API Endpoint

POST

```
/predict
```

Example

```json
{
    "url":"https://google.com"
}
```

---

## 📈 Future Improvements

- Domain Age Verification
- SSL Certificate Analysis
- WHOIS Integration
- QR Code Phishing Detection
- Deep Learning Model
- Dashboard Analytics

---

## 👨‍💻 Author

**Ramcharan Bellamkonda**

GitHub

https://github.com/ramcharanbellamkonda

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.


## 📸 Screenshots

### 🏠 Home Page
![Home](screenshots/home.png)

### ✅ Safe Website Detection
![Safe](screenshots/safe.png)

### ⚠️ Phishing Detection
![Phishing](screenshots/phishing.png)

### 🧩 Chrome Extension
![Extension](screenshots/extension.png)

### 📄 Scan Report
![Report](screenshots/report.png)