import csv
import requests
import os
import concurrent.futures
from urllib.parse import urlparse

# File paths
CSV_FILE = 'filtered_data.csv'
DOWNLOAD_DIR = 'downloaded_images2'

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_image(url):
    """Downloads a single image from the given URL."""
    if not isinstance(url, str) or not url.strip():
        return

    try:
        # Extract filename from URL (remove query parameters)
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If filename is empty or invalid, generate a unique name or skip
        if not filename:
             return

        filepath = os.path.join(DOWNLOAD_DIR, filename)

        # Skip if file already exists
        if os.path.exists(filepath):
            # print(f"Skipping {filename}, already exists.")
            return

        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    # Read CSV using csv module
    image_urls = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Image 1' in row and row['Image 1']:
                    image_urls.append(row['Image 1'])
                if 'Image 2' in row and row['Image 2']:
                    image_urls.append(row['Image 2'])

    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Remove duplicates
    image_urls = list(set(image_urls))
    
    print(f"Found {len(image_urls)} unique images to download.")

    # Download images concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_image, image_urls)

    print("Download complete.")

if __name__ == "__main__":
    main()
