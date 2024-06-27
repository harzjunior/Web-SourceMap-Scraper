import requests

# Set headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://edemy-react.envytheme.com/_next/static/chunks/fd9d1056-c0b11a5631d50738.js"
response = requests.get(url, headers=HEADERS)

with open("example.js", "w", encoding="utf-8") as file:
    file.write(response.text)

print(response.text[:500])  # Print the first 500 characters to inspect
