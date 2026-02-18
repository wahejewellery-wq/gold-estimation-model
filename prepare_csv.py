import pandas as pd
import os
from urllib.parse import urlparse, unquote

def prepare_data():
    csv_file = 'dataset_ring/filtered_data.csv'
    image_dir = 'dataset_ring'
    output_file = 'dataset_ring/data_with_images.csv'
    
    print(f"Loading {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return

    print(f"Found {len(df)} rows.")
    
    # Get set of local files for fast lookup
    if not os.path.exists(image_dir):
        print(f"Error: {image_dir} directory not found.")
        return
        
    local_files = set(os.listdir(image_dir))
    print(f"Found {len(local_files)} files in {image_dir}.")
    
    def get_local_path(url):
        if not isinstance(url, str):
            return None
        try:
            path = urlparse(url).path
            filename = os.path.basename(unquote(path))
            if filename in local_files:
                return filename
        except:
            return None
        return None

    # Apply to Image 1
    print("Mapping Image 1 to local files...")
    df['LocalImage'] = df['Image 1'].apply(get_local_path)
    
    # Count matches
    matches = df['LocalImage'].notna().sum()
    print(f"Found {matches} rows with matching local images.")
    
    # Save
    df.to_csv(output_file, index=False)
    print(f"Saved updated CSV to {output_file}")

if __name__ == "__main__":
    prepare_data()
