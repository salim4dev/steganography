# Fonctions de conversion d'images et manipulation pixel/bit
# stegano/image_utils.py

from PIL import Image
import io

def image_to_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def bytes_to_image(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))

def save_image(image: Image.Image, path: str) -> None:
    image.save(path)
