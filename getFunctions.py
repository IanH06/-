import sqlite3

users_db = "users.db"
userdb_connect = sqlite3.connect(users_db)

def getNotes(DID):
    sql = f"""SELECT * FROM notes WHERE DID = '{DID}'"""
    c = userdb_connect.execute(sql)
    return [x for x in c]

def getNextUID():
    sql = """ SELECT * FROM users"""
    c = userdb_connect.execute(sql)
    l = [x[0] for x in c]
    if l:
        latest = l[-1]
        latest  = str(int(latest.lstrip("0")) +1)
        while len(latest) < 4:
            latest = "0" + latest
        return(latest)
    else:
        return "0001"

def getdName(DID):
    sql = f"""SELECT deckName FROM decks WHERE DID = '{DID}'"""
    return [x for x in (userdb_connect.execute(sql))][0][0]

def getDeckInfo(DID):
    sql = f"""SELECT * FROM decks WHERE DID = '{DID}'"""
    return [x for x in (userdb_connect.execute(sql))][0]

def getLatestDID():
    sql = f"""SELECT DID FROM decks"""
    return [x for x in (userdb_connect.execute(sql))][-1][0]