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
    message_index = 0
    #Traverse through each pixel of the image, and modify the lsb to match the bit of the message
    for y in range(height):
        for x in range(width):
            if message_index >= needed_amount_of_bits:
                break
            r, g, b = pixels[x,y]
            rgb = [r, g, b]
            for i in range(3): #For each color
                if message_index < needed_amount_of_bits:
                    #Modify the LSB, by clearing the last bit of the binary version of the rgb value. Then set it to the bit of the message
                    rgb[i] = (rgb[i] & ~1) | int(binary_message[message_index])
                    message_index += 1
            pixels[x,y] = tuple(rgb) # Update the pixel with modified rgb values
        if message_index >= needed_amount_of_bits:
            break
    image.save(output_path)
    print(f"Message hidden in image and saved to {output_path}")

def extract_message_from_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = image.load()
    width, height = image.size
    binary_message = ""
    #Traverse through the pixels and extract the LSBs to reconstruct the binary message
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x,y]
            for color in (r, g, b):
                binary_message += str(color & 1)  # Extract LSB
                #The message is done when specific marker is found
                if binary_message[-16:] == '1111111111111110':
                    #Remove this marker from the message
                    binary_message = binary_message[:-16]
                    #Convert bits to characters
                    characters = []
                    for i in range(0, len(binary_message), 8):
                        characters.append(binary_message[i:i+8])
                    message = ''.join([chr(int(c, 2)) for c in characters]) #Converts the binary to an integer, to be converted to a characrter and added to the string
                    return message
    return None  # No message found
def main():
    parser = argparse.ArgumentParser(description = "Steganography Message Hider")
    subparsers = parser.add_subparsers(dest="command", help = "Hide or Reveal")
    #Commands to hide
    hide_parser = subparsers.add_parser("hide", help="Hide a message in an image")
    hide_parser.add_argument("-i", "--image", required=True, help="Path to the input image")
    hide_parser.add_argument("-m", "--message", required=True, help="Message to hide")
    hide_parser.add_argument("-o", "--output", required=True, help="Path to save the output image with hidden message")
    hide_parser.add_argument("-k", "--key", default = "secret.key", help = "Path to the encryption key file (default: secret.key)")
    #Commands to reveal
    reveal_parser = subparsers.add_parser("reveal", help="Reveal a hidden message from an image")
    reveal_parser.add_argument("-i", "--image", required=True, help="Path to the image with hidden message")
    reveal_parser.add_argument("-k", "--key", default = "secret.key", help = "Path to the encryption key file (default: secret.key)")
    args = parser.parse_args()

    if args.command == "hide":
        key = generate_key(args.key)
        encrypted_message = encrypt_message(args.message, key)
        hide_message_in_image(args.image, encrypted_message, args.output)
    elif args.command == "reveal":
        encrypted_message = extract_message_from_image(args.image)
        if encrypted_message is None:
            print("No hidden message found in the image.")
        else:
            key = load_key(args.key)
            decrypted_message = decrypt_message(encrypted_message, key)
            print("Hidden message: ", decrypted_message)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
