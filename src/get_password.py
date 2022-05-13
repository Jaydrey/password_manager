from utils import dbconfig
import hashlib
from typing import Any
from Crypto.Hash import SHA512
from Crypto.Protocol import KDF
from utils import aes256
from .save_password import generate_master

COUNT = 1_000_000
DKLEN = 32

def dbresponse_to_dict(response:list[tuple], decrypt:bool, master_key)->dict[str, dict[str, str]]:
    """
    Transforming the database response to a dictionary
    """
    dict_response = {}
    for site in response:
        site_info= {}
        site_info["sitename"] = site[0]
        site_info["siteurl"] = site[1]
        site_info["email"] = site[2]
        site_info["username"] = site[3]
        password_len = 0
        if decrypt:
            decrypted_password = decrypt_password(site[4], master_key)
            site_info["password"] = decrypted_password
            password_len = len(decrypted_password)
        else:
            site_info["password"] = password_len * "*"
        dict_response[site[0]] = site_info
    
    return dict_response

def decrypt_password(encrypted_pass:bytes, master_key:bytes)->str:
    decrypted = aes256.decrypt(master_key, encrypted_pass, keyType="bytes")
    return decrypted.decode()

async def verify_master_password(master_password:str):
    conn = dbconfig()
    cursor = conn.cursor()
    query = "SELECT masterkey_hash, salt_secret FROM secrets"
    await cursor.execute(query)
    response:tuple = await cursor.fetchall()[0]
    master_hash = hashlib.sha256(master_password.encode()).hexdigest()
    if master_hash==response[0]:
        return (True, response[1])
    else:
        return False

async def get_site_passwords(master_password:str, search_field:dict[str, str], decrypt:bool=False) -> dict[str, dict[str, str]]:
    conn = dbconfig()
    cursor = conn.cursor()

    master_is_correct = await verify_master_password(master_password)
    if isinstance(master_is_correct, bool):
        return {"response": "Invalid master password. Try again!"}
    device_secret:str = master_is_correct[1]
    master_key = generate_master(master_password, device_secret)

    query = ""
    if len(search_field)==0:
        query += "SELECT * FROM entries"
    else:
        query += "SELECT * FROM entries WHERE "        
        for key in search_field:
            query +=f"{key}='{search_field[key]}' AND "
        query = query[:-5]

    await cursor.execute(query)
    db_response = await cursor.fetchall()
    dict_response = dbresponse_to_dict(db_response, decrypt, master_key)
    if len(dict_response)>0:
        return dict_response

    conn.close()

