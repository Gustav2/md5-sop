import hashlib
import sqlite3


def connect_db():
    # Forbinder til databasen og laver den hvis den ikke findes
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Lav "credentials" tabellen hvis den ikke eksisterer
    t = 'CREATE TABLE IF NOT EXISTS credentials (username VARCHAR (32), password VARCHAR (32), userID INTEGER PRIMARY KEY AUTOINCREMENT)'
    c.execute(t)
    conn.commit()


if __name__ == "__main__":
    connect_db()