import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import io
import base64

class PayrollSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll System")
        self.root.geometry("900x600")
        self.root.configure(bg="#d8ffd8")
        
        # Define colors
        self.bg_color = "#d8ffd8"  # Light green background
        self.header_color = "#008000"  # Dark green for headers
        self.button_color = "#008000"  # Dark green for buttons
        self.text_color = "white"  # White text for buttons and headers
        self.border_color = "#4ca64c"  # Medium green for borders
        
        # Create the main layout
        self.create_header()
        self.create_content_area()
        self.create_footer()
    
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=80)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create money bag icon
        money_bag = self.create_money_bag_icon()
        icon_label = tk.Label(header_frame, image=money_bag, bg=self.bg_color)
        icon_label.image = money_bag  # Keep a reference
        icon_label.pack(side=tk.LEFT, padx=10)
        
        # Payroll System text
        title_frame = tk.Frame(header_frame, bg=self.bg_color)
        title_frame.pack(side=tk.LEFT)
        
        p_label = tk.Label(title_frame, text="P", font=("Arial", 36, "bold"), fg="#4ca64c", bg=self.bg_color)
        p_label.pack(side=tk.LEFT)
        
        ayroll_label = tk.Label(title_frame, text="AYROLL", font=("Arial", 36, "bold"), fg="#444444", bg=self.bg_color)
        ayroll_label.pack(side=tk.LEFT)
        
        s_label = tk.Label(title_frame, text="S", font=("Arial", 36, "bold"), fg="#4ca64c", bg=self.bg_color)
        s_label.pack(side=tk.LEFT, padx=(20, 0))
        
        ystem_label = tk.Label(title_frame, text="YSTEM", font=("Arial", 36, "bold"), fg="#444444", bg=self.bg_color)
        ystem_label.pack(side=tk.LEFT)
    
    def create_content_area(self):
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        sidebar_frame = tk.Frame(content_frame, width=180, bg=self.bg_color, bd=1, relief=tk.SOLID)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)  # Prevent shrinking
        
        # Welcome header in sidebar
        welcome_label = tk.Label(sidebar_frame, text="Welcome to system", bg=self.header_color, 
                                fg=self.text_color, font=("Arial", 10, "bold"), padx=10, pady=5)
        welcome_label.pack(fill=tk.X)
        
        # Sidebar buttons
        sidebar_buttons = [
            "ADD CLASS", "ADD Employee", "Employee Report", "Leave", 
            "Salary", "Salary Report", "Year wise Report", 
            "Admin Login", "Change Password", "LogOut"
        ]
        
        for button_text in sidebar_buttons:
            button = tk.Button(sidebar_frame, text=button_text, bg=self.bg_color, 
                              fg="dark green", font=("Arial", 10, "bold"), bd=1, 
                              relief=tk.SOLID, padx=10, pady=8, anchor="w",
                              activebackground="#b8ffb8", width=20)
            button.pack(fill=tk.X)
        
        # Main form area
        form_frame = tk.Frame(content_frame, bg=self.bg_color)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Generate Salary header
        header_label = tk.Label(form_frame, text="Generate Salary", bg=self.header_color, 
                               fg=self.text_color, font=("Arial", 10, "bold"), padx=10, pady=5)
        header_label.pack(fill=tk.X)
        
        # Form content
        form_content = tk.Frame(form_frame, bg=self.bg_color, padx=20, pady=10)
        form_content.pack(fill=tk.BOTH, expand=True)
        
        # First row - Month and Year
        row1 = tk.Frame(form_content, bg=self.bg_color)
        row1.pack(fill=tk.X, pady=5)
        
        month_label = tk.Label(row1, text="Month :", bg=self.bg_color, font=("Arial", 10))
        month_label.pack(side=tk.LEFT, padx=(0, 5))
        
        month_var = tk.StringVar(value="May")
        months = ["January", "February", "March", "April", "May", "June", 
                 "July", "August", "September", "October", "November", "December"]
        month_menu = ttk.Combobox(row1, textvariable=month_var, values=months, width=15, state="readonly")
        month_menu.pack(side=tk.LEFT)
        
        year_label = tk.Label(row1, text="Current Year :", bg=self.bg_color, font=("Arial", 10))
        year_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        year_entry = tk.Entry(row1, width=10, font=("Arial", 10))
        year_entry.insert(0, "2018")
        year_entry.pack(side=tk.RIGHT)
        
        # Second row - Class and Employee selection
        row2 = tk.Frame(form_content, bg=self.bg_color)
        row2.pack(fill=tk.X, pady=5)
        
        class_label = tk.Label(row2, text="Select Class :", bg=self.bg_color, font=("Arial", 10))
        class_label.pack(side=tk.LEFT, padx=(0, 5))
        
        class_var = tk.StringVar(value="Class I 6th Pay")
        classes = ["Class I 6th Pay", "Class II", "Class III"]
        class_menu = ttk.Combobox(row2, textvariable=class_var, values=classes, width=15, state="readonly")
        class_menu.pack(side=tk.LEFT)
        
        select_button = tk.Button(row2, text="SELECT", bg=self.button_color, fg=self.text_color, 
                                 font=("Arial", 9, "bold"), padx=10, pady=2)
        select_button.pack(side=tk.RIGHT)
        
        employee_var = tk.StringVar(value="Mehul Patel")
        employees = ["Mehul Patel", "John Doe", "Jane Smith"]
        employee_menu = ttk.Combobox(row2, textvariable=employee_var, values=employees, width=15, state="readonly")
        employee_menu.pack(side=tk.RIGHT, padx=(0, 10))
        
        employee_label = tk.Label(row2, text="Select Employee :", bg=self.bg_color, font=("Arial", 10))
        employee_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Employee info row (pink background)
        employee_info = tk.Frame(form_content, bg="#ffccff", padx=10, pady=5)
        employee_info.pack(fill=tk.X, pady=5)
        
        employee_text = tk.Label(employee_info, text="Employee Name : Mehul Patel , Account No : 552002010002", 
                                bg="#ffccff", font=("Arial", 10, "bold"))
        employee_text.pack(anchor="w")
        
        # Salary details area
        details_frame = tk.Frame(form_content, bg=self.bg_color)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column
        left_col = tk.Frame(details_frame, bg=self.bg_color)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Basic Pay
        basic_frame = tk.Frame(left_col, bg=self.bg_color)
        basic_frame.pack(fill=tk.X, pady=2)
        basic_label = tk.Label(basic_frame, text="Basic Pay :", bg=self.bg_color, font=("Arial", 10))
        basic_label.pack(side=tk.LEFT)
        basic_value = tk.Label(basic_frame, text="5800", bg=self.bg_color, font=("Arial", 10))
        basic_value.pack(side=tk.RIGHT)
        
        # Salary
        salary_frame = tk.Frame(left_col, bg=self.bg_color)
        salary_frame.pack(fill=tk.X, pady=2)
        salary_label = tk.Label(salary_frame, text="Salary :", bg=self.bg_color, font=("Arial", 10))
        salary_label.pack(side=tk.LEFT)
        salary_value = tk.Label(salary_frame, text="62000", bg=self.bg_color, font=("Arial", 10))
        salary_value.pack(side=tk.RIGHT)
        
        # Total Leave
        total_leave_frame = tk.Frame(left_col, bg=self.bg_color)
        total_leave_frame.pack(fill=tk.X, pady=2)
        total_leave_label = tk.Label(total_leave_frame, text="Total Leave :", bg=self.bg_color, font=("Arial", 10))
        total_leave_label.pack(side=tk.LEFT)
        total_leave_value = tk.Label(total_leave_frame, text="0", bg=self.bg_color, font=("Arial", 10))
        total_leave_value.pack(side=tk.RIGHT)
        
        # Approve Leave
        approve_leave_frame = tk.Frame(left_col, bg=self.bg_color)
        approve_leave_frame.pack(fill=tk.X, pady=2)
        approve_leave_label = tk.Label(approve_leave_frame, text="Approve Leave :", bg=self.bg_color, font=("Arial", 10))
        approve_leave_label.pack(side=tk.LEFT)
        approve_leave_value = tk.Label(approve_leave_frame, text="0", bg=self.bg_color, font=("Arial", 10))
        approve_leave_value.pack(side=tk.RIGHT)
        
        # Leave Deduction
        leave_deduction_frame = tk.Frame(left_col, bg=self.bg_color)
        leave_deduction_frame.pack(fill=tk.X, pady=2)
        leave_deduction_label = tk.Label(leave_deduction_frame, text="Leave Deduction :", bg=self.bg_color, font=("Arial", 10))
        leave_deduction_label.pack(side=tk.LEFT)
        leave_deduction_value = tk.Label(leave_deduction_frame, text="0", bg=self.bg_color, font=("Arial", 10))
        leave_deduction_value.pack(side=tk.RIGHT)
        
        # DA
        da_frame = tk.Frame(left_col, bg=self.bg_color)
        da_frame.pack(fill=tk.X, pady=5)
        da_label = tk.Label(da_frame, text="DA :", bg=self.bg_color, font=("Arial", 10))
        da_label.pack(side=tk.LEFT)
        da_entry = tk.Entry(da_frame, width=5, font=("Arial", 10))
        da_entry.insert(0, "2")
        da_entry.pack(side=tk.LEFT, padx=5)
        da_percent = tk.Label(da_frame, text="% 116", bg=self.bg_color, font=("Arial", 10))
        da_percent.pack(side=tk.LEFT)
        
        # HR
        hr_frame = tk.Frame(left_col, bg=self.bg_color)
        hr_frame.pack(fill=tk.X, pady=5)
        hr_label = tk.Label(hr_frame, text="HR :", bg=self.bg_color, font=("Arial", 10))
        hr_label.pack(side=tk.LEFT)
        hr_entry = tk.Entry(hr_frame, width=5, font=("Arial", 10))
        hr_entry.insert(0, "1")
        hr_entry.pack(side=tk.LEFT, padx=5)
        hr_percent = tk.Label(hr_frame, text="% 58", bg=self.bg_color, font=("Arial", 10))
        hr_percent.pack(side=tk.LEFT)
        
        # Right column
        right_col = tk.Frame(details_frame, bg=self.bg_color)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Travel Allowance
        travel_frame = tk.Frame(right_col, bg=self.bg_color)
        travel_frame.pack(fill=tk.X, pady=2)
        travel_label = tk.Label(travel_frame, text="TravelAllowance :", bg=self.bg_color, font=("Arial", 10))
        travel_label.pack(side=tk.LEFT)
        travel_entry = tk.Entry(travel_frame, width=10, font=("Arial", 10))
        travel_entry.insert(0, "600")
        travel_entry.pack(side=tk.RIGHT)
        
        # Medical Allowance
        medical_frame = tk.Frame(right_col, bg=self.bg_color)
        medical_frame.pack(fill=tk.X, pady=2)
        medical_label = tk.Label(medical_frame, text="MedicalAllowance :", bg=self.bg_color, font=("Arial", 10))
        medical_label.pack(side=tk.LEFT)
        medical_entry = tk.Entry(medical_frame, width=10, font=("Arial", 10))
        medical_entry.insert(0, "500")
        medical_entry.pack(side=tk.RIGHT)
        
        # Washing Allowance
        washing_frame = tk.Frame(right_col, bg=self.bg_color)
        washing_frame.pack(fill=tk.X, pady=2)
        washing_label = tk.Label(washing_frame, text="WashingAllowance :", bg=self.bg_color, font=("Arial", 10))
        washing_label.pack(side=tk.LEFT)
        washing_entry = tk.Entry(washing_frame, width=10, font=("Arial", 10))
        washing_entry.insert(0, "500")
        washing_entry.pack(side=tk.RIGHT)
        
        # Generate Salary button
        button_frame = tk.Frame(right_col, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=20)
        generate_button = tk.Button(button_frame, text="Generate Salary", bg=self.button_color, 
                                   fg=self.text_color, font=("Arial", 10, "bold"), padx=15, pady=5)
        generate_button.pack(anchor="center")
    
    def create_footer(self):
        # Footer frame
        footer_frame = tk.Frame(self.root, bg=self.header_color, height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Copyright text
        copyright_label = tk.Label(footer_frame, text="Copyrights 2018 @ Payroll System", 
                                  bg=self.header_color, fg=self.text_color, font=("Arial", 10))
        copyright_label.pack(pady=5)
    
    def create_money_bag_icon(self):
        # Create a money bag icon using PIL
        width, height = 50, 50
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw the bag (green circle)
        draw.ellipse((10, 10, 40, 40), fill="#4ca64c")
        
        # Draw the $ symbol
        draw.text((22, 18), "$", fill="#ffff00", font=None)
        
        # Draw the crown/top of the bag
        draw.polygon([(20, 10), (30, 10), (30, 5), (20, 5)], fill="#ffff00")
        
        # Convert to PhotoImage
        photo_image = ImageTk.PhotoImage(image)
        return photo_image

def main():
    root = tk.Tk()
    app = PayrollSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()

