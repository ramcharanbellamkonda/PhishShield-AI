import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    parsed = urlparse(url)
    hostname = parsed.netloc

    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)
    features.append(len(url))
    features.append(1 if any(x in url for x in ["bit.ly", "tinyurl", "goo.gl"]) else 0)
    features.append(1 if '@' in url else 0)
    features.append(1 if url.count("//") > 1 else 0)
    features.append(1 if '-' in hostname else 0)
    features.append(hostname.count('.'))
    features.append(1 if "https" in hostname else 0)

    suspicious_words = ["login", "secure", "update", "verify", "bank"]
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    features.append(len(hostname))

    return features