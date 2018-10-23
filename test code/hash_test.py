from passlib.hash import sha256_crypt
pass1 = sha256_crypt.encrypt("password1")

pass2 = sha256_crypt.encrypt("password2")
print(pass1)
print(pass2)

print(sha256_crypt.verify("password1"+ salt, pass2))


"""

import hashlib

user_password = "cookies"

salt = "chocolate"

new_password = user_password + salt

hashpass = hashlib.md5(new_password.encode())


print(hashpass.hexdigest())


"""