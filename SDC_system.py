from prettytable import PrettyTable
import sqlite3


# Connect to database
conn = sqlite3.connect('sanDamian.db')
# Set the row factory to sqlite3.Row
conn.row_factory = sqlite3.Row
db = conn.cursor()


class sdcExpenses:
    def __init__(self):
        self.total_income = 50000
    
    def add_student(self, name):
        db.execute("INSERT INTO Students (name) VALUES (?)", (name,))
        conn.commit()

        print("Successfully added the student")


    def add_expenses(self, date, student_name, expenditure, amount, description):
        try:
            db.execute('''
            INSERT INTO Expenses (date, studentID, expenditureID, amount, description) 
                VALUES (
                    ?,
                    (SELECT studentID FROM Students WHERE name = ?),
                    (SELECT expenditureID FROM Expenditures WHERE expenditure = ?),
                    ?, ?
                )
        ''', (date, student_name, expenditure, amount, description))
            # Commit changes
            conn.commit()

        except Exception as e:
            print("Adding Expenses Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            print("Successfully added the expenses")
        
    

    def add_income(self, date, description, amount):
        try:
            db.execute('''
            INSERT INTO Incomes (date, description, amount)
            VALUES (?, ?, ?)
            ''', (date, description, amount))
            # Commit changes
            conn.commit()

        except Exception as e:
            print("Adding Income Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            print("Successfully added the income")
            

    def add_expenditure(self, expenditure):
        try:
            db.execute("INSERT INTO Expenditures (expenditure) VALUES (?)", (expenditure,))
            conn.commit()

        except Exception as e:
            print("Adding Expenditure Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            print("Successfully added the expenditure")


    def change_base_income(self, month, amount):
        self.total_income = amount
        

    def display_main_table(self):
        
        rows = db.execute('''
            SELECT date, description AS name, amount, 'IN' AS type 
            FROM Incomes UNION ALL 
                SELECT date, name, SUM(amount) AS amount, 'OUT' AS type 
                FROM Expenses, Students WHERE Expenses.studentID = Students.studentID 
                GROUP BY Expenses.studentID
                ORDER BY date DESC
        ''')

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]

        return result
        # Create PrettyTable object
        # table = PrettyTable()
        # table.field_names = rows[0]
        # for row in rows:
        #     record = row['date'], row['name'], row['amount'], row['type']
        #     table.add_row(record)

        # print(table)

        # total = db.execute("SELECT SUM(amount) AS total FROM Expenses")
        # total_expenses = total[0]['total']
        # remaining_balance = self.total_income - total_expenses
        # print("Total Expenses: ", total_expenses)
        # print("Remainning Balance: ", remaining_balance)


    def display_incoming_table(self):
        rows = db.execute("SELECT * FROM Incomes").fetchall()

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]
        # Create PrettyTable object
        # table = PrettyTable()
        # table.field_names = rows[0]
        # for row in rows:
        #     record = row['date'], row['description'], row['amount']
        #     table.add_row(record)

        # print(table)
        return result


    def display_outgoings_table(self):
        rows = db.execute('''
            SELECT GROUP_CONCAT(expenseID) AS expenseIDs, date, IFNULL(name, '') AS name, SUM(amount) AS amount, 
                GROUP_CONCAT(expenditure, ', ') AS expenditure, description
            FROM Expenses
            LEFT JOIN Students ON Expenses.studentID = Students.studentID
            LEFT JOIN Expenditures ON Expenses.expenditureID = Expenditures.expenditureID
            GROUP BY date, name
            ORDER BY date DESC
        ''').fetchall()

        
        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]
    

        return result
        # Create PrettyTable object
        # table = PrettyTable()
        # table.field_names = rows[0]
        # for row in rows:
        #     record = row['date'], row['name'], row['amount'], row['expenditure']
        #     table.add_row(record)

        # print(table)


    def display_student_expenses(self, name):
        rows = db.execute('''
            SELECT date, name, expenditure, amount, description 
            FROM Expenses, Students, Expenditures
            WHERE Expenses.studentID = Students.studentID
            AND Expenses.expenditureID = Expenditures.expenditureID
            AND name LIKE ?
        ''', (f'%{name}%',)).fetchall()

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]

        totals = db.execute('''
            SELECT SUM(amount) AS total_amount
            FROM Expenses, Students
            WHERE Expenses.studentID = Students.studentID
            AND name LIKE ?
        ''', (f'%{name}%',)).fetchall()

        total = [dict(total) for total in totals]

        total_amount = total[0]
        
        return result, total_amount['total_amount']



    def generate_monthly_report(self):
        pass

    def display_students(self):
        rows = db.execute("SELECT * FROM Students ORDER BY name ASC").fetchall()

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]
        return result
    

    def get_expenditures(self):
        rows = db.execute("SELECT expenditure FROM Expenditures ORDER BY expenditure ASC").fetchall()

        # Convert rows to a list of dictionaries
        result = [dict(row) for row in rows]
        return result


    def delete_student(self, name):
        try:
            db.execute("DELETE FROM Students WHERE studentID = ?", (name,))
            # Commit changes
            conn.commit()
        except Exception as e:
            print("Delete Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            # print("Successfully deleted the student")
            pass

    
    def delete_expense(self, expenseIDs):
        try:
            # db.execute('''
            # DELETE FROM Expenses
            # WHERE date = ?
            # AND studentID = (SELECT studentID FROM Students WHERE name = ?)
            # ''', (date, name))
            # conn.commit()
            # The string containing comma-separated integers

            # Split the string into a list of substrings
            ID_list = expenseIDs.split(',')
            
            for integer in ID_list:
                db.execute('''
                DELETE FROM Expenses
                WHERE expenseID = ?
                ''', (integer,))
                conn.commit()

        except Exception as e:
            print("Delete Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            # print("Successfully deleted the expense")
            pass
        

    def get_info(self, index):
        try:
            index_list = index.split(',')
            placeholders = ','.join('?' for _ in index_list)

            query = f'''
                SELECT *
                FROM Expenses
                LEFT JOIN Expenditures ON Expenses.expenditureID = Expenditures.expenditureID
                LEFT JOIN Students ON Expenses.studentID = Students.studentID
                WHERE expenseID IN ({placeholders})
            '''

            # Execute the query with the list of IDs
            rows = db.execute(query, index_list).fetchall()

            # rows = db.execute('''
            #     SELECT * FROM Expenses
            #     WHERE expenseID IN (?)
            # ''', (index,)).fetchall()
            result = [dict(row) for row in rows]
            return result
        
        except Exception as e:
            print("An Error occured: ", e)
            return None
    

    def edit_expenses(self, date, student_name, expenditure, amount, description, expenseID):
        try:
            db.execute('''
            UPDATE Expenses
            SET date = ?,
                studentID = (SELECT studentID FROM Students WHERE name = ?),
                expenditureID = (SELECT expenditureID FROM Expenditures WHERE expenditure = ?),
                amount = ?,
                description = ?
            WHERE expenseID = ?
            ''', (date, student_name, expenditure, amount, description, expenseID))
            conn.commit()

        except Exception as e:
            print("Edit Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            print("Successfully edited the expense")


    def edit_student(self, studentID, name):
        try:
            db.execute('''
            UPDATE Students
            SET name = ?
            WHERE studentID = ?
            ''', (name, studentID))
            conn.commit()

        except Exception as e:
            print("Edit Unsuccessful")
            print(f"An Error occured: {e}")
        else:
            print("Successfully edited the student")