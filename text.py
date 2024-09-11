import bcrypt
print(bcrypt.hashpw('Qahram0n'.encode(), bcrypt.gensalt()))