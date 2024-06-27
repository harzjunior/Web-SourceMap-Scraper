# Project Title: Web Source Map Scraper and Inspector

## Overview
This project consists of several Python scripts designed to scrape, inspect, and download JavaScript source maps and other web resources from a Next.js website. The scripts utilize `requests` for HTTP requests, `BeautifulSoup` for HTML parsing, and `base64` for decoding base64-encoded source maps.

## Scripts

### 1. `inspecting.py`
This script fetches a JavaScript file from a specified URL and saves it locally for inspection.

#### Usage
1. Update the `url` variable with the URL of the JavaScript file you want to inspect.
2. Run the script to download the file and print the first 500 characters of its content.

```python
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://sample.com/_next/static/chunks/fd9d1056-c0b11a5631d50738.js"
response = requests.get(url, headers=HEADERS)

with open("example.js", "w", encoding="utf-8") as file:
    file.write(response.text)

print(response.text[:500])
```

### 2. `scrape_nextjs_sourcemaps.py`
This script scrapes a Next.js website for JavaScript files, extracts their source map URLs or base64-encoded source maps, and saves them locally.

#### Usage
1. Update the `BASE_URL` variable with the URL of the Next.js website you want to scrape.
2. Run the script to fetch JavaScript files and their corresponding source maps.

```python
# Configuration
OUTPUT_DIR = "output"
BASE_URL = "https://sample.com"
...
if __name__ == "__main__":
    main()
```

### 3. `scraper.py`
This script is similar to `scrape_nextjs_sourcemaps.py`, with minor adjustments. It scrapes a website for JavaScript files, extracts their source maps, and saves them locally.

#### Usage
1. Update the `BASE_URL` variable with the URL of the website you want to scrape.
2. Run the script to download JavaScript files and their source maps.

```python
# Configuration
OUTPUT_DIR = "output"
BASE_URL = "https://sample.com"
...
if __name__ == "__main__":
    main()
```

### 4. `scraperConfirmation.py`
This script checks if JavaScript files on a website contain source maps and a specific keyword.

#### Usage
1. Update the `url` variable with the URL of the website you want to check.
2. Update the `keyword` variable with the keyword you want to search for in the JavaScript files.
3. Run the script to check for source maps and the keyword.

```python
if __name__ == "__main__":
    main("https://sample.com", "html")
```

### 5. `webDownloader.py`
This script downloads the complete web content from a URL, including HTML, CSS, JavaScript files, and images, and saves them locally.

#### Usage
1. Update the `url` variable with the URL of the website you want to download.
2. Run the script to download the website's content and save it locally.

```python
if __name__ == "__main__":
    main("https://sample.com")
```

## Requirements
- Python 3.x
- `requests`
- `beautifulsoup4`

Install the required packages using pip:

```sh
pip install requests beautifulsoup4
```

## Notes
- Ensure you have permission to scrape and download content from the website.
- Modify the `HEADERS` variable if you encounter issues with HTTP requests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.