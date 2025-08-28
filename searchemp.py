import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader
import webbrowser
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO









# Function to connect to the database
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="9321675524@j",
            database="employee_management"  # Replace with your database name
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Function to search employees dynamically
def search_employee():
    query = search_var.get().lower()
    tree.delete(*tree.get_children())

    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    query_text = "SELECT emp_id, name, department FROM employees WHERE LOWER(name) LIKE %s OR emp_id LIKE %s"
    cursor.execute(query_text, (f"%{query}%", f"%{query}%"))
    employees = cursor.fetchall()
    
    for emp in employees:
        tree.insert("", "end", values=(emp[0], emp[1], emp[2]))

    conn.close()

# Function to handle dropdown actions
def handle_dropdown_action():
    selected_action = dropdown_var.get()
    if selected_action == "Print Data":
        print_employee_data()
    elif selected_action == "Generate Attendance Sheet":
        generate_attendance_pdf()
    else:
        messagebox.showwarning("Warning", "Please select a valid action.")

def go_to_home():
    root.destroy()
    subprocess.run(["python","home.py"])

# Function to print employee data
def print_employee_data():
    print("Printing Employee Data...")
    for child in tree.get_children():
        print(tree.item(child)["values"])  # Prints employee data to console (modify for real printing)

# Function to generate attendance sheet (dummy function)

def generate_attendance_pdf():
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT e.emp_id, e.name, e.email, e.contact, s.present_days
        FROM employees e
        JOIN employee_salary s ON e.emp_id = s.emp_id
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    if not employees:
        messagebox.showerror("Error", "No employee data found!")
        return

    pdf_path = "Attendance_Sheet.pdf"
    c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Add Logo
    try:
        logo = ImageReader("icon.png")
        c.drawImage(logo, 50, height - 100, width=100, height=50)
    except:
        print("Logo not found!")

    # Trademark
    c.setFont("Helvetica-Bold", 14)
    c.drawString(170, height - 80, "Company Trademark™")

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 120, "Employee Attendance Report")

    # Table Headers
    c.setFont("Helvetica-Bold", 12)
    headers = ["ID", "Name", "Email", "Contact", "Present", "Absent"]
    x_positions = [50, 120, 220, 350, 450, 520]
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], height - 160, header)

    # Table Data
    c.setFont("Helvetica", 10)
    y_position = height - 180
    total_present = 0
    total_absent = 0

    for emp in employees:
        emp_id, name, email, contact, present_days = emp["emp_id"], emp["name"], emp["email"], emp["contact"], emp["present_days"]
        absent_days = 30 - present_days  # Assuming a 30-day month

        total_present += present_days
        total_absent += absent_days

        row_data = [emp_id, name, email, contact, present_days, absent_days]
        for i, data in enumerate(row_data):
            c.drawString(x_positions[i], y_position, str(data))
        
        y_position -= 20  # Move to the next row

    # Generate Pie Chart for Attendance Overview
    chart_path = "attendance_chart.png"
    plt.figure(figsize=(2, 2))
    plt.pie([total_present, total_absent], labels=["Present", "Absent"], autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Overall Attendance")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    # Insert Chart into PDF
    c.drawImage(chart_path, 400, height - 400, width=150, height=150)

    c.save()

    # Open PDF after saving
    webbrowser.open(pdf_path)
    messagebox.showinfo("Success", "Attendance PDF Generated Successfully!")

    # Cleanup image file
    os.remove(chart_path)





def generate_employee_pdf(emp_id):
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM employees WHERE emp_id = %s"
    cursor.execute(query, (emp_id,))
    employee = cursor.fetchone()

    curse = conn.cursor(dictionary=True)
    sql = "SELECT * FROM employee_salary WHERE emp_id = %s"
    curse.execute(sql, (emp_id,))
    sal = curse.fetchone()

    conn.close()

    if not employee:
        messagebox.showerror("Error", "Employee not found!")
        return
    
    if not sal:
        messagebox.showerror("Error", "Salary details not found!")
        return

    pdf_path = f"{employee['name']}_Details.pdf"
    c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Add Logo
    try:
        logo = ImageReader("icon.png")
        c.drawImage(logo, 50, height - 100, width=100, height=50)
    except:
        print("Logo not found!")

    # Trademark
    c.setFont("Helvetica-Bold", 14)
    c.drawString(170, height - 80, "Company Trademark™")

    # Employee Details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, f"Employee Report: {employee['name']}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 170, f"Employee ID: {employee['emp_id']}")
    c.drawString(50, height - 190, f"Name: {employee['name']}")
    c.drawString(50, height - 210, f"Age: {employee['age']}")
    c.drawString(50, height - 230, f"Department: {employee['department']}")
    c.drawString(50, height - 250, f"Salary: {sal.get('salary', 'N/A')}")
    c.drawString(50, height - 270, f"Present Days: {sal['present_days']}")
    c.drawString(50, height - 290, f"Joining Date: {employee['doj']}")

    # Generate Pie Chart (Attendance)
    pie_chart_path = "attendance_pie.png"
    present_days = sal["present_days"]
    absent_days = 30 - present_days  # Assuming a 30-day month

    plt.figure(figsize=(2, 2))
    plt.pie([present_days, absent_days], labels=["Present", "Absent"], autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Attendance")
    plt.savefig(pie_chart_path, bbox_inches="tight")
    plt.close()

    # Insert Pie Chart in PDF
    c.drawImage(pie_chart_path, 350, height - 300, width=150, height=150)

    # Generate Progress Bar (Performance Score)
    perf_chart_path = "performance_bar.png"
    performance_score = sal.get("performance_score", 50)  # Default value

    fig, ax = plt.subplots(figsize=(2.5, 0.5))
    ax.barh(["Performance"], [performance_score], color="blue", height=0.3)
    ax.set_xlim(0, 100)
    plt.savefig(perf_chart_path, bbox_inches="tight")
    plt.close()

    # Insert Progress Bar in PDF
    c.drawImage(perf_chart_path, 350, height - 470, width=150, height=50)

    c.save()
    
    # Open the PDF after saving
    webbrowser.open(pdf_path)
    messagebox.showinfo("Success", "PDF Generated Successfully!")

    # Cleanup image files
    os.remove(pie_chart_path)
    os.remove(perf_chart_path)



# Function to print selected employee's data
def print_employee_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an employee to print.")
        return
    
    emp_id = tree.item(selected_item, "values")[0]
    generate_employee_pdf(emp_id)


# Create main window
root = tk.Tk()
root.title("Employee Search")
root.attributes('-fullscreen', True)
root.configure(bg="#222831")

# Exit button
exit_button = tk.Button(root, text="✖", command=go_to_home, font=("Arial", 14, "bold"),
                        bg="#FF2E63", fg="white", padx=10, pady=5, bd=0, relief=tk.FLAT)
exit_button.place(relx=0.98, rely=0.02, anchor="ne")

# Search frame with dropdown menu
# search_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
# search_frame.pack(pady=20, padx=20)
search_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
search_frame.pack(pady=20, padx=20)




# Canvas for underline effect
canvas = tk.Canvas(search_frame, height=2, bg="#FFFFFF", highlightthickness=0)
canvas.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))






# Search Bar (moved left and reduced width)
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 16), width=25, bg="#FFFFFF", bd=0, relief=tk.FLAT)
search_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)  # Added padding from right
search_entry.bind("<KeyRelease>", lambda event: search_employee())
# Adjust the line length dynamically based on search entry width
canvas.create_line(10, 1, search_entry.winfo_reqwidth() + 20, 1, fill="black", width=2)

# Load search icon
try:
    search_icon = Image.open("search_icon.png").resize((25, 25), Image.LANCZOS)
    search_icon = ImageTk.PhotoImage(search_icon)
except FileNotFoundError:
    print("Error: search_icon.png not found.")
    search_icon = None

# Search Button (moved closer)
search_button = tk.Button(search_frame, image=search_icon, command=search_employee, bg="#FFFFFF", bd=0, relief=tk.FLAT)
search_button.pack(side=tk.LEFT, padx=(5, 10))  # Padding between search bar and dropdown

# Dropdown menu for actions (separated with padding)
dropdown_var = tk.StringVar()
dropdown_options = ["Select Action", "Print Data", "Generate Attendance Sheet"]
dropdown_menu = ttk.Combobox(search_frame, textvariable=dropdown_var, values=dropdown_options, font=("Arial", 14), state="readonly", width=20)
dropdown_menu.current(0)  # Set default selection
dropdown_menu.pack(side=tk.LEFT, padx=(10, 5), pady=10)  # Added padding from left

# Action button (moved closer to dropdown)
action_button = tk.Button(search_frame, text="Execute", font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white", relief=tk.FLAT, command=handle_dropdown_action)
action_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

def handle_dropdown_action():
    selected_action = dropdown_var.get()
    if selected_action == "Print Data":
        print_employee_data()
    elif selected_action == "Generate Attendance Sheet":
        generate_attendance_pdf()
    else:
        messagebox.showwarning("Warning", "Please select a valid action.")




# Treeview frame
tree_frame = tk.Frame(root, bg="#222831")
tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Department"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Department", text="Department")

tree.pack(fill=tk.BOTH, expand=True)

# Load employees from the database
search_employee()

root.mainloop()
