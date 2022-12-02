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


def create_user_salted(username, password, salt="123"):
    # Hasher passwordet
    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()

    c.execute("INSERT INTO saltedCredentials(username,password,salt) VALUES (?,?,?)", (username, hashed_password, salt))
    conn.commit()
    print(f"User {username} created, with salt")


def create_user(username, password):
    # Hasher passwordet
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    c.execute("INSERT INTO credentials(username,password) VALUES (?,?)", (username, hashed_password))
    conn.commit()
    print(f"User {username} created")


def authenticate_user(username, password):
    c.execute("SELECT password FROM credentials WHERE username = ?", (username,))
    fetched_password = c.fetchone()[0]
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    if hashed_password == fetched_password:
        print("User authenticated")
        input("Press enter to exit")
    else:
        print("User not authenticated")
        input("Press enter to exit")


def authenticate_user_salted(username, password):
    c.execute("SELECT salt FROM saltedCredentials WHERE username = ?", (username,))
    salt = c.fetchone()[0]
    c.execute("SELECT password FROM saltedCredentials WHERE username = ?", (username,))
    fetched_password = c.fetchone()[0]

    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()

    if hashed_password == fetched_password:
        print("User authenticated")
        input("Press enter to exit")
    else:
        print("User not authenticated")
        input("Press enter to exit")

    print(salt, fetched_password, hashed_password)


def main():
    print("""
    Welcome!
    Press the corresponding number to do the following:
        1. Create a user
        2. Create a user with salt
        3. Authenticate a user
        4. Authenticate a user with salt
    
    n. Exit
    """)
    choice = input("Number: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        create_user(username, password)
    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        create_user_salted(username, password, "salt")

    elif choice == "3":
        username = input("Username: ")
        password = input("Password: ")
        authenticate_user(username, password)

    elif choice == "4":
        username = input("Username: ")
        password = input("Password: ")
        authenticate_user_salted(username, password)

    else:
        exit()


if __name__ == "__main__":
    while True:
        main()
