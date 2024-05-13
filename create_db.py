import os
import psycopg2
from config import host, user, password, db_name


try:

    connection = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=5433
    )


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")