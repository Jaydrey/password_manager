from utils import dbconfig
import hashlib
import sys
import random
import string

PASSWORD_LENGTH = 10

def connect():
    conn = dbconfig()
    cursor = conn.cursor()
    # create secrets table key for master key
    secrets_table_q = "CREATE TABLE secrets(masterkey_hash TEXT NOT NULL, salt_secret TEXT NOT NULL)"
    cursor.execute(secrets_table_q)

    # create password entries for storing our passwords
    entries_table_q = "CREATE TABLE entries(sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT NOT NULL, \
    username TEXT, password TEXT NOT NULL)"
    cursor.execute(entries_table_q)
    
    # creating a master password [function]
    while True:
        master_password = input("Create a master password atleast 8char(s):\t")
        repeat_password = input("Retype the password again:\t")
        if master_password!="" and len(master_password)>=PASSWORD_LENGTH and master_password==repeat_password:
            break
    
    # hashing our master password [function]
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    # Notification to user on hashed password success
    print("Hashed password success")

    # generate device secret
    device_secret = "".join(random.choices(string.ascii_letters + string.digits, k=PASSWORD_LENGTH))

    # inserting the hashed master password and device secret into the secrets table
    insert_query = "INSERT INTO secrets (masterkey_hash, salt_secret) VALUES (%s, %s)"
    cursor.execute(insert_query, (hashed_password, device_secret))
    conn.commit()
    # Notification to user on adding the hashed master password and device secret to tables
    print("Succesfully added the hashed master password and device secret")
    conn.close()

if __name__ == "__main__":
    connect()