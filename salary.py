import subprocess
from tkinter import *
from tkinter import Toplevel, messagebox, ttk,Frame, Label, Button, X
from PIL import Image, ImageTk, ImageDraw
import os
import mysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import mysql.connector
from datetime import datetime

# EN25978 happy employee

class SalaryApp:
    def __init__(self, root):
        self.root = root
        self.connect_database()
        self.root.title("Employee Salary Details")
        self.root.geometry("950x650")  # Increased window size
        self.root.resizable(False, False)  # Fixed window size

    def connect_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="9321675524@j",
                database="employee_management"
            )   
            self.cursor = self.conn.cursor()
            print("Database Connection Successful!")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {str(e)}")
        
        # Try to load icon, create a default if not found
        try:
            icon = PhotoImage(file="icon.png")
            root.iconphoto(True, icon)
        except:
            # Create a simple icon if icon.png is not found
            icon_img = self.create_default_icon()
            root.iconphoto(True, icon_img)
        
            
        
        # Set background image or create a gradient background if image not found
        try:
            self.bg_image = Image.open("salbg1.png")
            self.bg_image = self.bg_image.resize((950, 650), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            bg_label = Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # Create a gradient background if image not found
            self.create_gradient_background()
        
        # Variables
        self.var_emp_id = StringVar()
        self.var_emp_name = StringVar()
        self.var_base_pay = StringVar()
        self.var_present = StringVar()
        self.var_medical = StringVar()
        self.var_conv = StringVar()
        self.var_p_f = StringVar()
        self.var_net_sal = StringVar()
        
        # Main Frame for Salary Details
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=50, y=30, width=850, height=580)

       
        
        # Title with gradient
        title_frame = Frame(main_frame, height=80, bg="#08b9cb")
        title_frame.pack(fill=X)

       
        
        # Create a canvas for the title with gradient
        title_canvas = Canvas(title_frame, height=80, bg="#08b9cb", highlightthickness=0)
        title_canvas.pack(fill=X)
        
        # Create gradient for title
        for i in range(80):
            # Gradient from darker to lighter blue
            color = f'#{int(8-(i/10)):02x}{int(185-(i/2)):02x}{int(203-(i/2)):02x}'
            title_canvas.create_line(0, i, 850, i, fill=color)
        
        title_canvas.create_text(425, 40, text="Employee Salary Details", 
                                font=("Helvetica", 28, "bold"), fill="white")
        
        # Content Frame with subtle gradient
        content_frame = Frame(main_frame, bg="white")
        content_frame.pack(fill=BOTH, expand=True)

        insert_btn = Button(content_frame, text="Save to Database", 
                    font=("Arial", 14, "bold"), command=self.insert_data, 
                    bg="#08b9cb", fg="white", relief=RAISED, padx=20, pady=10, bd=0)
        insert_btn.place(x=320, y=450)

        
        # Create a canvas for the content with gradient
        content_canvas = Canvas(content_frame, bg="white", highlightthickness=0)
        content_canvas.pack(fill=BOTH, expand=True)
        
        # Create gradient for content background
        for i in range(500):
            # Very subtle gradient
            color = f'#{int(240-(i/10)):02x}{int(250-(i/10)):02x}{int(255-(i/10)):02x}'
            content_canvas.create_line(0, i, 850, i, fill=color)
        
        # Add a decorative element
        content_canvas.create_oval(650, 50, 800, 200, fill="#08b9cb", outline="")
        content_canvas.create_oval(670, 70, 780, 180, fill="white", outline="")
        content_canvas.create_text(725, 125, text="SALARY\nDETAILS", font=("Arial", 14, "bold"), fill="#08b9cb")
        
        # Employee Information Section
        content_canvas.create_text(425, 50, text="Employee Information", 
                                  font=("Arial", 18, "bold"), fill="#08b9cb")
        content_canvas.create_line(250, 70, 600, 70, fill="#08b9cb", width=2)
        
        # Employee ID
        content_canvas.create_text(150, 100, text="Employee ID:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        emp_id_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_emp_id, 
                             bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                             highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        emp_id_entry.place(x=170, y=90)
        
        # Employee Name
        content_canvas.create_text(500, 100, text="Employee Name:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        emp_name_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_emp_name, 
                               bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                               highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        emp_name_entry.place(x=510, y=90)
        
        # Salary Details Section
        content_canvas.create_text(425, 150, text="Salary Components", 
                                  font=("Arial", 18, "bold"), fill="#08b9cb")
        content_canvas.create_line(250, 170, 600, 170, fill="#08b9cb", width=2)
        
        # Base Pay
        content_canvas.create_text(150, 220, text="Base Pay:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        base_pay_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_base_pay, 
                              bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                              highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        base_pay_entry.place(x=170, y=210)
        
        # Base Days
        content_canvas.create_text(500, 220, text="Base Days:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        present_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_present, 
                             bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                             highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        present_entry.place(x=520, y=210)
        
        # Medical
        content_canvas.create_text(150, 280, text="Medical:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        medical_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_medical, 
                             bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                             highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        medical_entry.place(x=170, y=270)
        
        # Conveyance
        content_canvas.create_text(500, 280, text="Conveyance:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        conv_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_conv, 
                          bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                          highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        conv_entry.place(x=520, y=270)
        
        # P.F
        content_canvas.create_text(150, 340, text="P.F:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        pf_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_p_f, 
                        bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                        highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        pf_entry.place(x=170, y=330)
        
        # Net Salary
        content_canvas.create_text(500, 340, text="Net Salary:", 
                                  font=("Arial", 14), fill="#333333", anchor="e")
        net_sal_entry = Entry(content_frame, font=("Arial", 14), textvariable=self.var_net_sal, 
                             bg="#f0f8ff", fg="#0066cc", relief=FLAT, highlightthickness=1,
                             highlightbackground="#08b9cb", highlightcolor="#08b9cb", width=12)
        net_sal_entry.place(x=520, y=330)
        
      

        back_button = Button(content_frame, text="Back", font=("Arial", 10, "bold"), bg="white", fg="black",
                     command=self.backhome)  # Replace with your function
        back_button.place(relx=1.0, x=-10, y=10, anchor="ne") 
        
        # Save Button
        save_btn = Button(content_frame, text="Save", 
                        font=("Arial", 14, "bold"), command=self.insert_data,
                        bg="#08b9cb", fg="white", relief=RAISED,
                        activebackground="#057a85", activeforeground="white",
                        padx=20, pady=10, bd=0)
        save_btn.place(x=320, y=400)


        # Generate Slip Button (Placed Next to Save Button)
        generate_btn = Button(content_frame, text="Generate Slip", 
                            font=("Arial", 14, "bold"), command=self.generate_slip,
                            bg="#08b9cb", fg="white", relief=RAISED,
                            activebackground="#057a85", activeforeground="white",
                            padx=20, pady=10, bd=0)
        generate_btn.place(x=450, y=400)  # Adjust x value to position it next to Save Button





        # Add a decorative footer
        footer_frame = Frame(main_frame, height=30, bg="#08b9cb")
        footer_frame.pack(side=BOTTOM, fill=X)
        footer_label = Label(footer_frame, text="© 2025 Employee Salary Management System", 
                            font=("Arial", 10), bg="#08b9cb", fg="white")
        footer_label.pack(pady=5)

    def backhome(self):
        root.destroy()
        # subprocess.run(["python","home.py"])
    
    def create_default_icon(self):
        # Create a simple icon
        icon_size = 64
        icon_image = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon_image)
        
        # Draw a blue circle
        draw.ellipse((4, 4, icon_size-4, icon_size-4), fill="#08b9cb")
        
        # Draw a dollar sign
        draw.text((icon_size//2-10, icon_size//2-15), "$", fill="white", font=None)
        
        # Convert to PhotoImage
        icon_photo = ImageTk.PhotoImage(icon_image)
        return icon_photo
    
    def create_gradient_background(self):
        # Create a gradient background
        bg_canvas = Canvas(self.root, width=950, height=650, highlightthickness=0)
        bg_canvas.place(x=0, y=0)
        
        # Create gradient
        for i in range(650):
            # Gradient from light blue to white
            r = int(8 + (i/650) * 247)
            g = int(185 + (i/650) * 70)
            b = int(203 + (i/650) * 52)
            color = f'#{r:02x}{g:02x}{b:02x}'
            bg_canvas.create_line(0, i, 950, i, fill=color)
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def insert_data(self):
        emp_id = self.var_emp_id.get()
        emp_name = self.var_emp_name.get()
        base_pay = self.var_base_pay.get()
        present_days = self.var_present.get()
        medical = self.var_medical.get()
        conveyance = self.var_conv.get()
        pf = self.var_p_f.get()
        net_salary = self.var_net_sal.get()

        if emp_id == "" or emp_name == "":
            messagebox.showerror("Error", "Please fill in all required fields!")
            return

        try:
            query = """INSERT INTO employee_salary 
                    (emp_id, emp_name, base_pay, present_days, medical, conveyance, pf, net_salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (emp_id, emp_name, base_pay, present_days, medical, conveyance, pf, net_salary)
            self.cursor.execute(query, values)
            self.conn.commit()

            messagebox.showinfo("Success", "Salary details inserted successfully!")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error inserting data: {str(e)}")



    def generate_slip(self):
        emp_id = self.var_emp_id.get()

        if emp_id == "":
            messagebox.showerror("Error", "Please enter an Employee ID!")
            return

        try:
            query = "SELECT emp_name, base_pay, present_days, medical, conveyance, pf, net_salary FROM employee_salary WHERE emp_id = %s"
            self.cursor.execute(query, (emp_id,))
            result = self.cursor.fetchone()

            que = "SELECT department FROM employees WHERE emp_id = %s"
            self.cursor.execute(que, (emp_id,))
            dept = self.cursor.fetchone()  # Returns tuple like ('HR',) or None

            if dept:
                departme = dept[0]  # Extract the value from tuple
            else:
                departme = "N/A"  # Assign a default value to prevent errors

           



            if result:
                emp_name, base_pay, present_days, medical, conveyance, pf, net_salary = result
                self.var_emp_name.set(emp_name)
                self.var_base_pay.set(base_pay)
                self.var_present.set(present_days)
                self.var_medical.set(medical)
                self.var_conv.set(conveyance)
                self.var_p_f.set(pf)
                self.var_net_sal.set(net_salary)
                if dept:
                   
                    messagebox.showinfo("Success", "Employee Data Retrieved!")

            else:
                messagebox.showerror("Not Found", "Employee not found in database!")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")

 


        try:
            emp_id = self.var_emp_id.get()
            emp_name = self.var_emp_name.get()
            base_pay = float(self.var_base_pay.get() or 0)
            present_days = int(self.var_present.get() or 0)
            medical = float(self.var_medical.get() or 0)
            conveyance = float(self.var_conv.get() or 0)
            pf = float(self.var_p_f.get() or 0)
            

            # Get the current date in the format "DD-MM-YYYY"
            generated_date = datetime.now().strftime("%d-%m-%Y")

            # Calculate net salary if not provided
            if not self.var_net_sal.get():
                daily_rate = base_pay / 30  # Assuming 30 days in a month
                basic_salary = daily_rate * present_days
                net_salary = basic_salary + medical + conveyance - pf
                self.var_net_sal.set(f"{net_salary:.2f}")
            else:
                net_salary = float(self.var_net_sal.get())

            slip_content = f"""
    ╔══════════════════════════════════════════════╗
    ║              EMPLOYEE SALARY SLIP            ║
    ╚══════════════════════════════════════════════╝

    Company Name: Employee Corporation, Bandra (W)
    Address: Corporate Tower, Floor 456 Mumbai - 400051

    Employee ID      : {emp_id}
    Employee Name    : {emp_name}
    Department       : {departme}
    Generated On     : {generated_date}

    ╔══════════════════════════════════════════════╗
    ║               SALARY COMPONENTS              ║
    ╚══════════════════════════════════════════════╝

    Total Present    : {present_days} days
    Base Pay         : Rs. {base_pay:.2f}
    Conveyance       : Rs. {conveyance:.2f}
    Medical          : Rs. {medical:.2f}
    PF Deduction     : Rs. {pf:.2f}

    ╔═══════════════════════════════════════════╗
    ║               PAYMENT SUMMARY             ║
    ╚═══════════════════════════════════════════╝

    Net Salary       : Rs. {net_salary:.2f}

    This is a computer-generated slip, not requiring any signature.
    """
            self.show_slip(slip_content)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")



   

    def print_pdf(self):
        emp_id = self.var_emp_id.get()
        if emp_id == "":
            messagebox.showerror("Error", "Please enter an Employee ID!")
            return

        filename = f"salary_slip_{emp_id}.pdf"

        # Create PDF
        c = canvas.Canvas(filename, pagesize=letter)

        # Add Company Logo (Replace 'logo.png' with your actual logo file)
        try:
            logo = ImageReader("logo.png")  # Ensure 'logo.png' is in the working directory
            c.drawImage(logo, 50, 720, width=80, height=50)  # Adjust position and size
        except:
            pass  # If logo is missing, continue without it

        # Add Company Name & Tagline
        c.setFont("Helvetica-Bold", 16)
        c.drawString(150, 750, "Employee Corporation Pvt. Ltd.")
        
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(150, 735, "Empowering Workforce Since 2005™")

        # Add Decorative Title Box
        c.setStrokeColorRGB(0, 0, 0)  # Black Border
        c.setFillColorRGB(0.8, 0.8, 0.8)  # Light Gray Fill
        c.rect(50, 700, 500, 30, fill=1)
        c.setFillColorRGB(0, 0, 0)  # Reset to black text
        c.setFont("Helvetica-Bold", 14)
        c.drawString(230, 710, "SALARY SLIP")

        # Add Salary Slip Information
        c.setFont("Helvetica", 12)
        generated_date = datetime.now().strftime("%d-%m-%Y")
        
        details = [
            ("Employee ID", emp_id),
            ("Employee Name", self.var_emp_name.get()),
            ("Base Pay", f"Rs. {self.var_base_pay.get()}"),
            ("Present Days", self.var_present.get()),
            ("Medical", f"Rs. {self.var_medical.get()}"),
            ("Conveyance", f"Rs. {self.var_conv.get()}"),
            ("PF Deduction", f"Rs. {self.var_p_f.get()}"),
            ("Net Salary", f"Rs. {self.var_net_sal.get()}"),
            ("Generated On", generated_date)
        ]

        y_position = 670  # Starting position for details
        for label, value in details:
            c.drawString(100, y_position, f"{label}: {value}")
            y_position -= 20  # Move down for the next line

        # Footer Section
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)  # Gray color for footer text
        c.drawString(200, 100, "Thank you for being part of our team!")
        c.drawString(180, 85, "This is a system-generated slip, no signature required.")

        # Save the PDF
        c.save()
        messagebox.showinfo("Success", f"Salary Slip saved as {filename}!")




    def save_pdf_to_db(self):
        emp_id = self.var_emp_id.get()
        if emp_id == "":
            messagebox.showerror("Error", "Please enter an Employee ID!")
            return
        
        filename = f"salary_slip_{emp_id}.pdf"
        
        try:
            with open(filename, "rb") as file:
                pdf_data = file.read()

            # Insert PDF into database using existing connection
            query = "INSERT INTO salary_slips (emp_id, pdf_file) VALUES (%s, %s)"
            self.cursor.execute(query, (emp_id, pdf_data))
            self.conn.commit()

            messagebox.showinfo("Success", "PDF saved to database successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not save to database: {str(e)}")





    def show_slip(self, slip_content):
        slip_window = Toplevel(self.root)
        slip_window.title("Salary Slip")
        slip_window.geometry("800x500")
        slip_window.resizable(False, False)
        
        # Center the slip window
        self.center_child_window(slip_window, 600, 500)
        
        # Create a frame with a border
        frame = Frame(slip_window, bd=2, relief=RIDGE)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = Frame(frame, bg="#08b9cb", height=50)
        header_frame.pack(fill=X)
        
        header_label = Label(header_frame, text="EMPLOYEE SALARY SLIP", 
                            font=("Arial", 16, "bold"), bg="#08b9cb", fg="white")
        header_label.pack(pady=10)
        
            
        
        # Buttons frame
        button_frame = Frame(frame, bg="white", height=40)
        button_frame.pack(fill=X)
        
        

        save_btn = Button(button_frame, text="Save", command=self.save_pdf_to_db,
                         font=("Arial", 12), bg="#08b9cb", fg="white", bd=0, padx=15)
        save_btn.pack(side=RIGHT, padx=10, pady=5)
        
        print_btn = Button(button_frame, text="Print", command=self.print_pdf,
                          font=("Arial", 12), bg="#08b9cb", fg="white", bd=0, padx=15)
        print_btn.pack(side=RIGHT, padx=10, pady=5)
        
        # Text area with scrollbar
        text_frame = Frame(frame)
        text_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        scroll_y = Scrollbar(text_frame, orient=VERTICAL)
        self.TextArea = Text(text_frame, font=("Courier New", 12), bg="white", 
                            fg="#333333", wrap=WORD, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.TextArea.yview)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        self.TextArea.pack(fill=BOTH, expand=True)
        
        # Insert content
        self.TextArea.insert(END, slip_content)
        self.TextArea.config(state=DISABLED)  # Make read-only
    
    def center_child_window(self, window, width, height):
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def save_record(self, slip_content):
        try:
            with open("salary_slip.txt", "w") as file:
                file.write(slip_content)
            messagebox.showinfo("Success", "Salary Slip Saved Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file: {str(e)}")

    def on_closing(self):
        if hasattr(self, 'conn'):
            self.cursor.close()
            self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = SalaryApp(root)
    # root.protocol("WM_DELETE_WINDOW", obj.on_closing)  # Handle window close
    root.protocol("WM_DELETE_WINDOW", obj.on_closing)
    root.mainloop()


     