import os
from queue import Empty

from db.db_connect import *
from db.db_funcs import *
from db.server import *
from items_classes.vinted_items_classes import *
from utils.colors import *
from utils.funcs.get_info import *
from utils.funcs.manage_photos import *
from vinted_seller import Vinted_seller


class Program:
    def __init__(self):
        self.running = True
        self.categories = None
        self.colors = None
        self.db = None
        self.v_seller = Vinted_seller()
        self.last_id = None

    def set_db(self):
        self.db = connect()

    def set_last_id(self):
        last_id = select_last_id(self.db)

        if len(last_id) < 1:
            self.last_id = "0000"
        else:
            self.last_id = last_id[0]

    def set_categories(self):
        cursor = self.db.cursor()

        try:
            cursor.execute(queries["select_cats"])
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
            self.running = False
        else:
            self.categories = dict(result)

    def set_colors(self):
        self.colors = colors

    def quit(self):
        stop_server()
        self.running = False
        print("App stopped")

    def show_details(self, photo, dir=""):
        photo =  remove_jpg(photo)
        id = photo[-4:]
        item = select_where(self.db, id)

        if len(item) == 0:

            if is_in_directory(dir[0], photo):
                dir = dir[0]
            else:
                dir = dir[1]

            print(f"""
Product id: {id}
    photo: {photo}
    !! Product is not in DB
        """)
            
            try:
                int(id)
            except:
                print(f"""
    !! Photo needs its id            
                """)

            try:
                show_img(dir, photo)
            except:
                print("No photo in directory")
            else:
                print()
                input("Press Enter to continue...") 
                close_img()

        else:
            dir = get_dir(item[8], item[4])

            print(f"""
Product id {id}:
    category: {item[8]}
    photo: {item[2]}
    colors: {self.colors[item[5]]}, {self.colors[item[6]]}
    stock: {item[4]}
    price: {item[3]} zł
            """)

            try:
                show_img(dir, item[2])
            except:
                print("No photo in directory")
            else:
                print()
                input("Press Enter to continue...") 
                close_img()


    def check_details(self):
        running = True
        curr_cat = None

        while running:
            try:
                if curr_cat == None:
                    curr_cat = get_category(self.categories)

                    print()
                    print("In stock items in category:")
                    in_stock_dir = get_dir(curr_cat['name'], 1)
                    show_imgs_names(in_stock_dir)
                    print()
                    print("Out of stock items in category:")
                    out_stock_dir = get_dir(curr_cat['name'], 0)
                    show_imgs_names(out_stock_dir)
                    print()

            except:
                pass

            else:
                try:
                    photo = get_old_photo_id()
                except:
                    print("error occured")
                else:
                    try:
                        self.show_details(photo, [in_stock_dir, out_stock_dir])
                    except Exception as e:
                        print(f"Couldn't find {photo}")
                        print(e)
                    finally:
                        if input("Check another one? y/n ").lower() == "n":
                            running = False
                        else:
                            if input("Same category? y/n ").lower() == "n":
                                curr_cat = None
                                print()
   
                    
    def create_new_category(self):
        
        try:
            cat = get_new_category()
        except Exception as e:
            print(e)
        else:
            create_dir(cat)
            insert_cat(self.db, cat)
            self.set_categories()


    def change_one_name(self):
        running = True
        curr_cat = None

        while running:
            try:
                if curr_cat == None:
                    curr_cat = get_category(self.categories)

                    print()
                    print("In stock items in category:")
                    in_stock_dir = get_dir(curr_cat['name'], 1)
                    show_imgs_names(in_stock_dir)
                    print()
                    print("Out of stock items in category:")
                    out_stock_dir = get_dir(curr_cat['name'], 0)
                    show_imgs_names(out_stock_dir)
                    print()

                old = remove_jpg(get_old_photo_id())

                id = ""

                try:
                    int(old)
                except:
                    photo = old
                    id = get_or_create_photo_id(photo, self.last_id)
                else:
                    item = select_where(self.db, old)
                    photo = item[2]
                
                if is_in_directory(in_stock_dir, photo):
                    dir = in_stock_dir
                else:
                    dir = out_stock_dir

                try:
                    show_img(dir, photo)
                except:
                    print(f"Couldn't find a photo with id {old} in directory")
                else:
                    show_colors()
                    print()
                    new = get_new_photo_name()

                    if new[-4:] != id:
                        new_id = get_or_create_photo_id(new, self.last_id)
                        if new_id == id:
                            new = new + new_id
                            self.last_id = id
                        else:
                            if new_id > self.last_id:
                                self.last_id = new_id

                    close_img()

            except Exception as e:
                print(e)

            else:
                if is_in_directory(dir, old):
                    change_photo_name(photo, remove_jpg(new), dir)
                    update_photo(self.db, old, remove_jpg(new))
                else:
                    print(f"Couldn't find: {photo} in {curr_cat['name']} dir")

                print()

            finally:
                if input("Change another name? y/n ").lower() == "n":
                    running = False
                else:
                    if input("Same category? y/n ").lower() == "n":
                        curr_cat = None
                        print()



    def change_all_names(self):
        try:
            cat = get_category(self.categories)
            dirs = [get_dir(cat['name'], 1), get_dir(cat['name'], 0)]
        except:
            pass

        else:
            for dir in dirs:
                print(f"Directory: {dir}")
                for img in os.listdir(dir):
                    info = get_photo_info(img)
                    img = remove_jpg(img)
                    id = get_or_create_photo_id(info['id'], self.last_id)

                    show_img(dir, img)

                    try:
                        print()
                        show_colors()
                        print(f"Old name: {img}")
                        print()
                        new = get_new_photo_name()

                        if new[-4:] != id:
                            new = new + id
                            self.last_id = id
                        else:
                            if int(id) > int(self.last_id):
                                self.last_id = id

                    except Exception as e:
                        print(e)

                    else:
                        change_photo_name(img, new, dir)
                        update_photo(self.db, id, new)

                        print()

                    close_img()


    def insert_one_to_db(self):
        try:
            cat = get_category(self.categories)
            dirs = [get_dir(cat['name'], 0), get_dir(cat['name'], 1)]
            print()
            print("In stock photos from category: ")
            show_imgs_names(dirs[1])
            print("Out of stock photos from category: ")
            show_imgs_names(dirs[0])
            print()
            photo = remove_jpg(get_photo_name())

        except:
            pass

        else:
            dir = ""

            if is_in_directory(dirs[1], photo):
                dir = dirs[1]
            elif is_in_directory(dirs[0], photo):
                dir = dirs[0]
            else:
                print(f"There is no photo named {photo}.jpg in this category")

            if dir != "":
                show_img(dir, photo)
                photo = remove_jpg(photo)

                try:
                    price = get_price()

                    if dir == dirs[1]:
                        stock = get_stock()
                    else:
                        stock = 0

                    id = get_photo_info(photo)['id']

                    try:
                        int(id)
                    except:
                        raise Exception("!!This product does not have an id!!")

                    close_img()

                except Exception as e:
                    pass
                else:
                    insert_one(self.db, id, cat['num'], remove_jpg(photo), price, stock)


    def insert_all_to_db(self):
        try:
            cat = get_category(self.categories)
            dirs = [get_dir(cat['name'], 1), get_dir(cat['name'], 0)]

        except:
            pass

        else:
            for dir in dirs:
                print(f"Directory: {dir}")
                for img in os.listdir(dir):
                    show_img(dir, img)

                    try:
                        stock = get_stock()
                        price = get_price()
                        id = get_photo_info(img)['id']

                        try:
                            int(id)
                        except:
                            raise Exception("!!This product does not have an id!!")

                    except:
                        pass
                    else:
                        insert_one(self.db, id, cat['num'], remove_jpg(img), price, stock)
                        print()

                    close_img()

    def check_stock(self):
        try:
            id = get_id()
        except:
            pass

        else:
            stock = select_where(self.db, id)

            print()
            print(f"Stock for: {stock[2]} = {stock[4]} p.")

    def decrease_stock(self, ids=None, diff=1):
        try:
            if ids == None:
                ids = get_many_ids()
                diff = get_stock_diff()
                print()
        except:
            pass
        else:
            for id in ids:
                stock = select_where(self.db, id)[4]
                is_sold = check_if_sold(self.db, id)

                if not is_sold:
                    if stock-diff >= 0:
                        print(f"Processing stock decrease for id {id}")

                        update_stock(self.db, id, diff, "d")
                        is_sold = check_if_sold(self.db, id)

                        if is_sold:
                            item = select_where(self.db, id)
                            print()
                            photo = item[2]
                            cat = item[8]
                            move_to(photo, cat, "sold")
                            print()

                    else:
                        print(f"Can't decrease stock by {diff} for id {id}")


    def increase_stock(self, ids=None, diff=1):
        try:
            if ids == None:
                ids = get_many_ids()
                diff = get_stock_diff()

        except:
            pass

        else:
            for id in ids:
                was_sold = check_if_sold(self.db, id)
                print(f"Processing stock increase for id {id}")

                update_stock(self.db, id, diff, "i")
                is_sold = check_if_sold(self.db, id)

                if not is_sold and was_sold:
                    item = select_where(self.db, id)
                    photo = item[2]
                    cat = item[8]
                    print()
                    move_to(photo, cat, "sell")


    def check_price(self):
        try:
            id = get_id()

        except:
            pass

        else:
            current_price = select_where(self.db, id)[3]
            print(f"Current price of id: {id} = {current_price}zł")


    def change_price(self):
        try:
            id = get_id()
        except:
            pass
        else:
            current_price = select_where(self.db, id)[3]
            print(f"Current price of id: {id} = {current_price}zł")

            try:
                new_price = get_price()
            except:
                pass
            else:
                update_price(self.db, id, new_price)


    def upload_specific_items(self, ids=None):
        try:
            if ids == None:
                ids = get_many_ids()
        except: 
            pass
        else:
            for id in ids:
                if check_if_sold(self.db, id):
                    ids.remove(id)

            if len(ids) > 0:
                self.v_seller.run(ids)
                print("Uploading finished \n")


    def get_one_time_item(self):
        photo = get_photo_name()
        show_img("C:/bussin/imgs/one_times", add_jpg(photo))
        desc = get_description()
        cat = get_category_from_vinted()
        brand = get_brand()
        size = get_size()
        condition = get_condition()
        price = get_price()

        show_colors()
        colors = get_colors()

        return OneTimeSell(photo, price, 0, desc, colors, cat, brand, condition, size)


    def upload_one_time_item(self, item):
        self.v_seller.run(0, item)
        print("Uploading finished \n")

    
    def upload_category_items(self):
        try:
            cat = get_category(self.categories)
        except:
            pass
        else:
            ids = []

            items = select_where_cat(self.db, cat['num'])

            for item in items:
                if item[4] > 0:
                    ids.append(str(item[0]))

            if len(ids) > 0:
                print()
                self.v_seller.run(ids)
                print("Uploading finished \n")


    def sell_items(self):
        try:
            ids = get_many_ids()
        except:
            pass
        else:
            self.decrease_stock(ids)
            self.upload_specific_items(ids)


    def sell_items_out_of_db(self):
        items = []
        running = True

        while running:
            try:
                item = self.get_one_time_item()
                items.append(item)
            except:
                print("Something went wrong try again")
            finally:
                run = input(f"Continue? Y/N")

                if run == "Y" or run == "y":
                    running = True
                else:
                    running = False

        for item in items:
            self.upload_one_time_item(item)



    def get_task_num(self):
        print(f"""Hey! What do you want to do?

    0 for "Quit"

    ------ Manage photos or directories?
    1 for "Check details of item"
    2 for "Create a new category"
    3 for "Change one photo name"
    4 for "Change multiple photos names"

    ------ Items not in db?
    5 for "Insert one specific product to db"
    6 for "Insert all products from specific category to db"

    ------ Stock changed?
    7 for "Check stock for specific product"
    8 for "Decrease stock by..."
    9 for "Increase stock by..."

    ------ Details changed?
    10 for "Check price of specific product"
    11 for "Change price"

    ------ Items to sell?
    12 for "Upload specific items to Vinted"
    13 for "Upload all items from one category to Vinted"
    14 for "Upload one-time-sell items to Vinted"

    ------ Items sold?
    15 for "Sell items"

    """)

        task = input("Waiting for number... ")
        
        try:
            task = int(task)
        except:
            task = 1000000000000000000

        print()
        return task


    def run_task(self, task):
        if task == 0:
            self.quit()
        elif task == 1:
            self.check_details()
        elif task == 2:
            self.create_new_category()
        elif task == 3:
            self.change_one_name()
        elif task == 4:
            self.change_all_names()
        elif task == 5:
            self.insert_one_to_db()
        elif task == 6:
            self.insert_all_to_db()
        elif task == 7:
            self.check_stock()
        elif task == 8:
            self.decrease_stock()
        elif task == 9:
            self.increase_stock()
        elif task == 10:
            self.check_price()
        elif task == 11:
            self.change_price()
        elif task == 12:
            self.upload_specific_items()
        elif task == 13:
            self.upload_category_items()
        elif task == 14:
            self.sell_items_out_of_db()
        elif task == 15:
            self.sell_items()
        else:
            pass
        

    def run(self):
        start_server()
        self.set_db()
        self.set_last_id()
        print(self.last_id)
        self.set_categories()
        self.set_colors()

        while self.running:
            print()

            task = self.get_task_num()
            self.run_task(task)

            print()
            input("Press Enter to continue...") 
    
    