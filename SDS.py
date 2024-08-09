import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from SDC_system import sdcExpenses
from tkinter import messagebox, simpledialog
import os
import sys
import pandas as pd
from datetime import datetime
import shutil
import ctypes
from ctypes import wintypes


sdc_expenses = sdcExpenses()


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


def validate_float(value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False


# Function to get the month name and year in the desired format
def get_month_year_string(date):
    return date.strftime("%B %Y")

def homepage():
    global main_frame, hovered_row

    def refresh_table(table_data):
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(table_data):
            table.insert("", "end", iid=index, values=(f'                   {entry["date"].strftime("%d/%m/%Y")}', entry["name"], entry["amount"], entry["expenditure"], entry["description"]))
         


    # Functions
    def on_open_details(index):
        def show_details():
            view_window = tb.Toplevel(root)
            center_window(root, view_window, 440, 400)
            # view_window.resizable(width=False, height=True)
            view_window.iconbitmap(resource_path('san_damian_logo.ico'))

            details_data = sdc_expenses.get_info(sorted_data[index]["expenseIDs"])
            # Convert date strings to datetime objects for sorting
            for item in details_data:
                item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")


            sf = ScrolledFrame(view_window, autohide=True)
            sf.pack(fill=BOTH, expand=True)

            view_frame = tb.Frame(sf)
            view_frame.pack(fill=X, expand=True, padx=30, pady=(0,20))
            tb.Label(view_frame, text="Expenditure Details", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).grid(row=0, column=1, columnspan=2)


            tb.Label(view_frame, image=calendar_icon).grid(row=1, column=0, sticky="w")
            tb.Label(view_frame, image=name_icon).grid(row=2, column=0, sticky="w")
            tb.Label(view_frame, image=expenditure_icon).grid(row=3, column=0, sticky="w")
            tb.Label(view_frame, text="Date", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=1, column=1, sticky="w")
            tb.Label(view_frame, text="Name", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=2, column=1, sticky="w")
            tb.Label(view_frame, text="Expenditure", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=3, column=1, sticky="w")
            tb.Label(view_frame, text="Amount", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=3, column=2, sticky="e")

            tb.Label(view_frame, text=details_data[0]['date'].strftime("%d/%m/%Y"), bootstyle=DARK, font=('Poppins', 11)).grid(row=1, column=2, sticky="e")
            tb.Label(view_frame, text=details_data[0]['name'], bootstyle=DARK, font=('Poppins', 11)).grid(row=2, column=2, sticky="e")

            i = 0
            for i, detail in enumerate(details_data):
                tb.Label(view_frame, text=detail['expenditure'], bootstyle=DARK, font=('Poppins', 11)).grid(row=4+i, column=1, sticky="w")
                tb.Label(view_frame, text=detail['amount'], bootstyle=DARK, font=('Poppins', 11)).grid(row=4+i, column=2, sticky="e")
                

            tb.Label(view_frame, text="-----------------------------------------", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=5+i, column=1, sticky="w", columnspan=2)
            tb.Label(view_frame, text="TOTAL", bootstyle=DARK, font=('Poppins', 12, 'bold')).grid(row=6+i, column=1, sticky="w")
            tb.Label(view_frame, text=sum(item['amount'] for item in details_data), bootstyle=DARK, font=('Poppins', 12, 'bold')).grid(row=6+i, column=2, sticky="e")
            tb.Label(view_frame, image=details_icon).grid(row=7+i, column=0, sticky="w")
            tb.Label(view_frame, text="Description", bootstyle=SECONDARY, font=('Poppins', 11)).grid(row=7+i, column=1, sticky="w")
            tb.Label(view_frame, text=details_data[0]['description'], bootstyle=DARK, font=('Poppins', 11), wraplength=340).grid(row=8+i, column=1, columnspan=3, sticky="w")


            # print(details_data)

            


        return show_details

    def on_delete(row_index):
        def confirm_delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):

                sdc_expenses.delete_expense(data[row_index]["expenseIDs"])
                
                homepage()
        return confirm_delete


    def edit_refresh(dd):
        expenditures = []
        amounts = []

        # get the date
        date_text = date.entry.get()

        if name_box.get() == "":
            messagebox.showerror("Error", "Please select a student", parent=add_expenses_window)
            return
        elif name_box.get() not in [student["name"] for student in sdc_expenses.display_students()]:
            sdc_expenses.add_student(name_box.get())
        name = name_box.get()

        for idx, combobox in enumerate(comboboxes):
            if combobox.get() == "":
                messagebox.showerror("Error", "Please select an expenditure", parent=add_expenses_window)
                return
            elif combobox.get() not in [entry["expenditure"] for entry in expenditures_data]:
                sdc_expenses.add_expenditure(combobox.get())
                
           
            expenditures.append(combobox.get())

        for idx, entry in enumerate(amount_boxes):
            if entry.get() == "":
                messagebox.showerror("Error", "Please enter an amount", parent=add_expenses_window)
                return
            amounts.append(entry.get())

        description = ""
        if description_box.get("1.0", tk.END) != "\n":
            description = description_box.get("1.0", tk.END)


        for i in range(len(expenditures)):
            sdc_expenses.edit_expenses(date_text, name, expenditures[i], amounts[i], description, dd[i]["expenseID"])
            

        # # Update table
        homepage()
        edit_window.destroy()
        


    def on_edit(row_index):
        def edit_entry():
            global expenses_frame, comboboxes, amount_boxes, expenditures_data, description_box, name_box, date, edit_window
            edit_window = tb.Toplevel(root)
            center_window(root, edit_window, 440, 620)
            edit_window.resizable(width=False, height=True)
            edit_window.iconbitmap(resource_path('san_damian_logo.ico'))

            details_data = sdc_expenses.get_info(sorted_data[row_index]["expenseIDs"])
            # Convert date strings to datetime objects for sorting
            for item in details_data:
                item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")


            sf = ScrolledFrame(edit_window, autohide=True)
            sf.pack(fill=BOTH, expand=True)

            new_expenses = tb.Frame(sf)
            new_expenses.pack(fill=X, expand=True, padx=60, pady=(0,20))


            tb.Label(new_expenses, text="Edit Expenses", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).pack(pady=(30,20))

           
            tb.Label(new_expenses, text="Date: ", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
            datevar = details_data[0]['date'].strftime("%d/%m/%Y")
            date_obj = datetime.strptime(datevar, "%d/%m/%Y")
            date = tb.DateEntry(new_expenses, bootstyle=SUCCESS, startdate=datetime(date_obj.year, date_obj.month, date_obj.day))
            date.pack(fill=X, expand=True, pady=(0, 15))
            date.entry.configure(font=('Poppins', 11), bootstyle=DARK)
            

            get_student = sdc_expenses.display_students()
            student_names = [student["name"] for student in get_student]
            tb.Label(new_expenses, text="Student:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
            name_box = tb.Combobox(new_expenses, values=student_names, bootstyle=DARK, font=('Poppins', 11))
            name_box.pack(fill=X, expand=True, pady=(0, 15))
            name_box.bind("<MouseWheel>", do_nothing)
            name_box.set(details_data[0]['name'])  

            # List to store combobox references
            comboboxes = []
            amount_boxes = []
            expenditures_data = sdc_expenses.get_expenditures()

            tb.Label(new_expenses, text="Expenditure:                                   Amount:", bootstyle="DARK", font=('Poppins', 11)).pack(fill=X)
            expenses_frame = tb.Frame(new_expenses)
            expenses_frame.pack(fill=X, expand=True)
            # List to store combobox references
            for i, detail in enumerate(details_data):
                add_expenditure()
                comboboxes[i].set(detail['expenditure'])
                amount_boxes[i].insert(0, detail['amount'])



            tb.Label(new_expenses, text="Description:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)

            description_box = tb.Text(new_expenses, height=2, font=('Poppins', 11))
            description_box.pack(fill=X, expand=True, pady=(0, 30))
            description_box.insert(tk.END, details_data[0]['description'])

            submit_button = tb.Button(new_expenses, text="Submit", bootstyle=SUCCESS, command=lambda: edit_refresh(details_data))
            submit_button.pack(fill=X)
                
            

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
        elif name_box.get() not in [student["name"] for student in sdc_expenses.display_students()]:
            sdc_expenses.add_student(name_box.get())
        name = name_box.get()

        for idx, combobox in enumerate(comboboxes):
            if combobox.get() == "":
                messagebox.showerror("Error", "Please select an expenditure", parent=add_expenses_window)
                return
            elif combobox.get() not in [entry["expenditure"] for entry in expenditures_data]:
                sdc_expenses.add_expenditure(combobox.get())
                
           
            expenditures.append(combobox.get())

        for idx, entry in enumerate(amount_boxes):
            if entry.get() == "":
                messagebox.showerror("Error", "Please enter an amount", parent=add_expenses_window)
                return
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


    def add_new_entry():
        global expenses_frame, comboboxes, expenditures_data, add_expenses_window, amount_boxes, description_box, name_box, date

        add_expenses_window = tb.Toplevel(root)
        center_window(root, add_expenses_window, 400, 620)
        add_expenses_window.resizable(width=False, height=True)
        add_expenses_window.iconbitmap(resource_path('san_damian_logo.ico'))

    
        sf = ScrolledFrame(add_expenses_window, autohide=True)
        sf.pack(fill=BOTH, expand=True)

        new_expenses = tb.Frame(sf)
        new_expenses.pack(fill=X, expand=True, padx=60, pady=(0,20))


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




    def update_highlights(dat, fil_incom):
        total_expenditures = sum(entry["amount"] for entry in dat)

        base_in = sum(entry["amount"] for entry in fil_incom)

        base_income.set(base_in)

        remaining_balance = base_in - total_expenditures
        base_income_label.config(text=f"Base Balance:    {base_income.get()}")
        remaining_balance_label.config(text=f"Remaining Balance:    {remaining_balance}")
        total_expenditures_label.config(text=f"Total Expenditures:     {total_expenditures}")


    def apply_filter_sort(month_var, sort_var, order_var):
        global sorted_data, filtered_income
        month = month_var.get()
        sort = sort_var.get()
        order = order_var.get()

        filtered_data = data
        filtered_income = incomings

        if month != "All":
            month_datetime = datetime.strptime(month, "%B %Y")
            filtered_data = [item for item in data if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]
            filtered_income = [item for item in incomings if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]

        if sort == "Name":
            sorted_data = sorted(filtered_data, key=lambda x: x["name"], reverse=(order == "Descending"))
        elif sort == "Amount":
            sorted_data = sorted(filtered_data, key=lambda x: x["amount"], reverse=(order == "Descending"))
        else:
            sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=(order == "Descending"))

        # load_data(treeview, sorted_data)
        refresh_table(sorted_data)
        update_highlights(sorted_data, filtered_income)
        # data = sorted_data

    def on_combobox_change(event, month_var, sort_var, order_var):
        apply_filter_sort(month_var, sort_var, order_var)

    
    

    # Data
    data = sdc_expenses.display_outgoings_table()
    # sorted_data = data

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


    month_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))
    sort_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))
    asc_desc_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))

    refresh_table(data)
    
    # sorted_data = data


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


    # base_income = tk.DoubleVar(value=50000)
    incomings = sdc_expenses.display_incoming_table()
    for item in incomings:
        item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

    base_income = tk.DoubleVar(value=sum(entry["amount"] for entry in incomings))
    base_income_label = tb.Label(highlight_frame, text=f"Base Balance: {base_income.get()}", bootstyle=DARK)
    base_income_label.pack(side=LEFT, pady=30)

    remaining_balance_label = tb.Label(highlight_frame, text="Remaining Balance: ", bootstyle=DARK)
    remaining_balance_label.pack(side=LEFT, padx=60)

    total_expenditures_label = tb.Label(highlight_frame, text="Total Expenditures: ", bootstyle=DARK)
    total_expenditures_label.pack(side=LEFT)



    update_highlights(data, incomings)
    apply_filter_sort(month_var, sort_var, order_var)   # Handles the initial sorting and filtering



def students_page():
    global main_frame

    # No-op function
    def do_nothing(event):
        return "break"
    

    def refresh_table(dat):
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(dat):
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
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?", parent=main_frame):
                # refresh_table()
                sdc_expenses.delete_student(studs_sorted_data[row_index]["studentID"])
                # print(data[row_index]["studentID"])
                students_page()
        return confirm_delete


    def on_edit(row_index):
        def edit_entry():
            # new_date = messagebox.showinfo("Edit Entry", "The system doesn't support editing entries yet")
            edit_name = simpledialog.askstring("Edit Student", "Enter Name: ",parent=main_frame, initialvalue=studs_sorted_data[row_index]["name"])
            if edit_name != "" and edit_name is not None:
                sdc_expenses.edit_student(studs_sorted_data[row_index]["studentID"], edit_name)
                print(edit_name)
                students_page()
            
        return edit_entry


    def add_new_entry():
        new_student = simpledialog.askstring("New Student", "Enter Name: ")
        # print(new_student)

        if new_student != "" and new_student is not None:

            if new_student.lower() in [student["name"].lower() for student in data]:
                messagebox.showerror("Error", "Student already exists", parent=main_frame)
                return
        
            sdc_expenses.add_student(new_student)
            students_page()
        


    def apply_filter_sort(sort_var, order_var):
        global studs_sorted_data
        sort = sort_var.get()
        order = order_var.get()

        if sort == "Id":
            studs_sorted_data = sorted(data, key=lambda x: x["studentID"], reverse=(order == "Descending"))
        else:
            studs_sorted_data = sorted(data, key=lambda x: x["name"], reverse=(order == "Descending"))

        refresh_table(studs_sorted_data)


    # Data
    data = sdc_expenses.display_students()

    # Main Frame
    main_frame.pack_forget()
    main_frame = tb.Frame(root)
    main_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Header Buttons
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill=X, pady=10, padx=30)

    # Sort By Id, Name
    sort_var = tk.StringVar()
    sort_menu = tb.Combobox(header_frame, textvariable=sort_var, values=["Id", "Name"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
    sort_menu.pack(side=LEFT, padx=20)
    sort_menu.current(0)

    order_var = tk.StringVar()
    asc_desc_menu = tb.Combobox(header_frame, textvariable=order_var, values=["Ascending", "Descending"], state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
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


    sort_menu.bind("<<ComboboxSelected>>", lambda e: apply_filter_sort(sort_var, order_var))
    asc_desc_menu.bind("<<ComboboxSelected>>", lambda e: apply_filter_sort(sort_var, order_var))

    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click

    refresh_table(data)
    apply_filter_sort(sort_var, order_var)   # Handles the initial sorting and filtering

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



def incomings_page():
    global main_frame

    # No-op function
    def do_nothing(event):
        return "break"


    def refresh_table(dat):
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(dat):
            table.insert("", "end", iid=index, values=(f'                  {entry["date"].strftime("%d/%m/%Y")}', entry["description"], f'          {entry["amount"]}'))
        
    
    def update_total(dat):
        total_amount_label.config(text=f'Total Amount: {sum(entry["amount"] for entry in dat)}')



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
                sdc_expenses.delete_income(inc_filtered_data[row_index]["incomeID"])
                incomings_page()
        return confirm_delete


    def edit_refresh(dat, date_box, description_box, amount_box):
        date_text = date_box.entry.get()

        description = ""
        if description_box.get("1.0", tk.END).strip() == "":
            messagebox.showerror("Error", "Please enter description", parent=edit_window)
            return
        description = description_box.get("1.0", tk.END).strip()


        if amount_box.get() == "":
            messagebox.showerror("Error", "Please enter an amount", parent=edit_window)
            return
        amount = amount_box.get()

        sdc_expenses.edit_income(dat["incomeID"], date_text, description, amount)
        incomings_page()
        edit_window.destroy()  
        # print(dat["incomeID"], date_text, description, amount)

    def on_edit(row_index):
        def edit_entry():
            global edit_window
            edit_window = tb.Toplevel(root)
            center_window(root, edit_window, 440, 500)
            edit_window.resizable(width=False, height=True)
            edit_window.iconbitmap(resource_path('san_damian_logo.ico'))

            sf = ScrolledFrame(edit_window, autohide=True)
            sf.pack(fill=BOTH, expand=True)

            edit_frame = tb.Frame(sf)
            edit_frame.pack(fill=X, expand=True, padx=60, pady=(0,20))

            tb.Label(edit_frame, text="Edit Incomings", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).pack(pady=(30,20))

            tb.Label(edit_frame, text="Date: ", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
            datevar = inc_filtered_data[row_index]['date'].strftime("%m/%d/%Y")
            date_obj = datetime.strptime(datevar, "%m/%d/%Y")
            date = tb.DateEntry(edit_frame, bootstyle=SUCCESS, startdate=datetime(date_obj.year, date_obj.month, date_obj.day))
            date.pack(fill=X, expand=True, pady=(0, 15))
            date.entry.configure(font=('Poppins', 11), bootstyle=DARK)

            tb.Label(edit_frame, text="Description:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)

            description_box = tb.Text(edit_frame, height=2, font=('Poppins', 11))
            description_box.pack(fill=X, expand=True, pady=(0, 15))
            description_box.insert(tk.END, inc_filtered_data[row_index]['description'])

            vcmd = (edit_frame.register(validate_float), '%P')

            tb.Label(edit_frame, text="Amount:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
            amount_box = tb.Entry(edit_frame, bootstyle=DARK, font=('Poppins', 11), width=7, validate='key', validatecommand=vcmd)
            amount_box.pack(fill=X, expand=True, pady=(0, 30))
            amount_box.insert(0, inc_filtered_data[row_index]['amount'])

            submit_button = tb.Button(edit_frame, text="Submit", bootstyle=SUCCESS, command=lambda: edit_refresh(inc_filtered_data[row_index], date, description_box, amount_box))
            submit_button.pack(fill=X)
            
        return edit_entry


    def refresh(date, description_box, amount_entry):

        # get the date
        date_text = date.entry.get()

        # get the description
        if description_box.get("1.0", tk.END) == "\n":
            messagebox.showerror("Error", "Please enter description", parent=add_expenses_window)
            return
        description = description_box.get("1.0", tk.END)

        # get the amount
        if amount_entry.get() == "":
            messagebox.showerror("Error", "Please enter an amount", parent=add_expenses_window)
            return
        amount = amount_entry.get()

        sdc_expenses.add_income(date_text, description, amount)

        # Update table
        incomings_page()
        add_expenses_window.destroy()
        add_new_entry()


    def add_new_entry():
        global add_expenses_window
        add_expenses_window = tb.Toplevel(root)
        center_window(root, add_expenses_window, 400, 500)
        add_expenses_window.resizable(width=False, height=True)
        add_expenses_window.iconbitmap(resource_path('san_damian_logo.ico'))
        sf = ScrolledFrame(add_expenses_window, autohide=True)
        sf.pack(fill=BOTH, expand=True)


        new_expenses = tb.Frame(sf)
        new_expenses.pack(fill=X, expand=True, padx=60, pady=(0,20))


        tb.Label(new_expenses, text="Add Income", bootstyle=SUCCESS, font=('Poppins', 25, 'bold')).pack(pady=(30,20))
        
        tb.Label(new_expenses, text="Date: ", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)
        date = tb.DateEntry(new_expenses, bootstyle=SUCCESS)  
        date.pack(fill=X, expand=True, pady=(0, 15))
        date.entry.configure(font=('Poppins', 11), bootstyle=DARK)

        tb.Label(new_expenses, text="Description:", bootstyle=DARK, font=('Poppins', 11)).pack(fill=X)

        description_box = tb.Text(new_expenses, height=2, font=('Poppins', 11))
        description_box.pack(fill=X, expand=True, pady=(0, 15))

        tb.Label(new_expenses, text="Amount:", bootstyle="DARK", font=('Poppins', 11)).pack(fill=X)
        vcmd = (new_expenses.register(validate_float), '%P')
        amount_entry = tb.Entry(new_expenses, bootstyle=DARK, font=('Poppins', 11), validate='key', validatecommand=vcmd)
        amount_entry.pack(fill=X, expand=True, pady=(0, 15))

        submit_button = tb.Button(new_expenses, text="Submit", bootstyle=SUCCESS, command=lambda: refresh(date, description_box, amount_entry))
        submit_button.pack(fill=X)


    def apply_filter(month_var):
        global inc_filtered_data
        month = month_var.get()
        inc_filtered_data = data

        if month != "All":
            month_datetime = datetime.strptime(month, "%B %Y")
            inc_filtered_data = [item for item in data if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]

        refresh_table(inc_filtered_data)
        update_total(inc_filtered_data)



    # Data
    data = sdc_expenses.display_incoming_table()
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

    # Sort Month
    unique_months = list(set([get_month_year_string(item["date"]) for item in data]))
    unique_months.sort(key=lambda date: datetime.strptime(date, "%B %Y"))

    month_var = tk.StringVar()
    month_menu = tb.Combobox(header_frame, textvariable=month_var, values=["All"] + unique_months, state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
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
    table.column("date", anchor="w")
    table.column("description", width=500)
    # table.column("amount", width=20)


    month_menu.bind("<<ComboboxSelected>>", lambda e: apply_filter(month_var))


    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click

    

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
    
    
    total_amount = tk.DoubleVar(value=sum(entry["amount"] for entry in data))
    total_amount_label = tb.Label(highlight_frame, text=f"Total Amount:  {total_amount.get()}", bootstyle=DARK)
    total_amount_label.pack(side=LEFT, pady=30)

    # refresh_table(data)
    apply_filter(month_var) 

    # update_total(inc_filtered_data)


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
        update_listbox(query, month_var)


    def update_listbox(query, month_v):
        # global results
        if query == "🔍Search Student...":
            query = ""
        results, total = sdc_expenses.display_student_expenses(query)
        for item in results:
            item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

        filtered_results = results
        month = month_v.get()
        if month != "All":
            month_datetime = datetime.strptime(month, "%B %Y")
            filtered_results = [item for item in results if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]


        total_amount_label.config(text=f"Total Amount:  {sum(entry['amount'] for entry in filtered_results)}")
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(filtered_results):
            table.insert("", "end", iid=index, values=(entry["date"].strftime("%d/%m/%Y"), entry["name"], entry["expenditure"], entry["amount"], entry["description"]))
        



    def get_name(event):
        select = table.focus()
        try:
            name = table.item(select, 'values')[1]
            # print(name)
            entry.delete(0, tk.END)
            entry.insert(0, name)
            update_listbox(name, month_var)
        except:
            pass



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
    data, _ = sdc_expenses.display_student_expenses("")
    for item in data:
        item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

    unique_months = list(set([get_month_year_string(item["date"]) for item in data]))
    unique_months.sort(key=lambda date: datetime.strptime(date, "%B %Y"))

    month_var = tk.StringVar()
    month_menu = tb.Combobox(header_frame, textvariable=month_var, values=["All"] + unique_months, state="readonly", bootstyle=SUCCESS, font=('Poppins', 10))
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

    month_menu.bind("<<ComboboxSelected>>", on_key_release)
    update_listbox("", month_var)





def export_page():
    global main_frame

    def export_report():
        # data = sdc_expenses.display_outgoings_table()
        for entry in sorted_data:
            entry['date'] = entry['date'].strftime("%d/%m/%Y")

        df = pd.DataFrame(sorted_data)
        df = df[["date", "name", "expenditure", "description", "amount"]]
        df.columns = df.columns.str.upper()


        writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report', startrow=4, startcol=1)
        workbook = writer.book
        worksheet = writer.sheets['report']

        # Add formats for styling
        header_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 10, 'bold': True, 'align': 'center','valign': 'vcenter', 'bg_color': '#B8D3EF', 'border': 1, 'border_color': '#ADADAD'})
        data_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 10,'align': 'center','valign': 'vcenter', 'border': 1, 'border_color': '#ADADAD'})
        data_left_align = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 10, 'align': 'left','valign': 'vcenter', 'border': 1, 'border_color': '#ADADAD'})
        # Create a format with the desired font properties
        title_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 22, 'bold': True,'valign': 'vcenter', 'font_color': '#595959', 'border_color': '#ADADAD'})
        currency_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 10,'num_format': '#,##0.00','valign': 'vcenter', 'border': 1, 'border_color': '#ADADAD'})
        total_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 13, 'bold': True, 'num_format': '₱     #,##0.00','valign': 'vcenter'})
        total_text_format = workbook.add_format({'font_name': 'Century Gothic', 'font_size': 9, 'valign': 'vcenter', 'align': 'right'})

        # write title
        worksheet.write('B3', month_var.get() + ' EXPENSES', title_format)
        worksheet.write('D4', 'TOTAL: ', total_text_format)



        # Apply formats to headers and data
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(4, col_num + 1, value, header_format)

        for row_num in range(len(df)):
            for col_num, value in enumerate(df.iloc[row_num]):
                if df.columns[col_num] in ["DESCRIPTION", "NAME", "EXPENDITURE"]:
                    worksheet.write(row_num + 5, col_num + 1, value, data_left_align)
                elif df.columns[col_num] == "AMOUNT":
                    worksheet.write(row_num + 5, col_num + 1, value, currency_format)
                else:
                    worksheet.write(row_num + 5, col_num + 1, value, data_format)
            worksheet.set_row(row_num + 5, 22)

        # Auto-adjust column width
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col))
            worksheet.set_column(i + 1, i + 1, column_len + 5)
        

        # Set the height of the header row
        worksheet.set_row(4, 35)  # Adjust the height as needed

        # Merge E4 and F4 and set the value to the sum of the "AMOUNT" column
        total_amount = df['AMOUNT'].sum()
        worksheet.merge_range('E4:F4', total_amount, total_format)

        writer.close()
        messagebox.showinfo("Export Report", "Report exported successfully")


    def refresh_table(table_data):
        for row in table.get_children():
            table.delete(row)
        for index, entry in enumerate(table_data):
            table.insert("", "end", iid=index, values=(f'                   {entry["date"].strftime("%d/%m/%Y")}', entry["name"], entry["amount"], entry["expenditure"], entry["description"]))
        


    # No-op function
    def do_nothing(event):
        return "break"






    def update_highlights(dat, fil_incom):
        total_expenditures = sum(entry["amount"] for entry in dat)

        base_in = sum(entry["amount"] for entry in fil_incom)

        base_income.set(base_in)

        # remaining_balance = base_income.get() - total_expenditures
        remaining_balance = base_in - total_expenditures
        base_income_label.config(text=f"Base Balance:    {base_income.get()}")
        remaining_balance_label.config(text=f"Remaining Balance:    {remaining_balance}")
        total_expenditures_label.config(text=f"Total Expenditures:     {total_expenditures}")


    def apply_filter_sort(month_var, sort_var, order_var):
        global sorted_data, filtered_income
        month = month_var.get()
        sort = sort_var.get()
        order = order_var.get()

        filtered_data = data
        filtered_income = incomings

        # filtered_data = sdc_expenses.display_outgoings_table()
        if month != "All":
            month_datetime = datetime.strptime(month, "%B %Y")
            filtered_data = [item for item in data if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]
            filtered_income = [item for item in incomings if item["date"].year == month_datetime.year and item["date"].month == month_datetime.month]

        if sort == "Name":
            sorted_data = sorted(filtered_data, key=lambda x: x["name"], reverse=(order == "Descending"))
        elif sort == "Amount":
            sorted_data = sorted(filtered_data, key=lambda x: x["amount"], reverse=(order == "Descending"))
        else:
            sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=(order == "Descending"))

        # load_data(treeview, sorted_data)
        refresh_table(sorted_data)
        update_highlights(sorted_data, filtered_income)
        # data = sorted_data

    def on_combobox_change(event, month_var, sort_var, order_var):
        apply_filter_sort(month_var, sort_var, order_var)



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


    month_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))
    sort_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))
    asc_desc_menu.bind("<<ComboboxSelected>>", lambda e: on_combobox_change(e, month_var, sort_var, order_var))

    refresh_table(data)
    
    # sorted_data = data


    table.pack(side=tk.LEFT, fill=BOTH, expand=True)


    # Binding mouse click events to do_nothing function
    table.bind("<Button-1>", do_nothing)  # Left click
    table.bind("<Button-3>", do_nothing)  # Right click


    # Create a vertical scrollbar
    vsb = tb.Scrollbar(table_frame, orient="vertical", command=table.yview)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Treeview to use the vertical scrollbar
    table.configure(yscrollcommand=vsb.set)

    

    # Highlights
    highlight_frame = tb.Frame(main_frame)
    highlight_frame.pack(fill=X, padx=50)

    # New Entry Button
    new_button = tb.Button(highlight_frame, text="Export Report", image=add_icon, compound=tk.LEFT, command=export_report, bootstyle="outline-secondary", style="secondary.Outline.TButton")
    new_button.pack(fill=X, pady=2)


    # base_income = tk.DoubleVar(value=50000)
    incomings = sdc_expenses.display_incoming_table()
    for item in incomings:
        item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")

    base_income = tk.DoubleVar(value=sum(entry["amount"] for entry in incomings))
    base_income_label = tb.Label(highlight_frame, text=f"Base Balance: {base_income.get()}", bootstyle=DARK)
    base_income_label.pack(side=LEFT, pady=30)


    remaining_balance_label = tb.Label(highlight_frame, text="Remaining Balance: ", bootstyle=DARK)
    remaining_balance_label.pack(side=LEFT, padx=60)

    total_expenditures_label = tb.Label(highlight_frame, text="Total Expenditures: ", bootstyle=DARK)
    total_expenditures_label.pack(side=LEFT)



    update_highlights(data, incomings)
    apply_filter_sort(month_var, sort_var, order_var)   # Handles the initial sorting and filtering


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


try:
    import winreg
except ImportError:
    import _winreg as winreg

user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

FONTS_REG_PATH = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'

HWND_BROADCAST   = 0xFFFF
SMTO_ABORTIFHUNG = 0x0002
WM_FONTCHANGE    = 0x001D
GFRI_DESCRIPTION = 1
GFRI_ISTRUETYPE  = 3

if not hasattr(wintypes, 'LPDWORD'):
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

user32.SendMessageTimeoutW.restype = wintypes.LPVOID
user32.SendMessageTimeoutW.argtypes = (
    wintypes.HWND,   # hWnd
    wintypes.UINT,   # Msg
    wintypes.LPVOID, # wParam
    wintypes.LPVOID, # lParam
    wintypes.UINT,   # fuFlags
    wintypes.UINT,   # uTimeout
    wintypes.LPVOID) # lpdwResult

gdi32.AddFontResourceW.argtypes = (
    wintypes.LPCWSTR,) # lpszFilename

# http://www.undocprint.org/winspool/getfontresourceinfo
gdi32.GetFontResourceInfoW.argtypes = (
    wintypes.LPCWSTR, # lpszFilename
    wintypes.LPDWORD, # cbBuffer
    wintypes.LPVOID,  # lpBuffer
    wintypes.DWORD)   # dwQueryType

def install_font(src_path):
    # copy the font to the Windows Fonts folder
    dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                            os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    # load the font in the current session
    if not gdi32.AddFontResourceW(dst_path):
        os.remove(dst_path)
        raise WindowsError('AddFontResource failed to load "%s"' % src_path)
    # notify running programs
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0,
                               SMTO_ABORTIFHUNG, 1000, None)
    # store the fontname/filename in the registry
    filename = os.path.basename(dst_path)
    fontname = os.path.splitext(filename)[0]
    # try to get the font's real name
    cb = wintypes.DWORD()
    if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                  GFRI_DESCRIPTION):
        buf = (ctypes.c_wchar * cb.value)()
        if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                      GFRI_DESCRIPTION):
            fontname = buf.value
    is_truetype = wintypes.BOOL()
    cb.value = ctypes.sizeof(is_truetype)
    gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb),
        ctypes.byref(is_truetype), GFRI_ISTRUETYPE)
    if is_truetype:
        fontname += ' (TrueType)'
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0,
                        winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)


# Create the main application window
root = tb.Window(themename="yeti")
root.geometry("1360x768")
root.title("San Damian Training Center")
root.iconbitmap(resource_path("san_damian_logo.ico"))


try:
    install_font(resource_path("fonts\Poppins-Regular.ttf"))
except WindowsError as e:
    pass
try:
    install_font(resource_path("fonts\Poppins-Bold.ttf"))
except WindowsError as e:
    pass

# Configure the fonts
style = tb.Style()
style.configure('danger.TLabel', font=('Poppins', 12))
style.configure('dark.TLabel', font=('Poppins', 12))
style.configure('TButton', font=('Poppins', 11))
style.configure('but.success.TButton', font=('Poppins', 12), anchor='w')
style.configure('secondary.Link.TButton', font=('Poppins', 10))
style.configure('Treeview.Heading', font=('Poppins', 12, 'bold'))
style.configure('Treeview', font=('Poppins', 12))
style.configure('Treeview', rowheight=30)
style.configure('secondary.Outline.TButton', font=('Poppins', 11))
style.configure('inverse-success.TLabel', font=('Poppins', 10))

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
san_damian_center_logo = PhotoImage(file=resource_path('icons\san_damian_logo.png')).subsample(4, 4)


tb.Button(nav_frame, bootstyle=SUCCESS, image=san_damian_center_logo, compound=tk.LEFT, command=homepage).pack(fill=X, pady=(0, 40))
tb.Button(nav_frame, text="    Home", bootstyle=SUCCESS, image=home_dark, compound=tk.LEFT, command=homepage, style="but.success.TButton").pack(fill=X, pady=3)
tb.Button(nav_frame, text="   Students", bootstyle=SUCCESS, image=student_light, compound=tk.LEFT, command=students_page, style="but.success.TButton").pack(fill=X, pady=3)
tb.Button(nav_frame, text="   Incomings", bootstyle=SUCCESS, image=wallet_light, compound=tk.LEFT, command=incomings_page, style="but.success.TButton").pack(fill=X, pady=3)
tb.Button(nav_frame, text="   Search Student", bootstyle=SUCCESS, image=search_light, compound=tk.LEFT, command=search_page, style="but.success.TButton").pack(fill=X, pady=3)
tb.Button(nav_frame, text="   Export Report", bootstyle=SUCCESS, image=export_light, compound=tk.LEFT, command=export_page, style="but.success.TButton").pack(fill=X, pady=3)
tb.Label(nav_frame, bootstyle="inverse-success", text="Information Technology Solutions").pack(side=BOTTOM)
tb.Label(nav_frame, bootstyle="inverse-success", text="ITWORKS - ").pack(side=BOTTOM)
tb.Label(nav_frame, bootstyle="inverse-success", text="all rights reserved").pack(side=BOTTOM)
tb.Label(nav_frame, bootstyle="inverse-success", text="Copyright © 2024").pack(side=BOTTOM)



homepage()

root.mainloop()

