import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

class GenerateIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee ID Generator")
        self.root.geometry("400x300")
        self.root.config(bg="#f5f5f5")

        # Labels & Entry Fields
        tk.Label(root, text="Enter Name:", font=("Calibri", 14), bg="#f5f5f5").pack(pady=5)
        self.entry_name = tk.Entry(root, font=("Calibri", 14))
        self.entry_name.pack(pady=5)

        tk.Label(root, text="Enter Contact:", font=("Calibri", 14), bg="#f5f5f5").pack(pady=5)
        self.entry_contact = tk.Entry(root, font=("Calibri", 14))
        self.entry_contact.pack(pady=5)

        tk.Label(root, text="Enter Department:", font=("Calibri", 14), bg="#f5f5f5").pack(pady=5)
        self.entry_department = tk.Entry(root, font=("Calibri", 14))
        self.entry_department.pack(pady=5)

        # Button to Generate Employee ID
        btn_generate = tk.Button(root, text="Generate ID", font=("Calibri", 14, "bold"), bg="#7FE7D4", fg="black", 
                                 command=self.assign_employee_id)
        btn_generate.pack(pady=10)

    def connect_db(self):
        """ Establish connection to MySQL database. """
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="9321675524@j",
            database="employee_management"
        )

    def generate_unique_id(self):
        """ Generate a unique Employee ID in the format EN12345. """
        return "EN" + str(random.randint(10000, 99999))

    def assign_employee_id(self):
        """ Assigns a unique Employee ID to an employee in the database. """
        name = self.entry_name.get().strip()
        contact = self.entry_contact.get().strip()
        department = self.entry_department.get().strip()

        if not name or not contact or not department:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        db = self.connect_db()
        cursor = db.cursor()

        # Check if employee exists
        cursor.execute("SELECT emp_id FROM employees WHERE name = %s AND contact = %s", (name, contact))
        result = cursor.fetchone()

        if result:
            if result[0]:  # If emp_id is already assigned
                cursor.execute("UPDATE employees SET department = %s WHERE name = %s AND contact = %s", 
                               (department, name, contact))
                db.commit()
                messagebox.showinfo("Info", f"Employee ID already exists: {result[0]}")
            else:
                # Generate a unique ID
                new_emp_id = self.generate_unique_id()

                # Ensure the ID is unique
                cursor.execute("SELECT COUNT(*) FROM employees WHERE emp_id = %s", (new_emp_id,))
                while cursor.fetchone()[0] > 0:  # If ID exists, regenerate
                    new_emp_id = self.generate_unique_id()

                # Update the employee record
                cursor.execute("UPDATE employees SET emp_id = %s WHERE name = %s AND contact = %s", 
                               (new_emp_id, name, contact))
                cursor.execute("UPDATE employees SET department = %s WHERE name = %s AND contact = %s", 
                               (department, name, contact))
                
                db.commit()
                messagebox.showinfo("Success", f"Employee ID assigned: {new_emp_id}")
        else:
            messagebox.showerror("Error", "Employee not found. Check Name and Contact.")

        cursor.close()
        db.close()

# Run Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = GenerateIDApp(root)
    root.mainloop()

