import argparse
from PIL import Image # Reads and manipulates images
from cryptography.fernet import Fernet #Symmetric encryption protocol
import base64
import os

#Helper functions for key generation and loading
def generate_key(path="secret.key"):
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)
    print(f"Key generated and saved to {path}")
    return key
def load_key(path="secret.key"):
    return open(path, "rb").read()

def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode() #Encoding to make it easier storable in images

def decrypt_message(encrypted_message, key):
    fernet =Fernet(key)
    decoded_message = base64.b64decode(encrypted_message.encode())
    decrypted_message = fernet.decrypt(decoded_message).decode()
    return decrypted_message

def hide_message_in_image(image_path, message, output_path):
    #Load image
    image = Image.open(image_path)
    image = image.convert('RGB') #Ensures image in in RGB color format
    pixels = image.load()

    #Convert message to binary to be hidden in the LSB of pixels
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    binary_message += '1111111111111110'  # Indicates end of message

    width, height = image.size
    total_num_pixels = width * height
    needed_amount_of_bits = len(binary_message)
    if needed_amount_of_bits > total_num_pixels * 3: # Each pixel has 3 bits of data for RGB
        raise ValueError("Message is too long to hide in the provided image.")
    image_index = 0
    #Traverse through each pixel of the image, and modify the lsb to match the bit of the message
