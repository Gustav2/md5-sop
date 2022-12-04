import hashlib
import sqlite3
import string
import random

try:  # Prøver at oprette forbindelse til databasen og laver to tabeller
    # Forbinder til databasen og laver den hvis den ikke findes
    conn = sqlite3.connect('database.db')
    # Laver en cursor, som er en måde at hente og skrive til databasen
    c = conn.cursor()
    print("Created and connected to database")

    # laver en tabel med brugernavn, password og salt hvis den ikke findes. Skrevet i SQL.
    t = 'CREATE TABLE IF NOT EXISTS saltedCredentials (username VARCHAR (32), password VARCHAR (32), salt VARCHAR (32), userID INTEGER PRIMARY KEY ' \
        'AUTOINCREMENT) '

    # Kører SQL kommandoen beskreven i t
    c.execute(t)

    # Opdaterer databasen med den nye SQL kommando
    conn.commit()
    print("Created table with salted credentials")

    # laver en tabel med brugernavn og password hvis den ikke findes
    t = 'CREATE TABLE IF NOT EXISTS credentials (username VARCHAR (32), password VARCHAR (32), userID INTEGER PRIMARY KEY AUTOINCREMENT)'

    # Kører SQL kommandoen beskreven i t
    c.execute(t)

    # Opdaterer databasen med den nye SQL kommando
    conn.commit()
    print("Created table with credentials")

except Exception as e:  # Hvis der er en fejl, så printes den
    print(e)


def create_user_salted(username, password, salt):
    # Lægger saltet til passwordet og laver det om til bytes så det kan hashes
    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()

    # Laver en SQL kommando der henter alle brugernavnet brugeren har indsat
    c.execute("SELECT * FROM saltedCredentials WHERE username = ?", (username,))
    if c.fetchone() is None:  # Hvis der ikke er nogen brugere med det brugernavn
        # Laver en SQL kommando der indsætter brugernavn, password og salt i databasen
        c.execute("INSERT INTO saltedCredentials(username,password,salt) VALUES (?,?,?)", (username, hashed_password, salt))
        conn.commit()
        print(f"User {username} created, with salt")
    else:  # Printer at der allerede er en bruger med det brugernavn, hvis der er
        print("User already exists")


def create_user(username, password):
    # Hasher passwordet
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # Laver en SQL kommando der henter alle brugernavnet brugeren har indsat
    c.execute("SELECT * FROM credentials WHERE username = ?", (username,))
    if c.fetchone() is None:  # Hvis der ikke er nogen brugere med det brugernavn
        # Laver en SQL kommando der indsætter brugernavn og password i databasen
        c.execute("INSERT INTO credentials(username,password) VALUES (?,?)", (username, hashed_password))
        conn.commit()
        print(f"User {username} created")

    else:  # Printer at der allerede er en bruger med det brugernavn, hvis der er
        print("User already exists")


def authenticate_user(username, password):
    try:  # Prøver at hente passwordet fra databasen med en SQL kommando
        c.execute("SELECT password FROM credentials WHERE username = ?", (username,))
        fetched_password = c.fetchone()[0]  # siden der kun er et resultat, så hentes det første element i tuplen

    except TypeError:  # Skriver at brugeren ikke findes hvis der ikke er nogen brugere med det brugernavn
        print("Could not fetch password - user does not exist")
        return  # Stopper funktionen

    # Initialiserer en variable med det hashede password.
    # Passwordet fra brugeren, bliver lavet om til bytes via .encode() metoden
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # Tjekker om passwordet er det samme som det gemte og printer resultatet
    if hashed_password == fetched_password:
        print("User authenticated")
    else:
        print("User not authenticated")

    input("Press enter to exit")  # Stopper eksekveringen af programmet indtil brugeren trykker på en tast


def authenticate_user_salted(username, password):
    try:  # Prøver at hente passwordet og saltet fra databasen med en SQL kommando
        c.execute("SELECT salt FROM saltedCredentials WHERE username = ?", (username,))
        salt = c.fetchone()[0]  # siden der kun er et resultat, så hentes det første element i tuplen

        # Henter det hashede password fra databasen
        c.execute("SELECT password FROM saltedCredentials WHERE username = ?", (username,))
        fetched_password = c.fetchone()[0]

    except TypeError:  # Skriver at brugeren ikke findes hvis der ikke er nogen brugere med det brugernavn
        print("Could not fetch salt or password - user does not exist")
        return  # Stopper funktionen

    # Initialiserer en variable med det hashede password.
    # Passwordet fra brugeren sammen med hashed fra databasen, bliver lavet om til bytes via .encode() metoden
    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()

    # Tjekker om passwordet er det samme som det gemte og printer resultatet
    if hashed_password == fetched_password:
        print("User authenticated")

    else:
        print("User not authenticated")

    input("Press enter to exit")  # Stopper eksekveringen af programmet indtil brugeren trykker på en tast


def fetch_user_creds():  # Funktion der henter brugernavn og password fra brugeren
    username = input("Username: ")
    password = input("Password: ")

    return username, password


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
        username, password = fetch_user_creds()  # Henter brugernavn og password fra brugeren
        create_user(username, password)
    elif choice == "2":
        username, password = fetch_user_creds()

        # Genererer et tilfældigt salt
        letters = string.ascii_letters  # Laver en string med alle bogstaver i alfabetet
        salt = "".join(random.choice(letters) for _ in range(16))  # Laver en string med 16 tilfældige bogstaver fra "letters"

        create_user_salted(username, password, salt)

    elif choice == "3":
        username, password = fetch_user_creds()
        authenticate_user(username, password)

    elif choice == "4":
        username, password = fetch_user_creds()
        authenticate_user_salted(username, password)

    else:
        exit()


if __name__ == "__main__":
    while True:
        main()
