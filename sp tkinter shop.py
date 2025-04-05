import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox


def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='purchase_db'
    )


# Database Setup
conn = connect_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
    quantity INT NOT NULL
)
""")
conn.commit()


# Insert Data
def add_product():
    name = name_var.get()
    try:
        price = float(price_var.get())
        quantity = int(quantity_var.get())

        if name and price and quantity:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
            conn.commit()
            conn.close()
            fetch_data()
            clear_fields()
            messagebox.showinfo("Success", "Product added successfully")
        else:
            messagebox.showwarning("Warning", "All fields are required")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid price or quantity")


# Fetch Data
def fetch_data():
    tree.delete(*tree.get_children())
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()


# Get Selected Data
def get_selected(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        if values:
            id_var.set(values[0])
            name_var.set(values[1])
            price_var.set(values[2])
            quantity_var.set(values[3])


# Update Data
def update_product():
    product_id = id_var.get()
    name = name_var.get()
    try:
        price = float(price_var.get())
        quantity = int(quantity_var.get())

        if product_id and name and price and quantity:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s",
                           (name, price, quantity, product_id))
            conn.commit()
            conn.close()
            fetch_data()
            clear_fields()
            messagebox.showinfo("Success", "Product updated successfully")
        else:
            messagebox.showwarning("Warning", "All fields are required")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid price or quantity")


# Delete Data
def delete_product():
    product_id = id_var.get()
    if product_id:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        conn.close()
        fetch_data()
        clear_fields()
        messagebox.showinfo("Success", "Product deleted successfully")
    else:
        messagebox.showwarning("Warning", "Select a product to delete")


# Clear Fields
def clear_fields():
    id_var.set("")
    name_var.set("")
    price_var.set("")
    quantity_var.set("")


# GUI Setup
root = tk.Tk()
root.title("Purchase Product CRUD")
root.geometry("500x400")
root.configure(bg="pink")  # Set Background Color

# Variables
id_var = tk.StringVar()
name_var = tk.StringVar()
price_var = tk.StringVar()
quantity_var = tk.StringVar()

# Labels and Entry Fields
tk.Label(root, text="Product Name", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Price", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=price_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=quantity_var).grid(row=2, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Product", command=add_product, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
tk.Button(root, text="Update Product", command=update_product, bg="#FFA500", fg="white").grid(row=3, column=1, pady=10)
tk.Button(root, text="Delete Product", command=delete_product, bg="#FF5733", fg="white").grid(row=4, column=0, pady=10)
tk.Button(root, text="Clear", command=clear_fields, bg="#607D8B", fg="white").grid(row=4, column=1, pady=10)

# Treeview Style
style = ttk.Style()
style.configure("Treeview", background="#E3F2FD", fieldbackground="#E3F2FD", foreground="black")

# Data Display Table (Treeview)
columns = ("ID", "Name", "Price", "Quantity")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
tree.bind("<ButtonRelease-1>", get_selected)

fetch_data()  # Load Data on Start

root.mainloop()