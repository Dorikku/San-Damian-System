from ttkbootstrap import Style
from tkinter import Tk
from ttkbootstrap import DateEntry

# Create a Tkinter window
root = Tk()

# Create a ttkbootstrap style
style = Style(theme='journal')

# Create a DateEntry widget
date_entry = DateEntry(root, style='success.DateEntry')

# Pack the DateEntry widget
date_entry.pack()

# Get the selected date
selected_date = date_entry.get()
print(selected_date)

# Run the Tkinter event loop
root.mainloop()