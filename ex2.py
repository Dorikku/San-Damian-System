import tkinter as tk
from tkinter import ttk

def validate_float(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        return False

# Create the main window
root = tk.Tk()
root.title("Float Entry")
root.geometry("300x100")

# Register the validation function
vcmd = (root.register(validate_float), '%P')

# Create the Entry widget with validation
float_entry = ttk.Entry(root, validate='key', validatecommand=vcmd)
float_entry.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
