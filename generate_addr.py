import secrets
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256 , keccak
import ecdsa
import subprocess
import os
def checksum_encoded_Wallet_addr(private_key): # Takes a 20-byte binary address as input
    private_key_bytes = bytes.fromhex(private_key)

    singing_key = ecdsa.SigningKey.from_string(private_key_bytes , curve=ecdsa.SECP256k1)

    public_key_bytes= singing_key.verifying_key.to_string()

    keccak_hash = keccak.new(digest_bits=256)

    keccak_hash.update(public_key_bytes)
    k = keccak_hash.digest()
    hex_addr = k[-20:].hex()
    checksummed_buffer = ""

    # Treat the hex address as ascii/utf-8 for keccak256 hashiing
    hashed_address = keccak.new(digest_bits=256)
    hashed_address.update(hex_addr.encode('utf-8'))
    hashed_address = hashed_address.digest().hex()
    # Iterate over each character in the hex address
    for nibble_index, character in enumerate(hex_addr):

        if character in "0123456789":
            # We can't upper-case the decimal digits
            checksummed_buffer += character
        elif character in "abcdef":
            # Check if the corresponding hex digit (nibble) in the hash is 8 or higher
            hashed_address_nibble = int(hashed_address[nibble_index], 16)
            if hashed_address_nibble > 7:
                checksummed_buffer += character.upper()
            else:
                checksummed_buffer += character
        else:
            print("err")

    return "0x" + checksummed_buffer

def generate_private_key():
    """
    Generate a random 256-bit private key in hexadecimal format.
    """
    private_key = secrets.randbits(256)
    hex_private_key = hex(private_key)[2:]  # Remove '0x' prefix
    return hex_private_key

def save_private_key_to_der(private_key_hex, filename , path):
    """
    Save the private key in DER format to a file.
    """
    # Convert the hex private key to an integer
    private_key_int = int(private_key_hex, 16)
    
    # Generate an ECC private key object using PyCryptodome
    ecc_private_key = ECC.construct(curve="P-256", d=private_key_int)
    
    # Export the private key in DER format
    der_data = ecc_private_key.export_key(format="DER")
    
    # Save to file
    temp_file = "/tmp/temp_file.der"
    with open(temp_file, "wb") as f:
        f.write(der_data)
    # Move the temporary file to the root-owned directory using sudo
    root_path = f"/{path}/{filename}"
    subprocess.run(["sudo", "mv", temp_file, root_path], check=True)
    print(f"File saved to {root_path} as root.")

def gen(path):
    # Step 1: Generate a private key
    private_key_hex = generate_private_key()
    print("Generated Private Key (Hex):", private_key_hex)
    
    # Step 2: Save the private key in DER format
    der_filename = "private_key.der"
    save_private_key_to_der(private_key_hex, der_filename , path)
    print(f"Private key saved in DER format to {der_filename}")
    
    # Step 3: Generate and display the wallet address
    wallet_address = checksum_encoded_Wallet_addr(private_key_hex)
    print("Wallet Address:", wallet_address)
