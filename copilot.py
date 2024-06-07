import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk

root = tb.Window()
root.geometry("300x200")

# Define the font
font_style = ('Poppins', 12)

# Create Combobox
combo = tb.Combobox(root, font=('Poppins', 12, 'bold'), width=15)
combo['values'] = ('Option 1', 'Option 2', 'Option 3')
combo.pack(pady=20)

# Change the font of the options
combo.option_add('*TCombobox*Listbox.font', font_style)

root.mainloop()
