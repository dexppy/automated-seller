queries = {
    "insert" : "INSERT INTO items(id, type, photo, price, stock, color_1, color_2) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    "insert_cat" : "INSERT INTO categories(category_name) VALUES (%s)",
    "select_where_id" : "SELECT * FROM items JOIN categories ON items.type=categories.type_id WHERE items.id = %s",
    "select_cats" : "SELECT type_id, category_name FROM categories",
    "update_stock_d" : "UPDATE items SET stock = stock-%s WHERE id = %s",
    "update_stock_i" : "UPDATE items SET stock = stock+%s WHERE id = %s",
    "update_photo" : "UPDATE items SET photo = %s WHERE id = %s",
    "update_price" : "UPDATE items SET price = %s WHERE id = %s",
    "select_colors" : "SELECT * FROM colors WHERE id = %s",
    "select_where_cat" : "SELECT * FROM items WHERE type = %s",
    "select_all" : "SELECT * FROM items",
    "select_last_id": "SELECT * FROM items ORDER BY id DESC LIMIT 1"
}