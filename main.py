import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# ------------------ Database Setup ------------------ #
client = MongoClient("mongodb://localhost:27017/")
db = client["IceCreamDB"]
collection = db["flavors"]

# ------------------ Main Window ------------------ #
app = tk.Tk()
app.title("Ice Cream Shop - CRUD System")
app.geometry("700x520")
app.config(bg="#fafafa")

# ------------------ Title ------------------ #
title = tk.Label(
    app,
    text="422 - Priyanka Dhingi\nIce Cream Shop Management",
    font=("Verdana", 18, "bold"),
    bg="#fafafa",
    fg="#1f3b4d",
    justify="center"
)
title.pack(pady=15)

# ------------------ Input Section ------------------ #
form = tk.LabelFrame(app, text="Ice Cream Details", font=("Arial", 12, "bold"),
                     bg="#ffffff", fg="#2c3e50", padx=15, pady=15)
form.pack(fill="x", padx=25, pady=10)

# Flavor ID
tk.Label(form, text="Flavor ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=6)
id_box = ttk.Entry(form, width=35)
id_box.grid(row=0, column=1, pady=6)

# Flavor Name
tk.Label(form, text="Flavor Name:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=6)
name_box = ttk.Entry(form, width=35)
name_box.grid(row=1, column=1, pady=6)

# Price
tk.Label(form, text="Price (₹):", font=("Arial", 11), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=6)
price_box = ttk.Entry(form, width=35)
price_box.grid(row=2, column=1, pady=6)

# Category
tk.Label(form, text="Category:", font=("Arial", 11), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=6)
category_box = ttk.Combobox(form, width=33, values=["Cone", "Cup", "Sundae", "Shake"])
category_box.grid(row=3, column=1, pady=6)


# ------------------ Functions ------------------ #
def add_flavor():
    fid, fname, price, cat = id_box.get().strip(), name_box.get().strip(), price_box.get().strip(), category_box.get().strip()

    if not (fid and fname and price and cat):
        messagebox.showwarning("Warning", "Please complete all fields.")
        return

    try:
        collection.insert_one({"flavor_id": fid, "name": fname, "price": price, "category": cat})
        messagebox.showinfo("Success", f"'{fname}' has been added!")
        clear_inputs()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert.\n{e}")


def show_menu():
    try:
        all_data = collection.find()
        output = ""
        for d in all_data:
            output += f"🍦 {d['name']} (ID: {d['flavor_id']})\n   Price: ₹{d['price']} | Type: {d['category']}\n\n"
        result_box.config(text=output if output else "No flavors available.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch data.\n{e}")


def update_flavor():
    win = tk.Toplevel(app)
    win.title("Update Ice Cream Flavor")
    win.geometry("420x280")
    win.config(bg="#eef9f5")

    tk.Label(win, text="Flavor Name to Update:", font=("Arial", 11), bg="#eef9f5").pack(pady=8)
    old_name = ttk.Entry(win, width=30)
    old_name.pack()

    tk.Label(win, text="New Price (₹):", font=("Arial", 11), bg="#eef9f5").pack(pady=8)
    new_price = ttk.Entry(win, width=30)
    new_price.pack()

    tk.Label(win, text="New Category:", font=("Arial", 11), bg="#eef9f5").pack(pady=8)
    new_cat = ttk.Combobox(win, width=28, values=["Cone", "Cup", "Sundae", "Shake"])
    new_cat.pack()

    def confirm_update():
        n, p, c = old_name.get(), new_price.get(), new_cat.get()
        if not (n and p and c):
            messagebox.showwarning("Missing", "Fill all details!")
            return

        res = collection.update_one({"name": n}, {"$set": {"price": p, "category": c}})
        if res.modified_count:
            messagebox.showinfo("Done", "Flavor updated successfully!")
            win.destroy()
        else:
            messagebox.showinfo("No Match", "No matching flavor found.")

    ttk.Button(win, text="Update", command=confirm_update).pack(pady=15)


def delete_flavor():
    win = tk.Toplevel(app)
    win.title("Delete Ice Cream Flavor")
    win.geometry("350x200")
    win.config(bg="#fff0f0")

    tk.Label(win, text="Enter Flavor ID:", font=("Arial", 11), bg="#fff0f0").pack(pady=10)
    fid = ttk.Entry(win, width=30)
    fid.pack()

    def confirm_delete():
        res = collection.delete_many({"flavor_id": fid.get()})
        if res.deleted_count:
            messagebox.showinfo("Deleted", "Flavor removed successfully!")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No flavor found with given ID.")

    ttk.Button(win, text="Delete", command=confirm_delete).pack(pady=15)


def clear_inputs():
    id_box.delete(0, tk.END)
    name_box.delete(0, tk.END)
    price_box.delete(0, tk.END)
    category_box.set("")


# ------------------ Buttons ------------------ #
btns = tk.Frame(app, bg="#fafafa")
btns.pack(pady=15)

ttk.Button(btns, text="Add Flavor", command=add_flavor).grid(row=0, column=0, padx=10)
ttk.Button(btns, text="Show Flavors", command=show_menu).grid(row=0, column=1, padx=10)
ttk.Button(btns, text="Update Flavor", command=update_flavor).grid(row=0, column=2, padx=10)
ttk.Button(btns, text="Delete Flavor", command=delete_flavor).grid(row=0, column=3, padx=10)

# ------------------ Result Display ------------------ #
result_box = tk.Label(app, text="", justify="left", anchor="w", bg="#fafafa", fg="#2c3e50", font=("Consolas", 11))
result_box.pack(pady=10, fill="both", expand=True)

# ------------------ Run App ------------------ #
app.mainloop()
