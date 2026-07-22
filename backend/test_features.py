from features import extract_features

url = "https://www.google.com"

f = extract_features(url)

print(f)

print("Number of Features =", len(f))