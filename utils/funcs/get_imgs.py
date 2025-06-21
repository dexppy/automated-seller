import os
from os import walk
from PIL import Image
from utils.funcs.manage_photos import *

def show_img(dir, photo):
    photo = add_jpg(photo)
    image_dir = Image.open(dir + "/" + photo)
    image_dir.show()

def close_img():
    os.system('TASKKILL /F /IM  Microsoft.Photos.exe')

def show_imgs_names(dir):
    names = []
    for (dirpath, dirnames, filenames) in walk(dir):
        names.extend(filenames)
        break

    for name in names:
        print(f" - {name}")
