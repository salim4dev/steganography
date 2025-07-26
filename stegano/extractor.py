# Code pour extraire l'image cachée et la déchiffrer
# stegano/extractor.py

from PIL import Image
import numpy as np

def extract_data(stego_path: str) -> bytes:
    img = Image.open(stego_path)
    img = img.convert("RGB")
    np_img = np.array(img)
    flat = np_img.flatten()

    bits = []
    for value in flat:
        bits.append(str(value & 1))

    bit_string = ''.join(bits)
    end_marker = '1111111111111110'
    end_idx = bit_string.find(end_marker)

    if end_idx == -1:
        raise ValueError("No hidden data found.")

    useful_bits = bit_string[:end_idx]
    byte_array = bytearray()
    for i in range(0, len(useful_bits), 8):
        byte_array.append(int(useful_bits[i:i+8], 2))

    return bytes(byte_array)
