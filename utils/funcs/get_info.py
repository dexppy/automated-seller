import os
from os import listdir
from utils.funcs.get_imgs import *
from utils.funcs.manage_photos import *

def get_category(cats):
    print("Categories: ")
    for cat in cats:
        print(f"{cat}. {cats[cat]}")

    print() 
    category = int(input("Select category: "))

    return { 'num': category, 'name': cats[category] }

def get_old_photo_id():
    old = input("Product photo id or name (if not in db yet): ")

    if old == "":
        raise Exception("Photo id cannot be blank; Skipped")
    else:
        return old

def get_new_photo_name():
    new = input("New product photo name: ")

    if new == "":
        raise Exception("Photo name cannot be blank; Skipped")
    else:
        return new

def get_photo_name():
    photo = input("Product photo name: ")

    if photo == "":
        raise Exception("Photo name cannot be blank, Skipped")
    else:
        return photo


def get_dir(cat, stock):

    if stock > 0:
        dir = "C:/bussin/imgs/in_stock/" + cat
    else:
        dir = "C:/bussin/imgs/out_of_stock/" + cat

    return dir

def get_stock():
    return int(input("Stock: "))

def get_price():
    price = input("Price: ")
    price = round(float(price), 2)

    return price

def get_id():
    return input("Product id: ")

def get_photo_info(photo):
    photo = remove_jpg(photo)
    id = photo[-4:]
    name = photo[:-4]

    return {'id': id, 'name': name}

def is_in_directory(dir, photo):
    for img in os.listdir(dir):
        if img == add_jpg(photo):
            return True

    return False

def get_stock_diff():
    return int(input("How many items? "))

def get_new_category():
    cat = input("New category name: ")

    if cat == "":
        raise Exception("Category name cannot be blank, Skipped")
    else:
        return cat


def get_many_ids():
    ids = input("Type down all ids followed by a comma: \n")
    id_arr = ids.replace(" ", "").split(",")
    print()

    return id_arr


def create_new_id(last_id):
    
    try:    
        last_id = int(last_id)

        new_id = str(last_id+1)
        leng = 4 - len(new_id)

        new_id = leng*"0" + new_id

    except Exception as e:
        print(e)
    else:
        return new_id


def get_or_create_photo_id(photo, last_id):
    photo = remove_jpg(photo)
    id = photo[-4:]

    try:
        int(id)
        return id
    except:
        id = create_new_id(last_id)
        return id


def get_category_from_vinted():
    cat = input("Type down category listed and separated by /: ")

    return cat


def get_title():
    product_title = input("Product title: ")

    return product_title


def get_description():
    product_desc = input("Product description: ")

    return product_desc


def get_brand():
    product_brand = input("Product brand: ")

    return product_brand

def get_condition():
    print("""Number for condition:
 6-Nowy z metką
 1-Nowy bez metki
 2-Bardzo dobry
 3-Dobry
 4-Zadowalający   
    """)
    product_brand = input("Select from above: ")

    return product_brand

def get_colors():
    colors = input("Type down colors separated by /: ")
    colors = colors.split("/")

    return colors

def get_size():
    print("""Number for size:
    2-XS
    3-S
    4-M
    5-L
    6-XL 
       """)
    size = input("Select from above: ")

    return size

