from utils import dbconfig
import clipboard
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
# from Crypto.Random import get_random_bytes
from utils import aes256

COUNT = 1_000_000
DKLEN = 32

def generate_master(master_password:str, device_secret:str)->bytes:
    ms = master_password.encode()
    ds = device_secret.encode()
    master_key = PBKDF2(ms, ds, DKLEN, count=COUNT, hmac_hash_module=SHA512)
    return master_key

def save_entries(sitename:str, siteurl:str, username:str, email:str, master_password:str, device_password:str):
    conn = dbconfig()
    cursor = conn.cursor()

    master_secret = generate_master(master_password, device_password)
    password = clipboard.paste()
    encrypted_entries = aes256.encrypt(
        key=master_secret,
        source=password,
        keyType='bytes'
    )
    
    # adding the entries
    query = "INSERT INTO entries (sitename, siteurl, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (sitename, siteurl,email, username, encrypted_entries))
    conn.commit()
    # password = getpass("Enter master key")




def main():
    save_entries()

if __name__=="__main__":
    main()
