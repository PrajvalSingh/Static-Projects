import os
from cryptography.fernet import Fernet

files = []

for entry in os.listdir():
    append_file = entry != "main.py" and os.path.isfile(entry) and entry != "password.key" and entry != "decrypt.py"

    if append_file:
        files.append(entry)


with open("password.key", "rb") as thekey:
    key = thekey.read()

if input("Enter secret phrase to decrypt: ") == "phoenix":
    for file in files:
        with open(file, "rb") as current_file:
            contents = current_file.read()

        decrypted_content = Fernet(key).decrypt(contents)

        with open(file, "wb") as file_to_encrypt:
            file_to_encrypt.write(decrypted_content)

    print("Successfully decrypted.")
else:
    print("Enter correct phrase to decrypt.")
