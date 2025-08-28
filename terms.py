# import tkinter as tk
# from tkinter import scrolledtext

# def terms_window():
#     root = tk.Tk()
#     root.title("Terms & Conditions")
#     root.geometry("600x400")

#     tk.Label(root, text="Employee Management System - Terms & Conditions", 
#              font=("Arial", 12, "bold")).pack(pady=10)

#     terms_text = """\
# 1. Introduction
# Welcome to the Employee Management System. These Terms & Conditions govern the use of this software. By accessing or using the system, you agree to comply with these terms.

# 2. User Responsibilities
# - Users must provide accurate employee information.
# - Unauthorized access or modifications to the system are strictly prohibited.
# - Users are responsible for maintaining the confidentiality of their login credentials.

# 3. Data Privacy & Security
# - Employee data must be used solely for management purposes.
# - The system implements security measures to protect data, but users must also ensure responsible handling.
# - Any breach of security should be reported immediately.

# 4. Access & Usage
# - Only authorized personnel may access employee records.
# - The system should not be used for unlawful or unethical activities.
# - Modifications to employee records should be documented and justified.

# 5. Compliance
# - Users must comply with all company policies regarding employee data management.
# - Any misuse of the system may result in revocation of access and disciplinary action.

# 6. Limitation of Liability
# - The developers are not liable for any data loss due to improper usage.
# - Users should regularly back up critical data to avoid loss.

# 7. Amendments
# - These terms may be updated periodically.
# - Users will be notified of any significant changes.

# By using this system, you acknowledge that you have read and agreed to these Terms & Conditions.
# """

#     text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
#     text_area.insert(tk.END, terms_text)
#     text_area.config(state=tk.DISABLED)
#     text_area.pack(padx=10, pady=10)

#     close_button = tk.Button(root, text="Close", command=root.destroy)
#     close_button.pack(pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     terms_window()


import tkinter as tk
from tkinter import scrolledtext

def terms_window():
    root = tk.Tk()
    root.title("Terms & Conditions")
    root.geometry("700x500")
    root.configure(bg="#f4f4f4")  # Light background color

    # Header Frame
    header = tk.Frame(root, bg="#08b9cb", height=60)
    header.pack(fill="x")

    header_label = tk.Label(header, text="Terms & Conditions", 
                            font=("Arial", 18, "bold"), bg="#08b9cb", fg="white", padx=20)
    header_label.pack(pady=15)

    # Terms & Conditions Text
    terms_text = """\
1. Introduction
Welcome to the Employee Management System. These Terms & Conditions govern the use of this software. By accessing or using the system, you agree to comply with these terms.

2. User Responsibilities
- Users must provide accurate employee information.
- Unauthorized access or modifications to the system are strictly prohibited.
- Users are responsible for maintaining the confidentiality of their login credentials.

3. Data Privacy & Security
- Employee data must be used solely for management purposes.
- The system implements security measures to protect data, but users must also ensure responsible handling.
- Any breach of security should be reported immediately.

4. Access & Usage
- Only authorized personnel may access employee records.
- The system should not be used for unlawful or unethical activities.
- Modifications to employee records should be documented and justified.

5. Compliance
- Users must comply with all company policies regarding employee data management.
- Any misuse of the system may result in revocation of access and disciplinary action.

6. Limitation of Liability
- The developers are not liable for any data loss due to improper usage.
- Users should regularly back up critical data to avoid loss.

7. Amendments
- These terms may be updated periodically.
- Users will be notified of any significant changes.

By using this system, you acknowledge that you have read and agreed to these Terms & Conditions.
"""

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 12), bg="white", fg="black")
    text_area.insert(tk.END, terms_text)
    text_area.config(state=tk.DISABLED, padx=10, pady=10)
    text_area.pack(padx=20, pady=10, fill="both", expand=True)

    # Stylish Close Button
    close_button = tk.Button(root, text="Close", font=("Arial", 12, "bold"), bg="#ff5757", fg="white",
                             padx=20, pady=5, borderwidth=0, relief="flat", command=root.destroy)
    close_button.pack(pady=15)
    close_button.configure(cursor="hand2")  # Hand cursor effect

    root.mainloop()

if __name__ == "__main__":
    terms_window()

