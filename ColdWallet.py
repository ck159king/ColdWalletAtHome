import generate_addr
import os
from Crypto.PublicKey import ECC
def encrypt_pendrive(device):
    """
    Encrypts a pendrive using LUKS.
    
    Args:
        device (str): The block device path (e.g., /dev/sdb1).
        passphrase (str): The passphrase for LUKS encryption.
    """
    try:
        # # Step 1: Format the device with LUKS
        print(f"------Formatting {device} with LUKS...---- ")
        os.system(f"sudo cryptsetup -y -v luksFormat {device}")
        print("LUKS formatting completed successfully.")

        # # Step 2: Open the encrypted volume
        luks_name = "encrypted_pendrive"
        print(f"-------Opening encrypted volume as {luks_name}...")
        os.system(f"sudo cryptsetup luksOpen {device} {luks_name}")
        print("--------Encrypted volume opened successfully.")

        # # Step 3: Create a filesystem on the encrypted volume
        mapper_device = f"/dev/mapper/{luks_name}"
        print(f"--------Creating ext4 filesystem on {mapper_device}...")
        os.system(f"sudo mkfs.ext4 {mapper_device}")
        print("---------Filesystem created successfully.")

        # # Step 4: Mount the encrypted volume
        mount_point = "/mnt/encrypted_pendrive"
        print(f"-------Mounting {mapper_device} to {mount_point}...")
        os.system(f"sudo mkdir -p {mount_point}")
        os.system(f"sudo mount {mapper_device}  {mount_point}")
        print(f"-------Encrypted pendrive mounted at {mount_point}.")

        # Step 5: Generating Private key
        print("-------Generating private key")
        generate_addr.gen(mount_point)

        # Step 6: Copy the python file to the drive
        print(f"-------Copying Files to {mount_point}")
        os.system(f"sudo cp all.py {mount_point}")

        # Step 7: unmounting
        print(f"--------Unmounting drive")
        os.system(f"sudo umount {mount_point}")
        os.system(f"sudo cryptsetup luksClose {mapper_device}")
    finally:
        print("Process completed.")

def load_private_key_from_der(file_path):
    try:
        # Load the private key from the DER file
        with open(file_path, "rb") as der_file:
            der_data = der_file.read()
        
        # Import the private key using PyCryptodome
        ecc_private_key = ECC.import_key(der_data)
        
        # Extract the private key integer (d)
        private_key_int = ecc_private_key.d
        
        # Convert the integer to hexadecimal format
        hex_private_key = hex(private_key_int)[2:]  # Remove '0x' prefix
        print(hex_private_key)
        return hex_private_key

    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

def sign(device):

    luks_name = "encrypted_pendrive"
    print(f"-------Opening encrypted volume as {luks_name}...")
    os.system(f"sudo cryptsetup luksOpen {device} {luks_name}")
    print("--------Encrypted volume opened successfully.")

    mapper_device = f"/dev/mapper/{luks_name}"
    mount_point = "/mnt/encrypted_pendrive"
    print(f"-------Mounting {mapper_device} to {mount_point}...")
    os.system(f"sudo mkdir -p {mount_point}")
    os.system(f"sudo mount {mapper_device}  {mount_point}")
    print(f"-------Encrypted pendrive mounted at {mount_point}.")
    os.system(f"cd {mount_point} ; python3 {mount_point}/all.py")
    # Step 7: unmounting
    print(f"--------Unmounting drive")
    os.system(f"sudo umount {mount_point}")
    os.system(f"sudo cryptsetup luksClose {mapper_device}")
    
def wallet_addr(device):
    mount_point = "/mnt/encrypted_pendrive"
    luks_name = "encrypted_pendrive"
    print(f"-------Opening encrypted volume as {luks_name}...")
    os.system(f"sudo cryptsetup luksOpen {device} {luks_name}")
    print("--------Encrypted volume opened successfully.")

    mapper_device = f"/dev/mapper/{luks_name}"
    mount_point = "/mnt/encrypted_pendrive"
    print(f"-------Mounting {mapper_device} to {mount_point}...")
    os.system(f"sudo mkdir -p {mount_point}")
    os.system(f"sudo mount {mapper_device}  {mount_point}")
    print(f"-------Encrypted pendrive mounted at {mount_point}.")
    print("wallet address" , generate_addr.checksum_encoded_Wallet_addr( load_private_key_from_der(mount_point + "/private_key.der")))
    print(f"--------Unmounting drive")
    os.system(f"sudo umount {mount_point}")
    os.system(f"sudo cryptsetup luksClose {mapper_device}")
# Example usage
if __name__ == "__main__":
    # Replace '/dev/sdX' with your actual pendrive device path
    device_path = input("Enter the pendrive device path (e.g., /dev/sdb1): ")   
    print("Choose your option:")
    print(" [1] setup new wallet ")
    print(" [2] Sign a transaction")
    print(" [3] Print wallet address")
    i = int(input())
    if i==1:
        encrypt_pendrive(device_path)
    if i==2:
        sign(device_path)
    if i==3:
        wallet_addr(device_path)
    else:
        print("enter 1 or 2 to select the option")
