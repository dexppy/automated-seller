
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from items_classes.vinted_items_classes import *
from db.db_connect import *
from db.db_queries import *
from db.db_funcs import *
from dotenv import load_dotenv
from utils.funcs.manage_photos import remove_jpg

load_dotenv()

class Vinted_seller:
    def __init__(self):
        self.page = None
        self.login = [os.getenv("LOGIN"), os.getenv("PASSWORD")]
        self.item = None
        self.colors = None
        self.prof_items = None  


    def set_item(self, id, item=None):
        db = connect()

        if item is None:
            item = select_where(db, id)
            self.colors = select_colors(db, item[5], item[6])

            if item[1] == 1:
                self.item = Earrings(item[0], item[2], item[3], item[4], item[9], [self.colors[0][1], self.colors[1][1]])
            elif item[1] == 2:
                self.item = Necklaces(item[0], item[2], item[3], item[4], item[9], [self.colors[0][1], self.colors[1][1]])
            elif item[1] == 3:
                self.item = Bracelets(item[0], item[2], item[3], item[4], item[9], [self.colors[0][1], self.colors[1][1]])
            elif item[1] == 4:
                self.item = Necklaces(item[0], item[2], item[3], item[4], item[9], [self.colors[0][1], self.colors[1][1]])
        else:
            self.item = item


    def load_main_page(self):
        self.page.goto("https://www.vinted.pl/")
        self.page.wait_for_timeout(3000)

        if self.page.locator("button#onetrust-accept-btn-handler").count() > 0:
            self.page.dblclick("button#onetrust-accept-btn-handler")
            self.page.wait_for_timeout(2000)


    def load_selling_page(self):
        self.page.locator("span.c-button__label:has-text('Sprzedaj')").click()
        self.page.wait_for_timeout(5000)

        if self.page.title() == "Sprzedaj ubranie - Vinted":
            print("Filling sell item form...")



    def fill_login_form(self):
        self.fill_text_input("#username", self.login[0])
        self.fill_text_input("#password", self.login[1])
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(5000)

    
    def log_in(self):
        if self.page.locator("div.user-actions").count() < 1:
            self.page.goto('https://www.vinted.pl/member/general/login')
            self.fill_login_form()
            if self.page.locator("div.user-actions"):
                print("Logged in...")
            elif self.page.locator("span:has-text('Nieprawidłowy login lub hasło')"):
                print("Password incorrect")
            else:
                print("Logging error")
        else:
            print("Logged in...")

    
    def count_prof_items(self):
        self.load_main_page()
        self.page.click("#user-menu-button")
        self.page.click("a:has-text('Mój profil')")
        self.page.wait_for_timeout(5000)

        grid = self.page.locator("div.feed-grid")
        count = grid.locator("div.feed-grid__item-content").count()
        return count


    def check_stock(self):

        if self.item.stock > 0:
            return True

        return False


    def current_item(self):
        print(f"""
Selling:

id: {self.item.id}
title: {self.item.title}

description: {self.item.desc}

colors: {self.colors[0][1]}, {self.colors[1][1]}
price: {self.item.price} zl
                """)


    def fill_file_input(self, xpath, file_path):
        with self.page.expect_file_chooser() as fc_info:
            self.page.click(xpath)
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)


    def fill_text_input(self, xpath, value):
        self.page.locator(xpath).type(str(value))


    def fill_category_input(self):
        categories = self.item.cat.split("/")
        self.page.click("#catalog_id")

        for cat in categories:
            self.page.locator('div.Cell_title__--i7D').locator(f'text=/^{cat}$/i').click()

    def fill_one_time_checkbox(self):
        self.page.click("#size_id")
        size = "#size-"+self.item.size
        print(size)

        self.page.click(size)

        self.page.click("#status_id")
        status = "#status-" + self.item.cond
        print(status)

        self.page.click(status)
        self.page.click("#package-size-1")


    def fill_checkbox(self):
        self.page.click("#brand_id")
        self.page.click("#brand-573")

        self.page.click("#status_id")
        self.page.click("#status-6")

        if self.page.locator("#size_id").count() > 0:
            self.page.click("#size_id")
            self.page.click("#size-1224")


        if self.page.locator("#unisex").count() > 0:
            self.page.click("span:has-text('Unisex')")


        self.page.click("#package-size-1")

    
    def fill_colors_input(self):
        self.page.click("#color")

        color1_button = "#color-" + str(self.colors[0][2])
        self.page.click(color1_button)

        if str(self.colors[1][2]) != "0":
            color2_button = "#color-" + str(self.colors[1][2])
            self.page.click(color2_button)
        
        self.page.mouse.click(0, 0)


    def upload_item(self):
        self.page.locator('data-testid=upload-form-save-button').click()
        self.page.wait_for_timeout(5000)


    def sell_item(self, id):
        self.set_item(id)

        if self.check_stock():
            self.current_item()
            self.load_selling_page()
            photo = f"{self.item.path}/{remove_jpg(self.item.photo)}.jpg"
            self.fill_file_input("//html[1]/body[1]/main[1]/div[1]/section[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/button[1]", photo)
            
            self.fill_text_input("#title", self.item.title)
            self.fill_text_input("#description", self.item.desc)

            self.fill_category_input()
            
            self.fill_checkbox()
            self.fill_colors_input()
            self.fill_text_input("#price", self.item.price)

            self.upload_item()
        else:
            print(f"Item with id {id} is out of stock")


    def sell_one_time_item(self, item):
        self.set_item(item)
        self.current_item()
        self.load_selling_page()
        photo = f"{self.item.path}/{remove_jpg(self.item.photo)}.jpg"
        self.fill_file_input("//html[1]/body[1]/main[1]/div[1]/section[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/button[1]",photo)

        self.fill_text_input("#title", self.item.title)
        self.fill_text_input("#description", self.item.desc)

        self.fill_category_input()

        self.fill_one_time_checkbox()
        self.fill_colors_input()
        self.fill_text_input("#price", self.item.price)

        self.upload_item()


    def check_if_uploaded(self):
        count = self.count_prof_items()

        if count > self.prof_items:
            return True
        else:
            return False

    
    def run(self, ids=0, items=0):
        with sync_playwright() as p:
            browser = p.firefox.launch()
            self.page = browser.new_page()
            stealth_sync(self.page)
            print("Wait...")
            print()
            self.load_main_page()
            self.log_in()
            self.prof_items = self.count_prof_items()

            if ids != 0 and items == 0:
                for id in ids:
                    self.sell_item(id)

                    if self.check_if_uploaded():
                        self.prof_items+=1
                        print(f"Successfully uploaded id: {id}")

                    else:
                        print(f"Error occured while uploading id: {id}")

            elif ids == 0 and items != 0:
                for item in items:
                    self.sell_one_time_item()

                    if self.check_if_uploaded():
                        self.prof_items += 1
                        print(f"Successfully uploaded item: {item.title}")

                    else:
                        print(f"Error occured while uploading item: {item.title}")


