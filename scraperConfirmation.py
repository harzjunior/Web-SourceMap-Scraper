import requests
from bs4 import BeautifulSoup

def get_js_files(url, headers):
    """Fetch the webpage and return a list of JavaScript file URLs."""
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    script_tags = soup.find_all("script", src=True)

    js_files = [tag['src'] for tag in script_tags if tag['src'].endswith('.js')]
    return js_files

def check_source_maps(js_url, headers):
    """Check if a JavaScript file has a source map."""
    response = requests.get(js_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch {js_url}, status code: {response.status_code}")
        return False

    if 'sourceMappingURL' in response.text:
        return True
    return False

def check_keyword(js_url, headers, keyword):
    """Check if a JavaScript file contains a specific keyword."""
    response = requests.get(js_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch {js_url}, status code: {response.status_code}")
        return False

    if keyword in response.text:
        return True
    return False

def main(url, keyword):
    """Main function to check for source maps and keywords on a website."""
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    js_files = get_js_files(url, HEADERS)
    
    if not js_files:
        print("No JavaScript files found.")
        return

    print(f"Found {len(js_files)} JavaScript files.")

    source_map_found = False
    keyword_found = False
    for js_file in js_files:
        full_url = js_file if js_file.startswith('http') else url + js_file
        print(f"Checking {full_url} for source maps...")
        if check_source_maps(full_url, HEADERS):
            print(f"Source map found in {full_url}")
            source_map_found = True
        else:
            print(f"No source map found in {full_url}")

        print(f"Checking {full_url} for keyword '{keyword}'...")
        if check_keyword(full_url, HEADERS, keyword):
            print(f"Keyword '{keyword}' found in {full_url}")
            keyword_found = True
        else:
            print(f"Keyword '{keyword}' not found in {full_url}")

    if not source_map_found:
        print("No source maps found in any JavaScript files.")
    if not keyword_found:
        print(f"Keyword '{keyword}' not found in any JavaScript files.")

if __name__ == "__main__":
    # Replace 'https://example.com' with the target website URL and 'keyword' with the desired keyword
    main("https://html.merku.love/shelly/?storefront=envato-elements", "html")
