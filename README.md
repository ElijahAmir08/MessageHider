# MessageHider 🕵🏽‍♂️🔐

A Python-based tool to securely **encrypt** messages and **hide messages in images** using least significant bit (LSB) manipulation and Fernet symmetric encryption. 

## 💭 Design Overview & Inspiration
Recently I remembered learning about Cloudflare's wall of lava lamps for secure encryption. As I have now more formarlly learned about different types of encryptions. I figured why not try to make my own encryption tool that takes in images!
Why did I use the things that I did?
  1.) LSB Steganography: A simple way to hide data within the pixels of an image, and does not alter the quality of the image by much
  2.) Fernet encryption: Combines the goal of stealth with confidence, since this has many built in features with AES-based encryption. Helps my tool follow the best practices that it can.
  3.) PNG files were used, because it preserves every pixel exactly making it ideal for steganography. Unlike other file types such as JPEG which use lossy compression and can lose data. 

## Features
- 🔐 AES-based symmetric encryption (Fernet)
- 🖼️ Steganography using RGB pixel manipulation
- 🧠 Detects end of message with a 16-bit EOF marker
- 📦 Command-line interface using argparse
- 🔑 Saves/loads encryption key for message recovery

## Usage

### Hide a message:

```bash
python MessageHider.py hide -i Rabbit-PNG.png -m "The rabbit knows." -o stego.png

