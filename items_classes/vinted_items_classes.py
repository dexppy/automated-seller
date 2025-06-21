from utils.colors import *
from items_classes.item_class import Item

class OneTimeSell(Item):
    def __init__(self, photo, price, stock, desc, colors, cat, brand, cond, size):
        super().__init__(photo, price, stock, desc, colors, cat, brand, cond, size)
        self.cat = cat
        self.brand = brand
        self.cond = cond
        self.size = size
        self.path = "C:/bussin/imgs/one_times/"

class ItemVinted(Item):
    def __init__(self, id, photo, price, stock, desc, colors):
        super().__init__(id, photo, price, stock, desc, colors)
        self.cat = "Kobiety/Akcesoria/"
        self.brand = "Bez marki"
        self.cond = "Nowy z metką"

    def show_item(self):
        rest = f"""category: {self.cat}
            brand: {self.brand}
            condition: {self.cond}
            photo: { self.path }/{ self.photo }.jpg
        """
        Item.show_item(self, rest)


class Earrings(ItemVinted):
    def __init__(self, id, photo, price, stock, desc, colors):
        path = "/earrings"
        cat = "Biżuteria/Kolczyki"

        super().__init__(id, photo, price, stock, desc, colors)
        self.path = self.path + path
        self.cat = self.cat + cat


class Necklaces(ItemVinted):
    def __init__(self, id, photo, price, stock, desc, colors):
        path = "/necklaces"
        cat = "Biżuteria/Korale, wisiorki, naszyjniki"

        super().__init__(id, photo, price, stock, desc, colors)
        self.path = self.path + path
        self.cat = self.cat + cat


class Bracelets(ItemVinted):
    def __init__(self, id, photo, price, stock, desc, colors):
        path = "/bracelets"
        cat = "Biżuteria/Bransoletki"

        super().__init__(id, photo, price, stock, desc, colors)
        self.path = self.path + path
        self.cat = self.cat + cat


class Rings(ItemVinted):
    def __init__(self, id, photo, price, stock, desc, colors):
        path = "/rings"
        cat = "Biżuteria/Pierścionki"

        super().__init__(id, photo, price, stock, desc, colors)
        self.path = self.path + path
        self.cat = self.cat + cat
