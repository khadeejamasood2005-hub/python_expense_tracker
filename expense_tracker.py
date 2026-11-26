import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                expense_table.insert("", tk.END, values=row)
    update_total()

def save_expenses():
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Category", "Amount"])

        for row in expense_table.get_children():
            writer.writerow(expense_table.item(row)["values"])

def add_expense():
    description = description_entry.get().strip()
    category = category_box.get()
    amount = amount_entry.get().strip()

    if not description or not category or not amount:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showwarning("Warning", "Amount must be greater than zero.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    date = datetime.now().strftime("%d-%m-%Y")

    expense_table.insert(
        "",
        tk.END,
        values=(date, description, category, f"{amount:.2f}")
    )

    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    save_expenses()
    update_total()

def delete_expense():
    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select an expense.")
        return

    for item in selected:
        expense_table.delete(item)

    save_expenses()
    update_total()

def clear_all():
    if expense_table.get_children():
        answer = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete all expenses?"
        )

        if answer:
            for item in expense_table.get_children():
                expense_table.delete(item)

            save_expenses()
            update_total()

def update_total():
    total = 0

    for item in expense_table.get_children():
        values = expense_table.item(item)["values"]
        total += float(values[3])

    total_label.config(text=f"Total Expenses: ₹{total:.2f}")

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x700")
root.resizable(False, False)
root.configure(bg="#eaf2f8")

title = tk.Label(
    root,
    text="EXPENSE TRACKER",
    font=("Arial", 22, "bold"),
    bg="#eaf2f8",
    fg="#154360"
)
title.pack(pady=20)

input_frame = tk.Frame(root, bg="#eaf2f8")
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Description",
    font=("Arial", 11),
    bg="#eaf2f8"
).grid(row=0, column=0, padx=10, pady=5)

description_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
description_entry.grid(row=1, column=0, padx=10)

tk.Label(
    input_frame,
    text="Category",
    font=("Arial", 11),
    bg="#eaf2f8"
).grid(row=0, column=1, padx=10, pady=5)

category_box = ttk.Combobox(
    input_frame,
    values=["Food", "Travel", "Shopping", "Bills", "Other"],
    state="readonly",
    width=18
)
category_box.grid(row=1, column=1, padx=10)
category_box.set("Food")

tk.Label(
    input_frame,
    text="Amount (₹)",
    font=("Arial", 11),
    bg="#eaf2f8"
).grid(row=0, column=2, padx=10, pady=5)

amount_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
amount_entry.grid(row=1, column=2, padx=10)

add_button = tk.Button(
    root,
    text="ADD EXPENSE",
    command=add_expense,
    font=("Arial", 11, "bold"),
    bg="#2874a6",
    fg="white",
    width=20
)
add_button.pack(pady=15)

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("Date", "Description", "Category", "Amount")

expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)

expense_table.heading("Date", text="Date")
expense_table.heading("Description", text="Description")
expense_table.heading("Category", text="Category")
expense_table.heading("Amount", text="Amount (₹)")

expense_table.column("Date", width=120, anchor="center")
expense_table.column("Description", width=200, anchor="center")
expense_table.column("Category", width=150, anchor="center")
expense_table.column("Amount", width=120, anchor="center")

expense_table.pack()

delete_button = tk.Button(
    root,
    text="DELETE SELECTED",
    command=delete_expense,
    font=("Arial", 10, "bold"),
    bg="#c0392b",
    fg="white",
    width=20
)
delete_button.pack(pady=5)

clear_button = tk.Button(
    root,
    text="CLEAR ALL EXPENSES",
    command=clear_all,
    font=("Arial", 10),
    bg="#d5d8dc",
    width=20
)
clear_button.pack(pady=5)

total_label = tk.Label(
    root,
    text="Total Expenses: ₹0.00",
    font=("Arial", 18, "bold"),
    bg="#eaf2f8",
    fg="#154360"
)
total_label.pack(side=tk.BOTTOM,pady=20)

load_expenses()

root.mainloop()