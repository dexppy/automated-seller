import shutil
import os

def add_jpg(photo):
    if photo[-4:] != ".jpg":
        photo = photo + ".jpg"

    return photo

def remove_jpg(photo):
    if photo[-4:] == ".jpg":
        photo = photo[:-4]

    return photo


def move_to(photo, cat, dir):
    photo = add_jpg(photo)

    try:
        if dir == "sold":
            shutil.move(f"C:/bussin/imgs/in_stock/{cat}/{photo}", f"C:/bussin/imgs/out_of_stock/{cat}/{photo}")
            info = f"Photo: {photo} was moved to out_of_stock dir" 
        elif dir == "sell":
            shutil.move(f"C:/bussin/imgs/out_of_stock/{cat}/{photo}", f"C:/bussin/imgs/in_stock/{cat}/{photo}")
            info = f"Photo: {photo} was moved to in_stock dir"
    except Exception as e:
        print(f"Couldn't move {photo} to out_of_stock dir")
        print(e)
    else:
        print(info)


def create_dir(cat):
    path1 = os.path.join(f"C:/bussin/imgs/in_stock/", cat)
    path2 = os.path.join(f"C:/bussin/imgs/out_of_stock/", cat)

    try:
        os.mkdir(path1)
        os.mkdir(path2)
    except Exception as e:
        print(f"Couldn't create dirs for {cat} category: {e}")
    else:
        print(f"Dirs for {cat} category were created")


def change_photo_name(old, new, dir):
    old = add_jpg(old)
    new = add_jpg(new)

    old_path = os.path.join(dir + "/", old)
    new_path = os.path.join(dir + "/", new)

    if new != "":
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"Couldn't change {old} to {new}")
            print(e)
        else:
            print(f"Successfully changed name from {old} to {new}")
    else:
        print("Skipped")


    

