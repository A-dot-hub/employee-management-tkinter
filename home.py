import tkinter as tk
from tkinter import PhotoImage, ttk ,Toplevel,messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import subprocess  # To run main.py
from salary import SalaryApp
from generateid import GenerateIDApp
import os


# some color codes used:  #2596be  #535c68  #f0f4fc

def open_main():
    root.destroy()  # Close home.py window
    subprocess.run(["python", "main.py"])  # Open main.py

def go_to_login():
    root.destroy()
    subprocess.run(["python","loginpage.py"])

def search_employee():
    root.destroy()
    subprocess.run(["python","searchemp.py"])

def open_terms():
    subprocess.Popen(["python", "terms.py"])

def open_aboutus():
    subprocess.Popen(["python", "aboutus.py"])

def open_feedback():
    subprocess.Popen(["python", "feedback.py"])


def open_reportpage():
    root.destroy()
    subprocess.run(["python", "report.py"])



def open_cal():
    class StylishCalculator:
        def __init__(self, root):
            self.root = root
            self.root.title("Calculator")
            self.root.configure(bg='#9e9e9e')  # Medium gray background
            self.root.geometry("320x450")  # Fixed size for better proportions
            
            
            # Add padding around the entire calculator
            frame = tk.Frame(root, bg='#9e9e9e', padx=10, pady=10, 
                            highlightbackground='#707070', highlightthickness=2)
            frame.pack(fill=tk.BOTH, expand=True)
            
            # Variable to store current expression
            self.current = ""
            
            # Create display with rounded corners and better styling
            display_frame = tk.Frame(frame, bg='#707070', padx=3, pady=3)
            display_frame.pack(fill=tk.X, padx=5, pady=10)
            
            self.display = tk.Entry(display_frame, width=20, font=('Helvetica', 22), 
                                bg='#e6ffe6', fg='#333333', justify='right',
                                relief=tk.FLAT, bd=0)
            self.display.pack(fill=tk.BOTH, ipady=15)
            
            # Button layout
            buttons_frame = tk.Frame(frame, bg='#9e9e9e')
            buttons_frame.pack(fill=tk.BOTH, expand=True)
            
            # Define button colors and styles
            button_style = {
                'width': 4, 
                'height': 2,
                'font': ('Helvetica', 14, 'bold'),
                'bd': 0,
                'relief': tk.RAISED,
                'padx': 10
            }
            
            # Button layout with colors
            button_data = [
                ('7', '#4d4d4d', 'white'), ('8', '#4d4d4d', 'white'), ('9', '#4d4d4d', 'white'), ('/', '#4d4d4d', 'white'),
                ('4', '#4d4d4d', 'white'), ('5', '#4d4d4d', 'white'), ('6', '#4d4d4d', 'white'), ('*', '#4d4d4d', 'white'),
                ('1', '#4d4d4d', 'white'), ('2', '#4d4d4d', 'white'), ('3', '#4d4d4d', 'white'), ('-', '#4d4d4d', 'white'),
                ('.', '#4d4d4d', 'white'), ('0', '#4d4d4d', 'white'), ('+', '#4d4d4d', 'white'), ('AC', '#4d4d4d', 'white')
            ]
            
            # Create and place buttons in a grid
            row, col = 0, 0
            self.buttons = {}
            
            for (text, bg, fg) in button_data:
                btn = tk.Button(buttons_frame, text=text, bg=bg, fg=fg, 
                            activebackground='#666666', activeforeground='white',
                            **button_style)
                btn.configure(command=lambda x=text: self.click(x))
                
                # Store button reference for hover effects
                self.buttons[text] = btn
                
                # Add hover event bindings
                btn.bind("<Enter>", lambda e, btn=btn: self.on_hover(btn, True))
                btn.bind("<Leave>", lambda e, btn=btn: self.on_hover(btn, False))
                
                btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            
            # Configure grid weights for responsive layout
            for i in range(4):
                buttons_frame.columnconfigure(i, weight=1)
            for i in range(4):
                buttons_frame.rowconfigure(i, weight=1)
            
            # Create SUM button with special styling
            sum_frame = tk.Frame(frame, bg='#9e9e9e', pady=5)
            sum_frame.pack(fill=tk.X)
            
            sum_btn = tk.Button(sum_frame, text="SUM", font=('Helvetica', 16, 'bold'),
                            bg='#004d99', fg='white', 
                            activebackground='#0066cc', activeforeground='white',
                            relief=tk.RAISED, bd=0, padx=10, pady=10,
                            command=self.calculate)
            sum_btn.pack(fill=tk.X, ipady=5)
            
            # Add hover event bindings for SUM button
            sum_btn.bind("<Enter>", lambda e, btn=sum_btn: self.on_hover(btn, True))
            sum_btn.bind("<Leave>", lambda e, btn=sum_btn: self.on_hover(btn, False))
        
        def on_hover(self, button, is_hovering):
            """Change button appearance on hover"""
            if is_hovering:
                # Darken the button slightly when hovering
                current_bg = button.cget("background")
                if current_bg == '#004d99':  # SUM button
                    button.configure(background='#005cb3')
                else:
                    button.configure(background='#666666')
            else:
                # Restore original color
                if button.cget("text") == "SUM":
                    button.configure(background='#004d99')
                else:
                    button.configure(background='#4d4d4d')
        
        def click(self, char):
            """Handle button clicks"""
            if char == 'AC':
                self.current = ""
                self.display.delete(0, tk.END)
            else:
                self.current += char
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.current)
        
        def calculate(self):
            """Calculate the result"""
            try:
                result = eval(self.current)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.current = str(result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current = ""

    # Create and run the application
    if __name__ == "__main__":
        root = tk.Tk()
        root.resizable(False, False)
        calculator = StylishCalculator(root)
        root.mainloop()
    
     

class EmployeeManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management")
        self.root.attributes('-fullscreen', True)  # Open in full screen
        self.root.configure(bg='#FFFDF7')  # Light cream background

        # Escape key to exit full screen
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Header
        header_frame = tk.Frame(root, bg='#FFFDF7', height=80)
        header_frame.pack(fill='x', padx=20, pady=10)

        # Title
        title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        title = tk.Label(header_frame, text="Employee Management", font=title_font, bg='#FFFDF7')
        title.pack(side='left')

        # Logout button
        # logout_btn = tk.Button(header_frame, text="Log Out", bg='#7FE7D4', relief='flat', padx=15, pady=5,command=go_to_login)
        # logout_btn.pack(side='right')

        # Log Out Button (Move to Left)
        logout_btn = tk.Button(header_frame, text="Log Out", bg='#7FE7D4', relief='flat', padx=15, pady=5, command=go_to_login)
        logout_btn.pack(side='left', padx=10)  # Aligns left with padding

        # Close (X) Button (Top Right Corner)
        close_btn = tk.Button(header_frame, text="✖", font=("Arial", 12, "bold"), bg="red", fg="white", 
                            relief="flat", padx=10, pady=5, command=root.quit)
        close_btn.pack(side='right', padx=10)  # Aligns to the right with padding
        close_btn.configure(cursor="hand2")  # Hand cursor effect


        # Main content area
        main_frame = tk.Frame(root, bg='#FFFDF7')
        main_frame.pack(fill='both', expand=True, padx=20)

        # Sidebar
        sidebar = tk.Frame(main_frame, bg='#FFFDF7', width=200)
        sidebar.pack(side='left', fill='y', padx=(0, 20))

        


        # Create individual buttons
        btn_employee_details = tk.Button(sidebar, text="Employee Details", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_main)
        btn_employee_details.pack(pady=5)

        btn_salary_details = tk.Button(sidebar, text="Salary Details", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=self.sala)
        btn_salary_details.pack(pady=5)

        btn_generate_id = tk.Button(sidebar, text="Generate ID", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=self.generate_id)
        btn_generate_id.pack(pady=5)

        btn_calculator = tk.Button(sidebar, text="Calculator", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_cal)
        btn_calculator.pack(pady=5)

        # btn_all_employee = tk.Button(sidebar, text="All Employee", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command='')
        # btn_all_employee.pack(pady=5)

        btn_search_employee = tk.Button(sidebar, text="Search Employee", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=search_employee)
        btn_search_employee.pack(pady=5)

        btn_report = tk.Button(sidebar, text="Report", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_reportpage)
        btn_report.pack(pady=5)

        btn_terms = tk.Button(sidebar, text="terms and conditions", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_terms)
        btn_terms.pack(pady=5)

        btn_aboutus = tk.Button(sidebar, text="About us", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_aboutus)
        btn_aboutus.pack(pady=5)

        btn_feedback = tk.Button(sidebar, text="feedback", bg='#7FE7D4', relief='flat', width=20, pady=10, cursor='hand2', command=open_feedback)
        btn_feedback.pack(pady=5)



       




        # Content area (gray placeholder with image background)
        self.content_area = tk.Frame(main_frame, bg='#CCCCCC')
        self.content_area.pack(side='left', fill='both', expand=True)

        # Add canvas for image background
        self.canvas = tk.Canvas(self.content_area, bg='#CCCCCC')
        self.canvas.pack(fill="both", expand=True)

        # Load and display the image
        self.load_background_image()


    def sala(self):
        # root.destroy()
        # subprocess.run(["python","salary.py"])
        subprocess.Popen(["python", "salary.py"]) 


    def generate_id(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=GenerateIDApp(self.new_win)


    def load_background_image(self):
        try:
            # Load image
            self.bg_image = Image.open("home.png")
            self.bg_image = self.bg_image.resize((1400, 799), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)

            # Place image on canvas
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            self.canvas.image = self.bg_photo  # Prevent garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")

    def exit_fullscreen(self, event=None):
        """Exit full-screen mode when Escape key is pressed"""
        self.root.attributes('-fullscreen', False)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagement(root)
    app.run()

