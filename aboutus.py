import tkinter as tk
from tkinter import scrolledtext

def about_window():
    root = tk.Tk()
    root.title("About Us")
    root.geometry("700x500")
    root.configure(bg="#f4f4f4")  # Light background color

    # Header Frame
    header = tk.Frame(root, bg="#08b9cb", height=60)
    header.pack(fill="x")

    header_label = tk.Label(header, text="About Us", 
                            font=("Arial", 18, "bold"), bg="#08b9cb", fg="white", padx=20)
    header_label.pack(pady=15)

    # About Us Text
    about_text = """\
Welcome to the Employee Management System!

Our system is designed to streamline employee record management, making it easy to add, update, and track employees efficiently.

Our Mission
To provide a simple, efficient, and user-friendly platform for managing employee records with accuracy and security.

Key Features
✔ Secure employee data storage  
✔ Easy data entry and retrieval  
✔ Modern and user-friendly interface  
✔ Compliance with industry standards  

Our Team
We are a dedicated team of developers committed to delivering quality software solutions. Our goal is to make employee management hassle-free and reliable.

Contact Us
📧 Email: abhishekjaiswar224@gmail.com
📧 Email: tanishkajogle@gmail.com
📧 Email: kiranlondhe@gmail.com
🌐 Website: https://www.mctrgit.ac.in
📍 Address: Rajiv Gandhi institute of Technology versova link road Andheri west mumbai 400053 

Thank you for choosing our Employee Management System!
"""

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), bg="white", fg="black")
    text_area.insert(tk.END, about_text)
    text_area.config(state=tk.DISABLED, padx=10, pady=10)
    text_area.pack(padx=20, pady=10, fill="both", expand=True)

    # Stylish Close Button
    close_button = tk.Button(root, text="Close", font=("Arial", 12, "bold"), bg="#ff5757", fg="white",
                             padx=20, pady=5, borderwidth=0, relief="flat", command=root.destroy)
    close_button.pack(pady=15)
    close_button.configure(cursor="hand2")  # Hand cursor effect

    root.mainloop()

if __name__ == "__main__":
    about_window()
