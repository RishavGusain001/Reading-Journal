### image_utils.py
from PIL import Image
import os

def resize_image(image_path, output_path, size=(100, 150)):
    try:
        img = Image.open(image_path)
        img = img.resize(size)
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
