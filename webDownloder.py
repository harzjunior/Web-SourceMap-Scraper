import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import time

def download_file(url, save_path, headers, max_retries=3, delay=5):
    """Download a file from a URL and save it locally, with retries."""
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                if os.path.isdir(save_path):
                    filename = url.split('/')[-1]
                    save_path = os.path.join(save_path, filename)
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {url} to {save_path}")
                return True
            else:
                print(f"Failed to download {url}, status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {delay} seconds... (Attempt {retries + 1} of {max_retries})")
                time.sleep(delay)
    print(f"Failed to download {url} after {max_retries} attempts")
    return False

def save_html(content, save_path):
    """Save HTML content to a local file."""
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_local_path(url, base_path):
    """Generate a local file path for a URL."""
    parsed_url = urlparse(url)
    local_path = os.path.join(base_path, parsed_url.path.lstrip('/'))
    if local_path.endswith('/'):
        local_path += 'index.html'
    return local_path

def create_directories_for_file(file_path):
    """Create directories for a file path if they don't exist."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_resources(soup, tag, attribute, base_url, base_path, headers):
    """Download all resources of a given tag and attribute from the HTML."""
    for element in soup.find_all(tag):
        url = element.get(attribute)
        if url:
            full_url = urljoin(base_url, url)
            local_path = get_local_path(full_url, base_path)
            create_directories_for_file(local_path)
            if download_file(full_url, local_path, headers):
                element[attribute] = os.path.relpath(local_path, base_path)

def main(url):
    """Download complete web content from a URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = url

    # Determine the script directory and create a unique 'src' directory there
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    save_directory = os.path.join(script_dir, f'src_{timestamp}')

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    base_path = save_directory

    # Download and update links for CSS files
    download_resources(soup, 'link', 'href', base_url, base_path, headers)
    # Download and update links for JavaScript files
    download_resources(soup, 'script', 'src', base_url, base_path, headers)
    # Download and update links for images
    download_resources(soup, 'img', 'src', base_url, base_path, headers)

    # Save the modified HTML content
    html_save_path = os.path.join(save_directory, 'index.html')
    save_html(soup.prettify(), html_save_path)
    print(f"HTML content saved to {html_save_path}")

if __name__ == "__main__":
    main("https://preview.keenthemes.com/metronic8/demo1/index.html")
