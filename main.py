import tkinter as tk
from tkinter import ttk
import sqlite3


#Удаление файлов бд
#conn = sqlite3.connect('warehouse.db')
#c = conn.cursor()
#c.execute("DELETE FROM products")
#conn.commit()
#conn.close()



def load_inventory_from_db(cursor):
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        inventory_text.insert(tk.END, f"Товар: {row[1]}, Количество: {row[2]}\n")

def arrival():
    product = product_entry.get()
    quantity = int(quantity_entry.get())
    c.execute("SELECT * FROM products WHERE name=?", (product,))
    row = c.fetchone()
    if row:
        new_quantity = row[2] + quantity
        c.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_quantity, product))
    else:
        c.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (product, quantity))
    conn.commit()
    inventory_text.delete(1.0, tk.END)
    load_inventory_from_db(c)
    product_entry.delete(0, tk.END)  # Очистка поля "Введите товар"
    quantity_entry.delete(0, tk.END)  # Очистка поля "Введите количество"

def departure():
    product = product_entry.get()
    quantity = int(quantity_entry.get())
    c.execute("SELECT quantity FROM products WHERE name=?", (product,))
    row = c.fetchone()

    # Проверяем, что row не None, что значит товар найден в базе данных
    if row:
        new_quantity = row[0] - quantity
        if new_quantity <= 0:
            # Если количество становится 0 или меньше, удаляем товар из базы данных
            c.execute("DELETE FROM products WHERE name=?", (product,))
        else:
            # Иначе обновляем количество
            c.execute("UPDATE products SET quantity=? WHERE name=?", (new_quantity, product))
        conn.commit()
    else:
        print("Товар не найден")

    inventory_text.delete(1.0, tk.END)
    load_inventory_from_db(c)
    product_entry.delete(0, tk.END)  # Очистка поля "Введите товар"
    quantity_entry.delete(0, tk.END)  # Очистка поля "Введите количество"


def delete_selected_item():
    if inventory_text.tag_ranges("sel"):
        start_index = inventory_text.index("sel.first")
        end_index = inventory_text.index("sel.last")
        selected_text = inventory_text.get(start_index, end_index)
        if selected_text:
            if ',' in selected_text and ':' in selected_text:
                product = selected_text.split(',')[0].split(':')[1].strip()
                c.execute("DELETE FROM products WHERE name = ?", (product,))
                conn.commit()
                inventory_text.delete(start_index, end_index)
                inventory_text.delete(1.0, tk.END)
                load_inventory_from_db(c)
    else:
        print("Не выбран текст для удаления")

def finish():
    conn.close()
    root.destroy()

root = tk.Tk()
root.geometry("800x600")
root.title("АРМ работника склада")

left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = ttk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

label_product = tk.Label(left_frame, text="Введите товар:")
label_product.pack()

product_entry = tk.Entry(left_frame, bg="beige")
product_entry.pack()

label_quantity = tk.Label(left_frame, text="Введите количество:")
label_quantity.pack()

quantity_entry = tk.Entry(left_frame, bg="beige")
quantity_entry.pack()

btnArr = ttk.Button(left_frame, text="Приход", command=arrival)
btnArr.pack(fill=tk.X)

btnDep = ttk.Button(left_frame, text="Уход", command=departure)
btnDep.pack(fill=tk.X)

btnDel = ttk.Button(left_frame, text="Удалить", command=delete_selected_item)
btnDel.pack(fill=tk.X)

btnFinish = ttk.Button(left_frame, text="Закрыть приложение", command=finish)
btnFinish.pack(fill=tk.X)

label_inventory = tk.Label(right_frame, text="Список товаров:")
label_inventory.pack()

inventory_text = tk.Text(right_frame, width=60, height=20, bg="beige")
inventory_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

vsb = ttk.Scrollbar(right_frame, orient="vertical", command=inventory_text.yview)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
inventory_text.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(right_frame, orient="horizontal", command=inventory_text.xview)
hsb.pack(side=tk.BOTTOM, fill=tk.X)
inventory_text.configure(xscrollcommand=hsb.set)

conn = sqlite3.connect('warehouse.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)''')
conn.commit()

load_inventory_from_db(c)

root.mainloop()
