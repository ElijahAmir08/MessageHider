# MessageHider 🕵🏽‍♂️🔐

A Python tool to securely hide encrypted messages inside images using LSB (Least Significant Bit) steganography and Fernet encryption.

## Features
- 🔐 AES-based symmetric encryption (Fernet)
- 🖼️ Steganography using RGB pixel manipulation
- 🧠 Detects end of message with a 16-bit EOF marker
- 📦 Command-line interface using argparse
- 🔑 Saves/loads encryption key for message recovery

## Usage

### Hide a message:

```bash
python MessageHider.py hide -i input.png -m "Secret message" -o stego.png

