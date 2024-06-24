import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Sample data
data = [
    {"name": "Alice", "date": "2023-06-20"},
    {"name": "Bob", "date": "2023-06-21"},
    {"name": "Charlie", "date": "2023-06-19"},
    {"name": "David", "date": "2023-06-23"},
    {"name": "Eve", "date": "2023-06-22"}
]

# Convert date strings to datetime objects for sorting
for item in data:
    item["date"] = datetime.strptime(item["date"], "%Y-%m-%d")

def load_data(treeview, data):
    # Clear existing data
    for item in treeview.get_children():
        treeview.delete(item)
    
    # Insert new data
    for item in data:
        treeview.insert("", tk.END, values=(item["name"], item["date"].strftime("%Y-%m-%d")))

def apply_filter_sort(treeview, date_var, sort_order_var):
    selected_date = date_var.get()
    sort_order = sort_order_var.get()

    filtered_data = data
    if selected_date != "All":
        filtered_data = [item for item in data if item["date"].strftime("%Y-%m-%d") == selected_date]

    sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=(sort_order == "Descending"))

    load_data(treeview, sorted_data)

def on_combobox_change(event, treeview, date_var, sort_order_var):
    apply_filter_sort(treeview, date_var, sort_order_var)

# Main application
root = tk.Tk()
root.title("Treeview Filter and Sort")

# Combobox for date selection
dates = list(set([item["date"].strftime("%Y-%m-%d") for item in data]))
dates.sort()
date_var = tk.StringVar()
date_combobox = ttk.Combobox(root, textvariable=date_var)
date_combobox['values'] = ["All"] + dates
date_combobox.current(0)
date_combobox.pack(pady=10)

# Combobox for sort order selection
sort_order_var = tk.StringVar()
sort_order_combobox = ttk.Combobox(root, textvariable=sort_order_var)
sort_order_combobox['values'] = ["Ascending", "Descending"]
sort_order_combobox.current(0)
sort_order_combobox.pack(pady=10)

# Treeview widget
treeview = ttk.Treeview(root, columns=("Name", "Date"), show='headings')
treeview.heading("Name", text="Name")
treeview.heading("Date", text="Date")
treeview.pack(pady=10, fill=tk.BOTH, expand=True)

# Bind events to comboboxes to trigger automatic filtering and sorting
date_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(event, treeview, date_var, sort_order_var))
sort_order_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(event, treeview, date_var, sort_order_var))

# Load initial data
load_data(treeview, data)

# Start the main event loop
root.mainloop()
