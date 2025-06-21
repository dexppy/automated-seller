from select import select
from db.db_connect import *
from db.db_queries import queries

def get_affected_rows(rows):
    if rows <= 0:
        print("Nothing changed in db")
    else:
        print(f"Success, number of rows changed: {rows}")


def return_result(rows, count):
    if count <= 0:
        return []
    else:
        return rows


def insert_one(db, id, category, photo, price, stock):
    cursor = db.cursor()
    color_1 = photo[0:2]
    color_2 = photo[3:5]
    vals = (id, category, photo, price, stock, color_1, color_2)

    try:
        cursor.execute(queries["insert"], vals)
        db.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        get_affected_rows(cursor.rowcount)
        

def insert_cat(db, cat):
    cursor = db.cursor()
    vals = (cat,)

    try:
        cursor.execute(queries["insert_cat"], vals)
        db.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        get_affected_rows(cursor.rowcount)


def select_where(db, value):
    cursor = db.cursor()
    vals = (value,)

    try:
        cursor.execute(queries["select_where_id"], vals)
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print(err)
    else:
        return return_result(result, cursor.rowcount)


def select_where_many(db, value):
    cursor = db.cursor()
    vals = (value,)

    try:
        cursor.execute(queries["select_where_id"], vals)
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    else:
        return return_result(result, cursor.rowcount)


def select_where_cat(db, value):
    cursor = db.cursor()
    vals = (value,)

    try:
        cursor.execute(queries["select_where_cat"], vals)
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    else:
        return return_result(result, cursor.rowcount)


def select_all(db):
    cursor = db.cursor()

    try:
        cursor.execute(queries["select_all"])
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)
    else:
        return return_result(result, cursor.rowcount)


def select_last_id(db):
    cursor = db.cursor()

    try:
        cursor.execute(queries["select_last_id"])
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print(err)
    else:
        return return_result(result, cursor.rowcount)

def select_colors(db, color1, color2):
    cursor = db.cursor()
    vals1 = (color1,)
    vals2 = (color2,)

    try:
        cursor.execute(queries["select_colors"], vals1)
        result1 = cursor.fetchone()

        cursor.execute(queries["select_colors"], vals2)
        result2 = cursor.fetchone()
    except mysql.connector.Error as err:
        print(err)
    else:
        return [result1, result2]


def update_stock(db, id, value, change):
    cursor = db.cursor()
    vals = (value, id)

    try:
        if change == "d":
            cursor.execute(queries["update_stock_d"], vals)
        elif change == "i":
            cursor.execute(queries["update_stock_i"], vals)

        db.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        get_affected_rows(cursor.rowcount)


def update_photo(db, id, photo):
    cursor = db.cursor()
    vals = (photo, id)

    if photo != "":
        try:
            cursor.execute(queries["update_photo"], vals)
            db.commit()
        except mysql.connector.Error as err:
            print(err)
        else:
            get_affected_rows(cursor.rowcount)


def update_price(db, id, price):
    cursor = db.cursor()
    vals = (price, id)

    try:
        cursor.execute(queries["update_price"], vals)
        db.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        get_affected_rows(cursor.rowcount)


def check_if_sold(db, id):
    print()
    item = select_where(db, id)

    if item[4] == 0:
        print(f"Item: {item[2]} is out of stock \n")
        return True
    
    print(f"Item: {item[2]} is in stock = {item[4]} p.\n")
    return False

