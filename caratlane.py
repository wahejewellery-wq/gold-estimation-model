import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import sys
import copy

import subprocess

import os

def fetch_and_extract(url):
    html_content = None
    
    # 1. Try local file
    if os.path.exists(url):
        try:
            with open(url, 'r') as f:
                html_content = f.read()
        except Exception as e:
            print(f"Error reading local file {url}: {e}")
            return None
            
    # 2. Try curl via subprocess
    else:
        try:
            ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            with open('temp_page.html', 'w') as f:
                # Use --max-time to prevent hanging
                result = subprocess.run(['curl', '-s', '-A', ua, '-L', '--max-time', '45', url], stdout=f, stderr=subprocess.PIPE, text=True, timeout=60)
            
            if result.returncode == 0:
                with open('temp_page.html', 'r') as f:
                    html_content = f.read()
                if not html_content:
                    print("Curl output empty.")
            else:
                print(f"Curl failed for {url} with code {result.returncode}, stderr: {result.stderr}")
                print("Falling back to requests.")
                headers = {
                    'User-Agent': 'curl/8.7.1' 
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                html_content = response.text

        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    
    script_content = None
    for script in soup.find_all('script'):
        if script.string and 'window.__PRELOADED_STATE__' in script.string:
            script_content = script.string
            break
            
    if not script_content:
        print(f"Could not find data script in {url}")
        return None

    try:
        json_str = script_content.split('window.__PRELOADED_STATE__ = ', 1)[1]
        data, _ = json.JSONDecoder().raw_decode(json_str)
        return data
    except Exception as e:
        print(f"Error parsing JSON from {url}: {e}")
        return None

def extract_product_info(data, url):
    # Extract details from a specific page's data
    try:
        # Navigate to product info
        # Based on debug_data.json: data['appWrapper']['productInfo'] ???
        # Wait, inside debug_data.json, productInfo was at top level of ... something?
        # Let's re-verify the structure from debug_data.json
        # It was inside "productInfo": { ... } at line 43289
        # But what is the PARENT of productInfo?
        # Reading lines 43275-43289 showed:
        # "pdpagePriceOffer": ...,
        # "productInfo": { ... }
        # And scanning up, I saw "appWrapper" at line 11.
        # But "appWrapper" had "dashDeliveryEligibility".
        # Where does "pdpagePriceOffer" come from?
        # Lines 43276.
        # It seems "appWrapper" ENDed? No, indentation suggests it's inside "appWrapper"?
        # Let's check indentation of "appWrapper" (line 11) -> 2 spaces.
        # "productInfo" (line 43289) -> 4 spaces? No, 6 spaces?
        # Let's assume data['appWrapper']['productInfo'] is the path.
        
        info = data.get('appWrapper', {}).get('productInfo', {})
        if not info:
             # Try alternate path just in case
             pass

        # 1. Product Category
        # From breadcrumbs in 'seo' section
        category = "Unknown"
        seo = data.get('appWrapper', {}).get('seo', {})
        # Or info.get('seo') if it's there
        if not seo:
             seo = info.get('seo', {})
             
        breadcrumbs = seo.get('breadcrumbs', [])
        if breadcrumbs:
            # Usually the last one is product name, second to last is category
            if len(breadcrumbs) >= 2:
                 category = breadcrumbs[-2].get('title', 'Unknown')

        # 2. Diamond Weight
        # From 'diamond_type' or descriptions
        diamond_weight = "0"
        
        # Look for diamond weight in description
        desc = info.get('description', '')
        # "Set in 14 KT Yellow Gold(2.110 g) with diamonds (0.098 ct ,FG-SI)"
        
        d_match = re.search(r'(\d+\.?\d*)\s*ct', desc, re.IGNORECASE)
        if d_match:
            diamond_weight = d_match.group(1)
        
        # 3. Images (3 links)
        images = []
        media = info.get('media', [])
        for m in media:
            if m.get('url'):
                images.append(m['url'])
        
        img1 = images[0] if len(images) > 0 else ""
        img2 = images[1] if len(images) > 1 else ""
        img3 = images[2] if len(images) > 2 else ""

        # 4. Weight
        # info['weight']
        weight = info.get('weight', '')
        # Clean up "2.110 g" -> "2.110"
        if 'g' in weight:
            weight = weight.replace('g', '').strip()
            
        return {
            'Category': category,
            'Diamond Weight': diamond_weight,
            'Gold Weight': weight,
            'Image 1': img1,
            'Image 2': img2,
            'Image 3': img3,
            'Purity': "Unknown", # To be filled
            'Product URL': url
        }

    except Exception as e:
        print(f"Error extracting info: {e}")
        return None

def get_variants(data):
    # Extract variant SKUs from the 'customize' section
    variants = {} # purity -> SKU
    try:
        # Try finding productInfo in productPage (most likely) or appWrapper (if schema changes)
        product_page = data.get('productPage', {})
        print("ProductPage keys:", list(product_page.keys()))
        info = product_page.get('productInfo', {})
        
        if not info:
             # Fallback
             app_wrapper = data.get('appWrapper', {})
             info = app_wrapper.get('productInfo', {})
             
        if not info:
             print("productInfo not found in productPage or appWrapper")
             # Debug top level keys
             print("Top level keys:", list(data.keys()))
             return {}
             
        customize = info.get('customize', {})
        if not customize:
             print("customize section not found in productInfo")
             return {}
             
        sections = customize.get('sections', [])
        print(f"Found {len(sections)} sections in customize")
        for i, sec in enumerate(sections):
             print(f"Section {i} ID: {sec.get('id')}")
        
        size_section = None
        for sec in sections:
            if sec.get('id') == 'size':
                size_section = sec
                break
        
        if not size_section:
            return {}

        # Get default/selected size
        selected_size = size_section.get('selected', '12') # Default to 12 if not found
        
        options = size_section.get('options', [])
        
        # Find the option block for the selected size
        size_block = None
        for opt in options:
            if opt.get('id') == selected_size or opt.get('title_1') == selected_size:
                size_block = opt
                break
        
        if not size_block:
             # Fallback: take the first size?
             if options:
                size_block = options[0]

        if size_block:
            # Iterate through keys to find metals
            # Keys look like "14 KT_Yellow", "18 KT_White", etc.
            # But the structure is "14 KT_Yellow": { "FG-SI": { sku: ... } }
            # We want to support all diamond qualities? 
            # Usually we pick the default quality or just the first one.
            # Let's iterate all keys in size_block
            
            for key, val in size_block.items():
                if 'KT' in key:
                    # key example: "18 KT_Yellow"
                    purity = key.split('_')[0] # "18 KT"
                    
                    # val is a dict of diamond qualities
                    # e.g. "GH-VS": { sku: ... }
                    # Just pick the first available sku
                    if isinstance(val, dict):
                         first_quality = next(iter(val))
                         sku_data = val[first_quality]
                         sku = sku_data.get('sku')
                         if sku:
                             # Key by purity (e.g., "18 KT")
                             # If multiple Colors (Yellow, White, Rose), maybe prefer Yellow?
                             # The user asked for rows for 14k, 18k.
                             # If we have 18k Yellow and 18k White, should we list both?
                             # User said "gold purity all 14k 18k 19k". 
                             # distinct rows.
                             # Let's include color in the purity column to be distinct? 
                             # e.g. "18 KT Yellow", "18 KT White"
                             
                             variant_name = key.replace('_', ' ')
                             variants[variant_name] = sku

    except Exception as e:
        print(f"Error finding variants: {e}")
        
    return variants

def main(url):
    data = fetch_and_extract(url)
    if not data:
        return

    # 1. Get variants from the main page
    variants_map = get_variants(data)
    
    # 2. Also extract info for the current page (which is one of the variants)
    # But wait, we should just iterate through variants found and fetch them to be consistent.
    # However, one of them IS the current page, so we can save a request.
    
    # Find current SKU
    current_sku = data.get('appWrapper', {}).get('productInfo', {}).get('sku')
    
    results = []
    
    # Filter for desired purities? User said "all 14k 18k 19k if available".
    # My variants_map has everything found.
    
    # If local file, use a dummy URL for template construction
    if os.path.exists(url):
         target_url = "https://www.caratlane.com/jewellery/mesh-cluster-diamond-ring-jr05874-1ys300.html"
    else:
         target_url = url

    print(f"Found {len(variants_map)} variants.")

    base_url = target_url.split('.html')[0]
    
    # We need to strip the SKU from the URL.
    # A safe way is to find the SKU in the URL and replace it.
    
    url_template = None
    if current_sku and current_sku.lower() in target_url.lower():
         url_template = target_url.replace(current_sku.lower(), '{sku}')
         url_template = url_template.replace(current_sku, '{sku}') # just in case
    else:
        # Fallback regex replacement for the last part
        # .../name-sku.html
         match = re.search(r'(.+)-([a-zA-Z0-9-]+)\.html', target_url)
         if match:
             url_template = f"{match.group(1)}-{{sku}}.html"
             
    if not url_template:
        print("Could not determine URL pattern for variants.")
        # Continue if strictly for current variant? 
        # But loop depends on url_template for OTHER variants.
        if len(variants_map) > 1:
             print("Warning: Only processing current variant due to URL template failure.")

    processed_skus = set()

    for purity_label, sku in variants_map.items():
        if sku in processed_skus:
            continue
            
        print(f"Processing {purity_label} (SKU: {sku})...")
        
        # Check if this is the current page
        if sku == current_sku:
            variant_data = data
            variant_url = target_url
        else:
            if not url_template:
                 print(f"Skipping {sku} - no URL template")
                 continue
            variant_url = url_template.format(sku=sku.lower())
            variant_data = fetch_and_extract(variant_url)
        
        if variant_data:
            info = extract_product_info(variant_data, variant_url)
            if info:
                info['Purity'] = purity_label
                results.append(info)
        
        processed_skus.add(sku)

    # Output to CSV
    if results:
        df = pd.DataFrame(results)
        # Reorder columns as requested/logical
        cols = ['Product URL', 'Category', 'Purity', 'Gold Weight', 'Diamond Weight', 'Image 1', 'Image 2', 'Image 3']
        # Fill missing cols
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        
        print(df[cols].to_csv(index=False))
    else:
        print("No results generated.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.caratlane.com/jewellery/mesh-cluster-diamond-ring-jr05874-1ys300.html"
    main(url)
