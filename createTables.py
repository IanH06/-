import sqlite3

database = "users.db"
dbConnect = sqlite3.connect(database)

userTable  = """CREATE TABLE users (
    UID      TEXT PRIMARY KEY,
    username TEXT
);"""

deckTable = """CREATE TABLE decks (
    DID INTEGER PRIMARY KEY AUTOINCREMENT,
    UID TEXT    REFERENCES users (UID) ON DELETE CASCADE,
    deckName TEXT 
);"""

notesTable = """CREATE TABLE notes (
    DID             REFERENCES decks (DID) ON DELETE CASCADE,
    NID     INTEGER PRIMARY KEY AUTOINCREMENT,
    Title   TEXT,
    Content TEXT
);"""

dbConnect.execute(userTable)
dbConnect.execute(deckTable)
dbConnect.execute(notesTable)

dbConnect.commit()