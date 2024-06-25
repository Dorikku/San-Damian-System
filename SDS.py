import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from SDC_system import sdcExpenses
from tkinter import messagebox, simpledialog
from ttkbootstrap.dialogs import Querybox
import os
import sys
import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_rowcol_to_cell
from datetime import datetime



sdc_expenses = sdcExpenses()

class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
    

        # Make frame scrollable using mouse scroll wheel
        # def _on_mousewheel(event):
        #     canvas.yview_scroll(-1 * int(event.delta/120), "units")

        # canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


def homepage():
    global main_frame, hovered_row
    # , table, total_expenditures_label, base_income_label, remaining_balance_label, base_income, data

    def refresh_table(table_data):
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(table_data):
            table.insert("", "end", iid=index, values=(f'                   {entry["date"].strftime("%m/%d/%Y")}', entry["name"], entry["amount"], entry["expenditure"], entry["description"]))


    # Functions
    def on_open_details(index):
        def show_details():
            view_window = tb.Toplevel(root)
            center_window(root, view_window, 440, 400)
            # view_window.resizable(width=False, height=True)
            view_window.iconbitmap(resource_path('sds_icon.ico'))

            details_data = sdc_expenses.get_info(data[index]["expenseIDs"])



            # tb.Label(view_window, text="Expenditure Details", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).pack(pady=(30,20))
            scrollbar = VerticalScrolledFrame(view_window)
            scrollbar.pack(fill=BOTH, expand=True)

            view_frame = tb.Frame(scrollbar.interior)
            view_frame.pack(fill=X, expand=True, padx=30, pady=(0,20), side=tk.LEFT)
            tb.Label(view_frame, text="Expenditure Details", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).grid(row=0, column=1, columnspan=2)


            tb.Label(view_frame, image=calendar_icon).grid(row=1, column=0, sticky="w")
            tb.Label(view_frame, image=name_icon).grid(row=2, column=0, sticky="w")
            tb.Label(view_frame, image=expenditure_icon).grid(row=3, column=0, sticky="w")
            tb.Label(view_frame, text="Date", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=1, column=1, sticky="w")
            tb.Label(view_frame, text="Name", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=2, column=1, sticky="w")
            tb.Label(view_frame, text="Expenditure", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=3, column=1, sticky="w")
            tb.Label(view_frame, text="Amount", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=3, column=2, sticky="e")

            tb.Label(view_frame, text=data[index]['date'].strftime("%m/%d/%Y"), bootstyle=DARK, font=('Poppins', 11)).grid(row=1, column=2, sticky="e")
            tb.Label(view_frame, text=data[index]['name'], bootstyle=DARK, font=('Poppins', 11)).grid(row=2, column=2, sticky="e")

            i = 0
            for i, detail in enumerate(details_data):
                tb.Label(view_frame, text=detail['expenditure'], bootstyle=DARK, font=('Poppins', 11)).grid(row=4+i, column=1, sticky="w")
                tb.Label(view_frame, text=detail['amount'], bootstyle=DARK, font=('Poppins', 11)).grid(row=4+i, column=2, sticky="e")
                

            tb.Label(view_frame, text="-----------------------------------------", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=5+i, column=1, sticky="w", columnspan=2)
            tb.Label(view_frame, text="TOTAL", bootstyle=DARK, font=('Poppins', 12, 'bold')).grid(row=6+i, column=1, sticky="w")
            tb.Label(view_frame, text=data[index]['amount'], bootstyle=DARK, font=('Poppins', 12, 'bold')).grid(row=6+i, column=2, sticky="e")
            tb.Label(view_frame, image=details_icon).grid(row=7+i, column=0, sticky="w")
            tb.Label(view_frame, text="Description", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=7+i, column=1, sticky="w")
            tb.Label(view_frame, text=data[index]['description'], bootstyle=DARK, font=('Poppins', 11), wraplength=340).grid(row=8+i, column=1, columnspan=3, sticky="w")


            # print(details_data)

            


        return show_details

    def on_delete(row_index):
        def confirm_delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):

                # print(data[row_index]["expenseIDs"])
                # sdc_expenses.delete_expense(data[row_index]["date"], data[row_index]["name"])
                sdc_expenses.delete_expense(data[row_index]["expenseIDs"])
                
                # refresh_table()
                homepage()
        return confirm_delete

    def on_edit(row_index):
        def edit_entry():
            new_date = messagebox.showinfo("Edit Entry", "The system doesn't support editing entries yet")
        return edit_entry

    def on_hover(event):
        global hovered_row
        row_id = table.identify_row(event.y)
        if row_id != hovered_row:
            if hovered_row:
                for btn in table.winfo_children():
                    btn.destroy()
                table.item(hovered_row, tags=('normal',))
            table.item(row_id, tags=('hovered',))
            try:
                index = int(row_id)
                delete_button = tb.Button(table,image=delete_icon, command=on_delete(index), bootstyle="link")
                edit_button = tb.Button(table,image=edit_icon, command=on_edit(index), bootstyle="link")
                open_button = tb.Button(table, text="OPEN", image=open_icon, compound=tk.LEFT, command=on_open_details(index), bootstyle="secondary-link", style="secondary.Link.TButton")
                bbox = table.bbox(row_id)
                edit_button.place(x=bbox[0] + 30, y=bbox[1]-4)
                delete_button.place(x=bbox[0], y=bbox[1]-4)
                open_button.place(x=bbox[0] + bbox[2] - 100, y=bbox[1]-4)
                hovered_row = row_id
            except:
                pass

    def on_leave(event):
        global hovered_row
        if hovered_row:
            table.item(hovered_row, tags=('normal',))
            for btn in table.winfo_children():
                btn.destroy()
            hovered_row = None

    # No-op function
    def do_nothing(event):
        return "break"

    def validate_float(value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False

    def add_expenditure():
        # frame for entry
        entry_frame = tb.Frame(expenses_frame)
        entry_frame.pack(fill=X, expand=True, pady=(0, 5))

        # create a new combobox
        combobox = tb.Combobox(entry_frame, values=[entry["expenditure"] for entry in expenditures_data], bootstyle=DARK, font=('Poppins', 11), width=17)
        combobox.pack(side=tk.LEFT)
        # combobox.pack(fill=X, expand=True, pady=(0, 5))
        combobox.bind("<MouseWheel>", do_nothing)

        vcmd = (expenses_frame.register(validate_float), '%P')

        amuont_entry = tb.Entry(entry_frame, bootstyle=DARK, font=('Poppins', 11), width=7, validate='key', validatecommand=vcmd)
        amuont_entry.pack(side=tk.RIGHT, padx=(5,0))

        # Add combobox to the list
        comboboxes.append(combobox)
        amount_boxes.append(amuont_entry)

    def refresh():
        expenditures = []
        amounts = []

        # get the date
        date_text = date.entry.get()

        if name_box.get() == "":
            messagebox.showerror("Error", "Please select a student", parent=add_expenses_window)
            return
        # print(f'Name: {name_box.get()}')
        name = name_box.get()

        for idx, combobox in enumerate(comboboxes):
            if combobox.get() == "":
                messagebox.showerror("Error", "Please select an expenditure", parent=add_expenses_window)
                return
            # print(f"Combobox {idx} selected value: {combobox.get()}")
            expenditures.append(combobox.get())

        for idx, entry in enumerate(amount_boxes):
            if entry.get() == "":
                messagebox.showerror("Error", "Please enter an amount", parent=add_expenses_window)
                return
            # print(f"Entry {idx} amount: {entry.get()}")
            amounts.append(entry.get())

        description = ""
        if description_box.get("1.0", tk.END) != "\n":
            description = description_box.get("1.0", tk.END)


        for i in range(len(expenditures)):
            sdc_expenses.add_expenses(date_text, name, expenditures[i], amounts[i], description)

        # Update table
        homepage()
        add_expenses_window.destroy() 
        add_new_entry()

    def center_window(parent, window, width, height):
        # Get the parent's dimensions and position
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate the x and y coordinates to center the window relative to the parent
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        # Set the geometry of the window to center it
        window.geometry(f"{width}x{height}+{x}+{y}")

    def add_new_entry():
        global expenses_frame, comboboxes, expenditures_data, add_expenses_window, amount_boxes, description_box, name_box, date

        add_expenses_window = tb.Toplevel(root)
        center_window(root, add_expenses_window, 400, 620)
        add_expenses_window.resizable(width=False, height=True)
        add_expenses_window.iconbitmap(resource_path('sds_icon.ico'))

        # new_expenses = tb.Frame(add_expenses_window)
        # new_expenses.pack(fill=X, expand=True, padx=30, pady=(0,20), side=tk.LEFT)
        scrollbar = VerticalScrolledFrame(add_expenses_window)
        scrollbar.pack(fill=BOTH, expand=True)

        new_expenses = tb.Frame(scrollbar.interior)
        new_expenses.pack(fill=X, expand=True, padx=60, pady=(0,20), side=tk.LEFT)


        tb.Label(new_expenses, text="Add Expenses", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).pack(pady=(30,20))


        tb.Label(new_expenses, text="Date: ", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
        date = tb.DateEntry(new_expenses, bootstyle=SUCCESS)  
        date.pack(fill=X, expand=True, pady=(0, 15))
        date.entry.configure(font=('Poppins', 11), bootstyle=DARK)
        

        get_student = sdc_expenses.display_students()
        student_names = [student["name"] for student in get_student]
        tb.Label(new_expenses, text="Student:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
        name_box = tb.Combobox(new_expenses, values=student_names, bootstyle=DARK, font=('Poppins', 11))
        name_box.pack(fill=X, expand=True, pady=(0, 15))
        name_box.bind("<MouseWheel>", do_nothing)

        # List to store combobox references
        comboboxes = []
        amount_boxes = []
        # get expenditures data from the database
        expenditures_data = sdc_expenses.get_expenditures()

        tb.Label(new_expenses, text="Expenditure:                         Amount:", bootstyle="DARK", font=('Poppins', 11)).pack(fill=X)
        expenses_frame = tb.Frame(new_expenses)
        expenses_frame.pack(fill=X, expand=True)
        add_expenditure()

        submit_button = tb.Button(new_expenses, text="➕Add Expenditure", bootstyle="outline-secondary", command=add_expenditure)
        submit_button.pack(pady=(2,15))

        tb.Label(new_expenses, text="Description (optional):", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)

        description_box = tb.Text(new_expenses, height=2, font=('Poppins', 11))
        description_box.pack(fill=X, expand=True, pady=(0, 30))



        submit_button = tb.Button(new_expenses, text="Submit", bootstyle=SUCCESS, command=refresh)
        submit_button.pack(fill=X)




    def update_base_income():
        new_income = simpledialog.askfloat("Base Balance", "Enter new base income:")
        if new_income is not None:
            base_income.set(new_income)
            update_highlights(data)

    def update_highlights(sorted_data):
        total_expenditures = sum(entry["amount"] for entry in sorted_data)
        remaining_balance = base_income.get() - total_expenditures
        base_income_label.config(text=f"Base Balance:    {base_income.get()}")
        remaining_balance_label.config(text=f"Remaining Balance:    {remaining_balance}")
        total_expenditures_label.config(text=f"Total Expenditures:     {total_expenditures}")


    def apply_filter_sort(table, month_var, sort_var, order_var):
        month = month_var.get()
        sort = sort_var.get()
        order = order_var.get()

        filtered_data = data
        if month != "All":
            month_datetime = datetime.strptime(month, "%B %Y")
            filtered_data = [item for item in data if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]

        if sort == "Name":
            sorted_data = sorted(filtered_data, key=lambda x: x["name"], reverse=(order == "Descending"))
        elif sort == "Amount":
            sorted_data = sorted(filtered_data, key=lambda x: x["amount"], reverse=(order == "Descending"))
        else:
            sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=(order == "Descending"))

        # load_data(treeview, sorted_data)
        refresh_table(sorted_data)
        update_highlights(sorted_data)

    def on_combobox_change(event, table, month_var, sort_var, order_var):
        apply_filter_sort(table, month_var, sort_var, order_var)

    # Function to get the month name and year in the desired format
    def get_month_year_string(date):
        return date.strftime("%B %Y")
    

    # Data
    data = sdc_expenses.display_outgoings_table()

    # Convert date strings to datetime objects for sorting
    for item in data:
        item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Header Buttons
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill=X, pady=10, padx=30)


    # Extract unique months and years from the data
    unique_months = list(set([get_month_year_string(item["date"]) for item in data]))
    unique_months.sort(key=lambda date: datetime.strptime(date, "%B %Y"))
    # Sort Month
    # months = ['January', ' February',' March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_var = tk.StringVar()
    month_menu = tb.Combobox(header_frame, textvariable=month_var, values=["All"] + unique_months, state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    month_menu.pack(side=LEFT, padx=20)
    month_menu.current(0)   

    # Sort By Name, Date, Amount
    sort_var = tk.StringVar()
    sort_menu = tb.Combobox(header_frame, textvariable=sort_var, values=["Date", "Name", "Amount"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    sort_menu.pack(side=LEFT, padx=20)
    sort_menu.current(0)

    order_var = tk.StringVar()  
    asc_desc_menu = tb.Combobox(header_frame, textvariable=order_var, values=["Ascending", "Descending"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    asc_desc_menu.pack(side=LEFT, padx=20)
    asc_desc_menu.current(1)

    # Table
    table_frame = tb.Frame(main_frame)
    table_frame.pack(fill=BOTH, expand=True, padx=50, pady=1)
    columns = ("Date", "Name", "Amount", "Expenditures", "Description")
    table = tb.Treeview(table_frame, columns=columns, show="headings")
    table.heading("Date", text="Date")
    table.heading("Name", text="Name")
    table.heading("Amount", text="Amount")
    table.heading("Expenditures", text="Expenditures")
    table.heading("Description", text="Description")
    table.column("Amount", anchor="center")


    month_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, table, month_var, sort_var, order_var))
    sort_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, table, month_var, sort_var, order_var))
    asc_desc_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, table, month_var, sort_var, order_var))


    refresh_table(data)

    table.pack(side=tk.LEFT, fill=BOTH, expand=True)


    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click


    hovered_row = None

    # Bind the hover event
    table.bind("<Motion>", on_hover)
    table.bind("<Leave>", on_leave)

    # Create a vertical scrollbar
    vsb = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Treeview to use the vertical scrollbar
    table.configure(yscrollcommand=vsb.set)

    

    # Highlights
    highlight_frame = tb.Frame(main_frame)
    highlight_frame.pack(fill=X, padx=50)

    # New Entry Button
    new_button = tb.Button(highlight_frame, text="Add Expenses", image=add_icon, compound=tk.LEFT, command=add_new_entry, bootstyle="outline-secondary", style="secondary.Outline.TButton")
    new_button.pack(fill=X, pady=2)


    base_income = tk.DoubleVar(value=50000)
    base_income_label = tb.Label(highlight_frame, text=f"Base Balance: {base_income.get()}", bootstyle=DARK)
    base_income_label.pack(side=LEFT, pady=30)
    base_income_label.bind("<Enter>", lambda e: base_income_label.config(bootstyle=DANGER))
    base_income_label.bind("<Leave>", lambda e: base_income_label.config(bootstyle=DARK))
    base_income_label.bind("<Button-1>", lambda e: update_base_income())

    remaining_balance_label = tb.Label(highlight_frame, text="Remaining Balance: ", bootstyle=DARK)
    remaining_balance_label.pack(side=LEFT, padx=60)

    total_expenditures_label = tb.Label(highlight_frame, text="Total Expenditures: ", bootstyle=DARK)
    total_expenditures_label.pack(side=LEFT)



    update_highlights(data)


def students_page():
    global main_frame

    # No-op function
    def do_nothing(event):
        return "break"
    

    def refresh_table():
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(data):
            table.insert("", "end", iid=index, values=(entry["studentID"], entry["name"]))


    def on_hover(event):
        global hovered_row
        row_id = table.identify_row(event.y)
        if row_id != hovered_row:
            if hovered_row:
                for btn in table.winfo_children():
                    btn.destroy()
                table.item(hovered_row, tags=('normal',))
            table.item(row_id, tags=('hovered',))
            try:
                index = int(row_id)
                delete_button = tb.Button(table,image=delete_icon, command=on_delete(index), bootstyle="link")
                edit_button = tb.Button(table,image=edit_icon, command=on_edit(index), bootstyle="link")
                bbox = table.bbox(row_id)
                edit_button.place(x=bbox[0] + 30, y=bbox[1]-2)
                delete_button.place(x=bbox[0], y=bbox[1]-2)
                hovered_row = row_id
            except:
                pass


    def on_leave(event):
        global hovered_row
        if hovered_row:
            table.item(hovered_row, tags=('normal',))
            for btn in table.winfo_children():
                btn.destroy()
            hovered_row = None


    # Functions
    def on_delete(row_index):
        def confirm_delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
                refresh_table()
        return confirm_delete


    def on_edit(row_index):
        def edit_entry():
            new_date = messagebox.showinfo("Edit Entry", "The system doesn't support editing entries yet")
        return edit_entry


    def add_new_entry():
        new_date = simpledialog.askstring("New Entry", "Enter Date:")


    # Data
    data = sdc_expenses.display_students()

    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Header Buttons
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill=X, pady=10, padx=30)

    # Sort By Name, Date, Amount
    sort_menu = tb.Combobox(header_frame, values=["Id", "Name"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    sort_menu.pack(side=LEFT, padx=20)
    sort_menu.current(0)

    asc_desc_menu = tb.Combobox(header_frame, values=["Ascending", "Descending"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    asc_desc_menu.pack(side=LEFT, padx=20)
    asc_desc_menu.current(1)

    # Table
    table_frame = tb.Frame(main_frame)
    table_frame.pack(fill=BOTH, expand=True, padx=50, pady=1)
    columns = ("studentID", "name")
    table = tb.Treeview(table_frame, columns=columns, show="headings")
    table.heading("studentID", text="Student ID")
    table.heading("name", text="Name", anchor="w")
    table.pack(side=tk.LEFT, fill=BOTH, expand=True)
    table.column("studentID", anchor="center")

    table.tag_configure('hovered', background='#d9d9d9')
    table.tag_configure('normal', background='white')

    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click

    refresh_table()

    # Bind the hover event
    table.bind("<Motion>", on_hover)
    table.bind("<Leave>", on_leave)

    # Create a vertical scrollbar
    vsb = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Treeview to use the vertical scrollbar
    table.configure(yscrollcommand=vsb.set)


    # Highlights
    highlight_frame = tb.Frame(main_frame)
    highlight_frame.pack(fill=X, padx=50)

    # New Entry Button
    new_button = tb.Button(highlight_frame, text="Add Student", image=add_icon, compound=tk.LEFT, command=add_new_entry, bootstyle="outline-secondary", style="secondary.Outline.TButton")
    new_button.pack(fill=X, pady=2)


    total_students_label = tb.Label(highlight_frame, text=f"Total Students:    {len(data)}", bootstyle=DARK)
    total_students_label.pack(side=LEFT, pady=30)

    # Highlights
    # footer = tb.Frame(main_frame)
    # footer.pack(fill=X, padx=50, pady=20)


def incomings_page():
    global main_frame

    # No-op function
    def do_nothing(event):
        return "break"


    def refresh_table():
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(data):
            table.insert("", "end", iid=index, values=(entry["date"], entry["description"], entry["amount"]))


    def on_hover(event):
        global hovered_row
        row_id = table.identify_row(event.y)
        if row_id != hovered_row:
            if hovered_row:
                for btn in table.winfo_children():
                    btn.destroy()
                table.item(hovered_row, tags=('normal',))
            table.item(row_id, tags=('hovered',))
            try:
                index = int(row_id)
                delete_button = tb.Button(table,image=delete_icon, command=on_delete(index), bootstyle="link")
                edit_button = tb.Button(table,image=edit_icon, command=on_edit(index), bootstyle="link")
                open_button = tb.Button(table, text="OPEN", image=open_icon, compound=tk.LEFT, command=on_open_details(data[index]["description"]), bootstyle="secondary-link", style="secondary.Link.TButton")
                bbox = table.bbox(row_id)
                edit_button.place(x=bbox[0] + 30, y=bbox[1]-2)
                delete_button.place(x=bbox[0], y=bbox[1]-2)
                open_button.place(x=bbox[0] + bbox[2] - 100, y=bbox[1]-3)
                hovered_row = row_id
            except:
                pass


    def on_leave(event):
        global hovered_row
        if hovered_row:
            table.item(hovered_row, tags=('normal',))
            for btn in table.winfo_children():
                btn.destroy()
            hovered_row = None


    # Functions
    def on_open_details(details):
        def show_details():
            messagebox.showinfo("Expenditure Details", details)
        return show_details
    

    def on_delete(row_index):
        def confirm_delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
                refresh_table()
        return confirm_delete


    def on_edit(row_index):
        def edit_entry():
            new_date = messagebox.showinfo("Edit Entry", "The system doesn't support editing entries yet")
        return edit_entry


    def add_new_entry():
        new_date = simpledialog.askstring("New Entry", "Enter Date:")


    # Data
    data = sdc_expenses.display_incoming_table()
    
    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Header Buttons
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill=X, pady=10, padx=30)

    # Sort Month
    months = ['January', ' February',' March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_menu = tb.Combobox(header_frame, values=months, state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    month_menu.pack(side=LEFT, padx=20)
    month_menu.current(0)
    
    month_menu.config()

    # Table
    table_frame = tb.Frame(main_frame)
    table_frame.pack(fill=BOTH, expand=True, padx=50, pady=1)
    columns = ("date", "description", "amount") 
    table = tb.Treeview(table_frame, columns=columns, show="headings")
    table.heading("date", text="Date")
    table.heading("description", text="Description")
    table.heading("amount", text="Amount")
    table.pack(side=tk.LEFT, fill=BOTH, expand=True)
    table.column("date", anchor="center")

    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click

    refresh_table()

    # Bind the hover event
    table.bind("<Motion>", on_hover)
    table.bind("<Leave>", on_leave)

    # Create a vertical scrollbar
    vsb = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Treeview to use the vertical scrollbar
    table.configure(yscrollcommand=vsb.set)


    # Highlights
    highlight_frame = tb.Frame(main_frame)
    highlight_frame.pack(fill=X, padx=50)

    # New Entry Button
    new_button = tb.Button(highlight_frame, text="Add Income", image=add_icon, compound=tk.LEFT, command=add_new_entry, bootstyle="outline-secondary", style="secondary.Outline.TButton")
    new_button.pack(fill=X, pady=2)

    total_amount = sum(entry["amount"] for entry in data)
    total_amount_label = tb.Label(highlight_frame, text=f"Total Amount:  {total_amount}", bootstyle=DARK)
    total_amount_label.pack(side=LEFT, pady=30)


def search_page():
    global main_frame

    # functions for entry widget
    def on_focus_in(entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(foreground='grey')

    def add_placeholder(entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(foreground='grey')
        entry.bind('<FocusIn>', lambda e: on_focus_in(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: on_focus_out(entry, placeholder))

    def on_key_release(event):
        query = entry.get()
        update_listbox(query)

    def update_listbox(query):
        results, total = sdc_expenses.display_student_expenses(query)

        total_amount_label.config(text=f"Total Amount:  {total}")
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(results):
            table.insert("", "end", iid=index, values=(entry["date"], entry["name"], entry["expenditure"], entry["amount"], entry["description"]))


    def get_name(event):
        select = table.focus()
        name = table.item(select, 'values')[1]
        # print(name)
        entry.delete(0, tk.END)
        entry.insert(0, name)
        update_listbox(name)


    global entry

    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Header frame
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill=X, pady=10, padx=50)

    # search bar frame
    search_frame = tb.Frame(main_frame)
    search_frame.pack(fill=X, pady=10, padx=50)

    # Sort Month
    months = ['January', ' February',' March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_menu = tb.Combobox(header_frame, values=months, state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    month_menu.pack(side=LEFT)
    month_menu.current(0)  

    entry = tb.Entry(search_frame, bootstyle="success")
    entry.pack(fill=X)
    entry.config(font=('Poppins', 12))

    placeholder_text = "🔍Search Student..."
    add_placeholder(entry, placeholder_text)
    entry.bind('<KeyRelease>', on_key_release)

    # Table
    table_frame = tb.Frame(main_frame)
    table_frame.pack(fill=BOTH, expand=True, padx=50, pady=1)

    columns = ("Date", "Name", "Expenditures", "Amount", "Description")
    table = tb.Treeview(table_frame, columns=columns, show="headings")
    table.heading("Date", text="Date")
    table.heading("Name", text="Name", anchor="w")
    table.heading("Expenditures", text="Expenditures")
    table.heading("Amount", text="Amount")
    table.heading("Description", text="Description", anchor="w")
    table.column("Date", anchor="center")
    table.column("Amount", anchor="center")
    table.column("Expenditures", anchor="center")

    table.bind("<ButtonRelease-1>", get_name)
    table.pack(side=tk.LEFT, fill=BOTH, expand=True)

    # Create a vertical scrollbar
    vsb = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(fill=tk.Y, side=tk.RIGHT)

    # scrollbar frame
    hsb_frame = tb.Frame(main_frame)
    hsb_frame.pack(fill=X, padx=50)

    # Create a vertical scrollbar
    hsb = tb.Scrollbar(hsb_frame, orient="horizontal", command=table.xview)
    hsb.pack(fill=tk.X)

    # Configure the Treeview to use the vertical scrollbar
    table.configure(yscrollcommand=vsb.set)
    table.configure(xscrollcommand=hsb.set)

    

    # Highlights
    highlight_frame = tb.Frame(main_frame)
    highlight_frame.pack(fill=X, padx=50)

    total_amount_label = tb.Label(highlight_frame, text=f"Total Amount: ", bootstyle=DARK, font=('Poppins', 12, 'bold'))
    total_amount_label.pack(side=LEFT, pady=30)

    update_listbox("")




def export_page():
    global main_frame

    def export_report():
        data = sdc_expenses.display_outgoings_table()
        df = pd.DataFrame(data)
        # df.to_excel("report.xlsx", index=False)

        writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']

        # Add formats for styling
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#F7F7F7', 'border': 1})
        data_format = workbook.add_format({'align': 'center', 'border': 1})

        # Apply formats to headers and data
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        for row_num in range(len(df)):
            for col_num, value in enumerate(df.iloc[row_num]):
                worksheet.write(row_num + 1, col_num, value, data_format)

        # Auto-adjust column width
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col))
            worksheet.set_column(i, i, column_len + 2)

        # Close the Pandas Excel writer and output the Excel file
        writer.close()
        messagebox.showinfo("Export Report", "Report exported successfully")



    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    export_button = tb.Button(main_frame, text="Export Report", bootstyle="success", command=export_report)
    export_button.pack(pady=60)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Create the main application window
root = tb.Window(themename="yeti")
root.geometry("1360x768")
root.title("San Damian System")
root.iconbitmap(resource_path("sds_icon.ico"))

# Configure the fonts
style = tb.Style()
style.configure('danger.TLabel', font=('Poppins', 12))
style.configure('dark.TLabel', font=('Poppins', 12))
style.configure('TButton', font=('Poppins', 11))
style.configure('but.success.TButton', font=('Poppins', 12))
style.configure('secondary.Link.TButton', font=('Poppins', 10))
style.configure('Treeview.Heading', font=('Poppins', 12, 'bold'))
style.configure('Treeview', font=('Poppins', 12))
style.configure('Treeview', rowheight=30)
style.configure('secondary.Outline.TButton', font=('Poppins', 11))
# style.configure('success.TEntry', font=('Poppins', 6))


# Main Frame
main_frame = tb.Frame(root, padding=30)
main_frame.pack(side=LEFT, fill=BOTH, expand=True)


# Navigation Bar
nav_frame = tb.Frame(root, padding=10, bootstyle="SUCCESS")
nav_frame.pack(side=LEFT, fill=Y)

# Load the image
home_dark = PhotoImage(file=resource_path("icons/home-regular-24.png"))
student_light = PhotoImage(file=resource_path("icons/user-white.png"))
wallet_light = PhotoImage(file=resource_path("icons/wallet-regular-24.png"))
search_light = PhotoImage(file=resource_path("icons/search-regular-24.png"))
search_dark = PhotoImage(file=resource_path("icons/search-dark-24.png"))
export_light = PhotoImage(file=resource_path("icons/export-regular-24.png"))
delete_icon = PhotoImage(file=resource_path("icons/trash-regular-36.png")).subsample(2, 2)
edit_icon = PhotoImage(file=resource_path("icons/edit-solid-36.png"))
open_icon = PhotoImage(file=resource_path("icons/door-open-solid-24.png"))
add_icon = PhotoImage(file=resource_path("icons/plus-regular-24.png"))
calendar_icon = PhotoImage(file=resource_path('icons/calendar-regular-24.png'))
name_icon = PhotoImage(file=resource_path('icons/user-circle-regular-24.png'))
details_icon = PhotoImage(file=resource_path('icons\menu-regular-24.png'))
expenditure_icon = PhotoImage(file=resource_path('icons\wallet-gray.png'))



tb.Button(nav_frame, text="Home", bootstyle=SUCCESS, image=home_dark, compound=tk.LEFT, command=homepage, style="but.success.TButton").pack(fill=X, pady=5)
tb.Button(nav_frame, text="Students", bootstyle=SUCCESS, image=student_light, compound=tk.LEFT, command=students_page, style="but.success.TButton").pack(fill=X, pady=5)
tb.Button(nav_frame, text="Incomings Table", bootstyle=SUCCESS, image=wallet_light, compound=tk.LEFT, command=incomings_page, style="but.success.TButton").pack(fill=X, pady=5)
tb.Button(nav_frame, text="Search Student", bootstyle=SUCCESS, image=search_light, compound=tk.LEFT, command=search_page, style="but.success.TButton").pack(fill=X, pady=5)
tb.Button(nav_frame, text="Export Report", bootstyle=SUCCESS, image=export_light, compound=tk.LEFT, command=export_page, style="but.success.TButton").pack(fill=X, pady=5)


homepage()

root.mainloop()

