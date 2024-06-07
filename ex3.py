import tkinter as tk
from tkinter import ttk

def add_combobox():
    # Sample values for the combobox
    values = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    
    # Create a new combobox
    combobox = ttk.Combobox(combobox_frame, values=values)
    combobox.pack(pady=5)
    
    # Add combobox to the list
    comboboxes.append(combobox)

def get_combobox_values():
    for idx, combobox in enumerate(comboboxes, start=1):
        print(f"Combobox {idx} selected value: {combobox.get()}")

# Create the main window
root = tk.Tk()
root.title("Combobox Creator")
root.geometry("300x300")

# List to store combobox references
comboboxes = []

# Button to add combobox
add_button = ttk.Button(root, text="Add Combobox", command=add_combobox)
add_button.pack(pady=10)

# Button to get combobox values
get_button = ttk.Button(root, text="Get Combobox Values", command=get_combobox_values)
get_button.pack(pady=10)

# Frame to hold the comboboxes
combobox_frame = ttk.Frame(root)
combobox_frame.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
