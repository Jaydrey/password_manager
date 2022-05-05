import psycopg2
from decouple import config
import sys

def dbconfig():
    try:
        database = psycopg2.connect(
            host=config("DATABASE_HOST", cast=str),
            database=config("DATABASE_NAME", cast=str),
            user=config("DATABASE_USER", cast=str),
            password=config("DATABASE_PASSWORD", cast=str),
            port=config("DATABASE_PORT", cast=int)
        )
    except psycopg2.Error as e:
        print(e)
        sys.exit(0)
    
    return database