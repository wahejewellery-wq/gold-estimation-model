import requests
import os

url = "http://127.0.0.1:8000/predict"
image_path = "backend/valid_test.jpg"  # Assuming valid_test.jpg exists from previous tests

def test_category(category):
    print(f"Testing Category: {category}")
    try:
        with open(image_path, "rb") as f:
            files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
            data = {"category": category, "purity": "22"}
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                print(f"Success! Response: {response.json()}")
            else:
                print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    print("-" * 40)

if __name__ == "__main__":
    if not os.path.exists(image_path):
        print(f"Test image not found at {image_path}. Please create one or modify the path.")
    else:
        for cat in ["ring", "bangle", "necklace", "earring"]:
            test_category(cat)
