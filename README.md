# ColdWalletAtHome
![pendrive image](img/image.jpg)
## Overview
**ColdWalletAtHome** is an Ethereum cold wallet designed for early-stage development. It is tailored for Linux users (I used WSL) and does not include a graphical user interface (GUI). This project provides a script that handles the signing process offline, effectively acting as a cold wallet when saved on a USB drive.

## Concept
The idea behind this project stems from the availability of various hardware wallet devices. I thought, "Why not create my own wallet using a USB drive?" After dedicating a week to learning about blockchain signing, elliptic curve cryptography, and related concepts, I developed this solution.

## How It Works
The provided Python script manages transactions and operates as a cold wallet. To ensure security, store the script on a LUKS-encrypted USB drive that is protected by a passphrase.

## TL;DR
1. Set up a new wallet on a USB drive.
2. Use the Python script to sign transactions.
3. Configure an Etherscan API key to eliminate the need for a JSON-RPC node.
4. The script generates a QR code that can be scanned to send an Etherscan request with the signed transaction hash. For enhanced privacy, use this tool offline.
# Setup
clone the project using 
```git clone https://github.com/ck159king/ColdWalletAtHome.git```

Check the location of your pendrive by using
```lsblk```

Run ``` python3 ColdWallet.py ```
provide it the data


### Important Note
- This tool is compatible with all EVM-compatible chains. To change networks, use the appropriate chain ID:
  - Mainnet: `1`
  - POLYGON: `137`
  - Sepolia: `11155111`

# Usage Instructions for WSL
## CHECK IF THESE MODULES ARE LOADED
``` sudo modprobe dm_crypt ``` 
and ``` sudo modprobe vhci_hcd ```

IF they return fatal error then you need to build you kernel
## Building wsl kernel
Install required packages
```sudo apt install build-essential flex bison libssl-dev libelf-dev libncurses5-dev git bc pahole```

Clone the WSL kernel files
``` git clone https://github.com/microsoft/WSL2-Linux-Kernel.git
cd WSL2-Linux-Kernel
export KCONFIG_CONFIG=Microsoft/config-wsl
make menuconfig
 ```
Then menu will appear
 ``` Device Drivers --->
    [*] Multiple devices driver support (RAID and LVM) --->
        <*> Device mapper support
    [*] USB Support --->
    	<*> USB/IP support 
```
then ``` sudo make -j$((nproc)*1.5) ```
the -jN option will enable multithreading. You can experiment with it

Now we will copy the kernel
``` cp arch/x86_64/boot/bzImage  /mnt/c/Users/USERNAME ```

Now exit wsl and write this command in cmd or powershell
``` wsl --shutdown ```
Now make a file .wslconfig in you ``` C:/Users/USERNAME ```
Add the following code
``` 
[wsl2]
kernel=C:\\Users\\USERNAME\\bzImage 
```
Now open wsl.
You may read this for to connect your pendrive to wsl.
[Connect USB devices](https://learn.microsoft.com/en-us/windows/wsl/connect-usb "OPEN THIS")
### Note:
```USERNAME``` : Replace with your username your windows username
Certain modules may not be loaded by default in WSL. You may need to compile the kernel to use `cryptsetup`, especially in WSL environments.

---

Feel free to adjust any specific details or add additional sections as needed!
