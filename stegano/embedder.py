# Code pour insérer une image chiffrée dans une autre (LSB)
# stegano/embedder.py

from PIL import Image
import numpy as np

def embed_data(cover_path: str, data: bytes, output_path: str) -> None:
    img = Image.open(cover_path)
    img = img.convert("RGB")
    np_img = np.array(img)
    flat = np_img.flatten()

    # Convert data to bits
    bits = ''.join(format(byte, '08b') for byte in data)
    bits += '1111111111111110'  # End marker

    if len(bits) > len(flat):
        raise ValueError("Image too small to hold the data.")

    for i in range(len(bits)):
        flat[i] = (flat[i] & ~1) | int(bits[i])

    stego_array = flat.reshape(np_img.shape)
    stego_img = Image.fromarray(stego_array.astype('uint8'))
    stego_img.save(output_path)
