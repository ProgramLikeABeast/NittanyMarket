from re import S
import pandas
import sqlite3 as sql

import hashlib

def encrypt(s):
    hash_obj = hashlib.sha256(bytes(s, encoding='utf-8'))
    hex_result = hash_obj.hexdigest()
    return hex_result

email,password = 'arubertelli0@nsu.edu', 'TbIF16hoUqGl'

def loginVerify(email, password):
    e_password = encrypt(password)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email=? AND password=?;", (email, e_password))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True

print(loginVerify(email, password))
