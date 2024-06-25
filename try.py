import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Sample data
data = [
    {"name": "Alice", "date": "6/20/2023"},
    {"name": "Bob", "date": "6/20/2023"},
    {"name": "Charlie", "date": "6/20/2023"},
    {"name": "David", "date": "6/20/2023"},
    {"name": "Eve", "date": "6/20/2023"},
    {"name": "Fuck", "date": "7/20/2023"}
]

# Convert date strings to datetime objects for sorting
for item in data:
    item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

# Function to get the month name and year in the desired format
def get_month_year_string(date):
    return date.strftime("%B %Y")

# Extract unique months and years from the data
unique_months = list(set([get_month_year_string(item["date"]) for item in data]))
unique_months.sort(key=lambda date: datetime.strptime(date, "%B %Y"))

def load_data(treeview, data):
    # Clear existing data
    for item in treeview.get_children():
        treeview.delete(item)
    
    # Insert new data
    for item in data:
        treeview.insert("", tk.END, values=(item["name"], item["date"].strftime("%m/%d/%Y")))

def apply_filter_sort(treeview, month_var, sort_order_var):
    selected_month = month_var.get()
    sort_order = sort_order_var.get()

    filtered_data = data
    if selected_month != "All":
        selected_month_datetime = datetime.strptime(selected_month, "%B %Y")
        filtered_data = [item for item in data if item["date"].year == selected_month_datetime.year and item["date"].month == selected_month_datetime.month]

    sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=(sort_order == "Descending"))

    load_data(treeview, sorted_data)

def on_combobox_change(event, treeview, month_var, sort_order_var):
    apply_filter_sort(treeview, month_var, sort_order_var)

# Main application
root = tk.Tk()
root.title("Treeview Filter and Sort")

# Combobox for month selection
month_var = tk.StringVar()
month_combobox = ttk.Combobox(root, textvariable=month_var)
month_combobox['values'] = ["All"] + unique_months
month_combobox.current(0)
month_combobox.pack(pady=10)

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
month_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(event, treeview, month_var, sort_order_var))
sort_order_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(event, treeview, month_var, sort_order_var))

# Load initial data
load_data(treeview, data)

# Start the main event loop
root.mainloop()
