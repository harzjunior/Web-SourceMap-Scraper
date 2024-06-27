import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import base64

# Configuration
OUTPUT_DIR = "output"
BASE_URL = "https://edemy-react.envytheme.com"  # Replace with the Next.js website URL

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def find_js_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    script_tags = soup.find_all("script", src=True)
    js_urls = [urljoin(base_url, tag["src"]) for tag in script_tags]
    return js_urls

def extract_sourcemap_url(js_content):
    sourcemap_url_pattern = r"//# sourceMappingURL=(.+\.map)"
    base64_sourcemap_pattern = r"//# sourceMappingURL=data:application/json;base64,(.+)"

    url_match = re.findall(sourcemap_url_pattern, js_content)
    base64_match = re.findall(base64_sourcemap_pattern, js_content)

    return url_match, base64_match

def save_file(content, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')

def main():
    html = fetch(BASE_URL)
    if not html:
        return

    print("HTML content fetched successfully.")
    
    js_links = find_js_links(html, BASE_URL)
    print(f"Found {len(js_links)} JavaScript links.")
    if not js_links:
        print("No JavaScript links found.")
        return

    for js_link in js_links:
        print(f"Fetching JavaScript file: {js_link}")
        js_content = fetch(js_link)
        if not js_content:
            print(f"Failed to fetch JavaScript file: {js_link}")
            continue
        
        sourcemap_urls, base64_maps = extract_sourcemap_url(js_content)
        
        if sourcemap_urls:
            for sourcemap_url in sourcemap_urls:
                full_sourcemap_url = urljoin(js_link, sourcemap_url)
                print(f"Fetching source map URL: {full_sourcemap_url}")
                sourcemap_content = fetch(full_sourcemap_url)
                if sourcemap_content:
                    filename = f"{os.path.basename(js_link)}.map"
                    save_file(sourcemap_content, filename)
                    print(f"Saved source map from {full_sourcemap_url} as {filename}")
        elif base64_maps:
            for base64_map in base64_maps:
                sourcemap_content = decode_base64(base64_map)
                filename = f"{os.path.basename(js_link)}.map"
                save_file(sourcemap_content, filename)
                print(f"Saved source map from base64 data in {js_link} as {filename}")
        else:
            print(f"No source map found in JavaScript file: {js_link}")

if __name__ == "__main__":
    main()
