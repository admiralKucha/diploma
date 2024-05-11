import bcrypt

salt = bcrypt.gensalt(rounds=10)

password = "admin"

hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

print(hashed_password)