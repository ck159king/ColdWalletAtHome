from py_ecc.secp256k1 import *
from Crypto.Hash import keccak
from Crypto.PublicKey import ECC
import rlp
from rlp.sedes import big_endian_int,text
import sys
import qrcode
from PIL import Image

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
        
        return hex_private_key
    
    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

sys.set_int_max_str_digits(43000)
def k_h(inputt):
    keccak_hashh = keccak.new(digest_bits=256)
    return keccak_hashh.update(inputt).digest().hex()
private_key  = bytes.fromhex(load_private_key_from_der("private_key.der"))
class Txn(rlp.Serializable):
    fields = [
        # ('transactionType',big_endian_int),
        ('nonce',big_endian_int),
        ('gasPrice',big_endian_int),
        ('gasLimit',big_endian_int),
        ('to',big_endian_int),
        ('value',big_endian_int),
        ('data',big_endian_int),
        # ('signature',List([big_endian_int,big_endian_int,big_endian_int]))
        ('v',big_endian_int),
        ('r',big_endian_int),
        ('s',big_endian_int)
    ]

to = int(input("Enter the recipient's address (e.g., 0x7Ce3049dEAD53dEE4cDBdC4c360b789a9E07A895): "),16)
gasPrice = int(eval(input("Enter the gas price (e.g., 13 * 10**9): ")))
gasLimit = int(eval(input("Enter the gas limit (e.g., 21000): ")))
nonce = int(input("Enter the transaction nonce (e.g., 39): "))
value = int(eval(input("Enter the transaction value in wei (e.g., 1 * 10**6): ")))
data = int(input("Enter the transaction data in hex (e.g., 0): "),16)
chainId = int(input("Enter the chain ID (e.g., 11155111 for sepolia): "))





unsigned_txn = Txn(nonce,gasPrice,gasLimit,to,value,data,chainId,0,0)
rlp_encoded_unsigned_txn = rlp.encode(unsigned_txn)
print(rlp_encoded_unsigned_txn.hex())
kh = keccak.new(digest_bits=256)
hash_of_unsigned_txn = kh.update(rlp_encoded_unsigned_txn).digest()
print(hash_of_unsigned_txn.hex())
offset = 11155111*2 + 35
#GET OUT R AND S
signed_txn_hash_bytes = ecdsa_raw_sign(hash_of_unsigned_txn,private_key)
v,r,s = signed_txn_hash_bytes
# v = v -27
# v = v + 11155111*2 + 35
print(f"v:{v},r:{(r)},s:{(s)}")

offset = chainId*2 + 35 - 27
signed_txn = Txn(nonce,gasPrice,gasLimit,to,value,data,v + offset,r,s)
print(signed_txn)
signed_txn_rlp_encoded = rlp.encode(signed_txn)
print("0x"+ signed_txn_rlp_encoded.hex())

req_data = '{' \
'"jsonrpc" : "2.0" ,' \
'"method": "eth_sendRawTransaction",' \
'"params":["%s"], "id":57}'%("0x" + signed_txn_rlp_encoded.hex())
print(req_data)

api = "YOUR API KEY"
request = f"https://api.etherscan.io/v2/api?module=proxy&action=eth_sendRawTransaction&hex={'0x' + signed_txn_rlp_encoded.hex()}&apikey={api}&chainid={chainId}"

print((request))
img = qrcode.make(request)

img.show()
