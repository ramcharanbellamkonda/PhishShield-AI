import re
import math
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login","signin","verify","update","secure",
    "account","bank","paypal","password","confirm",
    "wallet","free","bonus","gift","win","ebayisapi",
    "webscr","client","admin"
]

SHORTENERS = [
    "bit.ly","goo.gl","tinyurl","ow.ly",
    "t.co","buff.ly","is.gd","cutt.ly"
]

SUSPICIOUS_TLDS = [
    ".tk",".ml",".ga",".cf",".gq"
]

def entropy(text):
    prob = [float(text.count(c))/len(text) for c in dict.fromkeys(list(text))]
    return -sum([p * math.log2(p) for p in prob])

def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()

    features = []

    # Length Features
    features.append(len(url))
    features.append(len(domain))
    features.append(len(path))
    features.append(len(query))

    # Character Counts
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('_'))
    features.append(url.count('/'))
    features.append(url.count('?'))
    features.append(url.count('='))
    features.append(url.count('&'))
    features.append(url.count('@'))
    features.append(url.count('%'))

    # Digits
    features.append(sum(c.isdigit() for c in url))

    # HTTPS
    features.append(int(url.startswith("https://")))

    # HTTP
    features.append(int(url.startswith("http://")))

    # IP Address
    features.append(
        int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", url)))
    )

    # URL Shortener
    features.append(
        int(any(x in domain for x in SHORTENERS))
    )

    # Subdomains
    features.append(domain.count('.'))

    # Long URL
    features.append(int(len(url) > 75))

    # Entropy
    features.append(entropy(url))

    # Suspicious keywords
    features.append(
        sum(word in url.lower() for word in SUSPICIOUS_WORDS)
    )

    # Suspicious TLD
    features.append(
        int(any(domain.endswith(t) for t in SUSPICIOUS_TLDS))
    )

    # Path Depth
    features.append(path.count('/'))

    # Query Parameters
    features.append(query.count('&'))

    # Special Character Ratio
    special = sum(not c.isalnum() for c in url)
    features.append(special / len(url))

    # Uppercase Ratio
    upper = sum(c.isupper() for c in url)
    features.append(upper / len(url))

    return features