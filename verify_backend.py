import requests
import os

# usage: python3 verify_backend.py [local|remote]

URLS = {
    "local": "http://localhost:8000/predict",
    "remote": "https://backend-rh7d.onrender.com/predict"
}

target = "remote" # Default to remote for diagnosing deployment

print(f"Testing {target} backend at {URLS[target]}...")

from PIL import Image
import io

# Create valid dummy image
img = Image.new('RGB', (100, 100), color = 'white')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='JPEG')
img_byte_arr.seek(0)

files = {
    'image': ('test_image.jpg', img_byte_arr, 'image/jpeg')
}
data = {
    'category': 'ring',
    'purity': '22'
}

try:
    response = requests.post(URLS[target], files=files, data=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        json_data = response.json()
        print("Response JSON:")
        print(json_data)
        
        data_obj = json_data.get('data', {})
        print("\nKeys in data object:", data_obj.keys())
        
        required_keys = ['gold_weight', 'diamond_weight']
        missing = [k for k in required_keys if k not in data_obj]
        
        if missing:
            print(f"❌ MISSING KEYS: {missing}")
        else:
            print("✅ Keys check passed.")
            
    else:
        print("❌ Request failed.")
        print(response.text)

except Exception as e:
    print(f"❌ Exception: {e}")

