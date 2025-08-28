from tkinter import *
from tkinter import ttk, messagebox
import subprocess
from connection import connect_db

def open_employee_detail():
    global root, tv, name, age, doj, gender, email, contact, txtAddress
    root = Tk()
    root.title("Employee Details")
    root.geometry("1920x1080+0+0")
    root.config(bg="#2c3e50")
    root.state("zoomed")

    def go_home():
        root.destroy()
        subprocess.run(["python", "home.py"])

    def fetch_data():
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("SELECT id,emp_id,name,age,doj,email,department,gender,contact,address FROM employees")
        rows = cursor.fetchall()
        con.close()
        tv.delete(*tv.get_children())
        for row in rows:
            tv.insert("", END, values=row)

    def add_employee():
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("INSERT INTO employees (name, age, doj, email, gender, contact, address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name.get(), age.get(), doj.get(), email.get(), gender.get(), contact.get(), txtAddress.get("1.0", END)))
        con.commit()
        con.close()
        fetch_data()
        clear_fields()

    def update_employee():
        selected = tv.focus()
        if not selected:
            messagebox.showerror("Error", "Select an employee to update")
            return
        values = tv.item(selected, "values")
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("UPDATE employees SET name=%s, age=%s, doj=%s, email=%s, gender=%s, contact=%s, address=%s WHERE id=%s",
                       (name.get(), age.get(), doj.get(), email.get(), gender.get(), contact.get(), txtAddress.get("1.0", END), values[0]))
        con.commit()
        con.close()
        fetch_data()

    def delete_employee():
        selected = tv.focus()
        if not selected:
            messagebox.showerror("Error", "Select an employee to delete")
            return
        values = tv.item(selected, "values")
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("DELETE FROM employees WHERE id=%s", (values[0],))
        con.commit()
        con.close()
        fetch_data()

    def clear_fields():
        name.set("")
        age.set("")
        doj.set("")
        email.set("")
        gender.set("")
        contact.set("")
        txtAddress.delete("1.0", END)

    name, age, doj, email, gender, contact = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
    entries_frame = Frame(root, bg="#cccccc")
    entries_frame.pack(side=TOP, fill=X)
    Label(entries_frame, text="Enter Employee Details", font=("Calibri", 18, "bold"), bg="#cccccc").grid(row=0, column=0, padx=10, pady=20)
    Button(entries_frame, text="HOME", bg='#7FE7D4', command=go_home).grid(row=0, column=1, padx=10, pady=10, sticky="e")

    Label(entries_frame, text="Name", font=("Calibri", 16), bg="#cccccc").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30).grid(row=1, column=1, padx=10, pady=10, sticky="w")

    Label(entries_frame, text="Age", font=("Calibri", 16), bg="#cccccc").grid(row=1, column=2, padx=10, pady=10, sticky="w")
    Entry(entries_frame, textvariable=age, font=("Calibri", 16), width=30).grid(row=1, column=3, padx=10, pady=10, sticky="w")

    Label(entries_frame, text="D.O.J", font=("Calibri", 16), bg="#cccccc").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    Entry(entries_frame, textvariable=doj, font=("Calibri", 16), width=30).grid(row=2, column=1, padx=10, pady=10, sticky="w")

    Label(entries_frame, text="Email", font=("Calibri", 16), bg="#cccccc").grid(row=2, column=2, padx=10, pady=10, sticky="w")
    Entry(entries_frame, textvariable=email, font=("Calibri", 16), width=30).grid(row=2, column=3, padx=10, pady=10, sticky="w")

    Label(entries_frame, text="Gender", font=("Calibri", 16), bg="#cccccc").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=gender, state="readonly", values=("Male", "Female")).grid(row=3, column=1, padx=10, sticky="w")

    Label(entries_frame, text="Contact", font=("Calibri", 16), bg="#cccccc").grid(row=3, column=2, padx=10, pady=10, sticky="w")
    Entry(entries_frame, textvariable=contact, font=("Calibri", 16), width=30).grid(row=3, column=3, padx=10, sticky="w")

    Label(entries_frame, text="Address", font=("Calibri", 16), bg="#cccccc").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    txtAddress = Text(entries_frame, width=85, height=5, font=("Calibri", 16))
    txtAddress.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")



    btn_frame = Frame(entries_frame, bg="#cccccc")
    btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
    Button(btn_frame, command=add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white",bg="#7FE7D4", bd=0).grid(row=0, column=0)
    Button(btn_frame, command=update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"),fg="white", bg="#7FE7D4",bd=0).grid(row=0, column=1, padx=10)
    Button(btn_frame, command=delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"),fg="white", bg="#7FE7D4",bd=0).grid(row=0, column=2, padx=10)
    Button(btn_frame, command=clear_fields, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white",bg="#7FE7D4",bd=0).grid(row=0, column=3, padx=10)

   

   


    # Tree Frame
    tree_frame = Frame(root, bg="#ecf0f1")
    tree_frame.place(x=0, y=480, width=1980, height=520)

    # Scrollbars
    tree_scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL)
    tree_scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)

    # Treeview Style
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 14), rowheight=35)
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 16, 'bold'))

    # Treeview Widget
    tv = ttk.Treeview(
        tree_frame,
        columns=(1, 2, 3, 4, 5, 6, 7, 8),
        show='headings',
        yscrollcommand=tree_scroll_y.set,
        xscrollcommand=tree_scroll_x.set,
        style="mystyle.Treeview"
    )

    # Configure Scrollbars
    tree_scroll_y.config(command=tv.yview)
    tree_scroll_x.config(command=tv.xview)

    # Positioning Scrollbars
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x.pack(side=BOTTOM, fill=X)

    

    columns = ("ID","Employee Id", "Name", "Age", "D.O.J", "Email","Department", "Gender", "Contact", "Address")

    tv = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tv.heading(col, text=col, anchor="center")  # ✅ Reference by name instead of index
        tv.column(col, anchor="center", width=100)  # Optional: Set column width

    tv.pack(fill="both", expand=True)


    # Fetch Data Function (Assuming fetch_data() exists)
    fetch_data()


    root.mainloop()

if __name__ == "__main__":
    open_employee_detail()

