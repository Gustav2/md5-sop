import hashlib
import sqlite3


# Forbinder til databasen og laver den hvis den ikke findes
conn = sqlite3.connect('database.db')
c = conn.cursor()
print("Created and connected to database")

# laver en tabel med brugernavn, password og salt hvis den ikke findes
t = 'CREATE TABLE IF NOT EXISTS saltedCredentials (username VARCHAR (32), password VARCHAR (32), salt VARCHAR (32), userID INTEGER PRIMARY KEY ' \
    'AUTOINCREMENT) '
c.execute(t)
conn.commit()
print("Created table with salted credentials")

# laver en tabel med brugernavn og password hvis den ikke findes
t = 'CREATE TABLE IF NOT EXISTS credentials (username VARCHAR (32), password VARCHAR (32), userID INTEGER PRIMARY KEY AUTOINCREMENT)'
c.execute(t)
conn.commit()
print("Created table with credentials")

def create_user_salted(username, password, salt="UsikkertSalt"):
    # Hasher passwordet
    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()

    c.execute("INSERT INTO credentials(username,password,salt) VALUES (?,?)", (username, hashed_password, salt))
    conn.commit()
    print(f"User {username} created, with salt")


def create_user(username, password):
    # Hasher passwordet
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    c.execute("INSERT INTO credentials(username,password) VALUES (?,?)", (username, hashed_password))
    conn.commit()
    print(f"User {username} created")


def main():
    pass


if __name__ == "__main__":
    main()
