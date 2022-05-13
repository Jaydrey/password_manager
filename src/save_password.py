from utils import dbconfig
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import hashlib
from utils import aes256
from generate_password import generate


def generate_master(master_password:str, device_secret:str)->str:
    COUNT = 1_000_000
    DKLEN = 32
    ms = master_password.encode()
    ds = device_secret.encode()
    master_key = PBKDF2(ms, ds, DKLEN, count=COUNT, hmac_hash_module=SHA512)
    return str(master_key)

def verify_master_password(master_password:str):
    conn = dbconfig()
    cursor = conn.cursor()
    query = "SELECT masterkey_hash, salt_secret FROM secrets"
    cursor.execute(query)
    response:tuple = cursor.fetchall()[0]
    master_hash = hashlib.sha256(master_password.encode()).hexdigest()
    if master_hash==response[0]:
        return (True, response[1])
    else:
        return False

def save_entries(sitename:str, siteurl:str, username:str, email:str, master_password:str):
    conn = dbconfig()
    cursor = conn.cursor()
    master_is_correct = verify_master_password(master_password)
    if isinstance(master_is_correct, bool):
        return {"response": "Invalid master password!\n Try again"}
    device_secret = master_is_correct[1]
    master_secret = generate_master(master_password, device_secret)
    password = generate()
    encrypted_entries = aes256.encrypt(
        key=master_secret,
        source=password,
        keyType='bytes'
    )
    
    # adding the entries
    query = "INSERT INTO entries (sitename, siteurl, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (sitename, siteurl,email, username, encrypted_entries))
    conn.commit()
    

def main()->None:
    sitename = input("sitename: ")
    siteurl = input("siteurl: ")
    username = input("username: ")
    email = input("email: ")
    master_password = input("master password: ")
    save_entries(sitename, siteurl, username, email, master_password)
    print("Success")
    return

if __name__=="__main__":
    main()
