import re

def extract_features(url):
    return [
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,  # IP address
        len(url),                                          # URL length
        1 if '-' in url else 0,                            # prefix-suffix
        1 if '@' in url else 0,                            # @ symbol
        url.count('.'),                                    # subdomains
    ]