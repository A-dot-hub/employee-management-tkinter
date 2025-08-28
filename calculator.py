
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class StylishCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Calculator")
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