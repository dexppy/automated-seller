colors = { "sr": "Srebrny",
        "zl": "Złoty",
        'cz': "Czarny",
        'bi': "Biały", 
        'ro': "Różowy", 
        'fi': "Fioletowy", 
        'ce': "Czerwony", 
        'nb': "Niebieski", 
        'zi': "Zielony", 
        'po': "Pomarańczowy", 
        'zo': "Żółty",
        'br': "Brązowy",
        'sz': "Szary",
        '00': "brak"
}

def show_colors():
        colrs = ""

        for color in colors:
                colrs += f"{colors[color]}: {color}, "

        print(colrs)




