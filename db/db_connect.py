import mysql.connector


def connect():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "bussin"
    )

    return db
