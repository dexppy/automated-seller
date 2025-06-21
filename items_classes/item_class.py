
class Item:
    def __init__(self, id=0, photo="", price=0, stock=0, desc="", colors=None):
        self.id = id
        self.photo = photo
        self.title = (self.photo)[6:].strip("1234567890").replace("_", " ")
        self.desc = desc
        self.price = round(float(price), 2)
        self.stock = int(stock)
        self.colors = colors

        if self.stock > 0:
            self.path = "imgs/in_stock"
        else:
            self.path = "imgs/out_of_stock"


    # def show_item(self, rest):
    #     print(f"""Item: 
    #         title: {self.title}
    #         description: {self.desc}
    #         price: {self.price}
    #         colors: { colors[self.color[0]]}, { colors[self.color[1]] }
    #         { rest }
    #     """)