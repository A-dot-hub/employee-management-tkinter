import tkinter as tk
from tkinter import messagebox

def submit_feedback():
    rating = selected_rating.get()
    feedback_text = feedback_entry.get("1.0", tk.END).strip()
    
    if rating == 0:
        messagebox.showwarning("Warning", "Please select a star rating!")
        return
    if not feedback_text:
        messagebox.showwarning("Warning", "Please provide feedback in the text box.")
        return
    
    messagebox.showinfo("Thank You!", "Your feedback has been submitted successfully!")
    root.destroy()  # Close the feedback window after submission

def select_star(n):
    selected_rating.set(n)
    for i in range(5):
        if i < n:
            stars[i].config(text="★", fg="gold")  # Filled star
        else:
            stars[i].config(text="☆", fg="gray")  # Empty star

root = tk.Tk()
root.title("Feedback")
root.geometry("700x500")
root.configure(bg="#f4f4f4")  # Light background color

# Header Frame
header = tk.Frame(root, bg="#08b9cb", height=60)
header.pack(fill="x")

header_label = tk.Label(header, text="Feedback", 
                        font=("Arial", 18, "bold"), bg="#08b9cb", fg="white", padx=20)
header_label.pack(pady=15)

# Instructions Label
instructions = tk.Label(root, text="Please rate your experience and provide feedback below:",
                        font=("Arial", 12), bg="#f4f4f4", fg="black")
instructions.pack(pady=10)

# Star Rating System
selected_rating = tk.IntVar(value=0)
stars = []

stars_frame = tk.Frame(root, bg="#f4f4f4")
stars_frame.pack(pady=10)

for i in range(5):
    star_button = tk.Label(stars_frame, text="☆", font=("Arial", 30), fg="gray", cursor="hand2")
    star_button.bind("<Button-1>", lambda event, n=i+1: select_star(n))
    star_button.pack(side="left", padx=5)
    stars.append(star_button)

# Feedback Text Area
feedback_entry = tk.Text(root, wrap="word", width=70, height=8, font=("Arial", 12), bg="white", fg="black")
feedback_entry.pack(padx=20, pady=10, fill="both", expand=True)

# Submit Button
submit_button = tk.Button(root, text="Submit Feedback", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                          padx=20, pady=5, borderwidth=0, relief="flat", command=submit_feedback)
submit_button.pack(pady=10)
submit_button.configure(cursor="hand2")  # Hand cursor effect

# Close Button
close_button = tk.Button(root, text="Close", font=("Arial", 12, "bold"), bg="#ff5757", fg="white",
                         padx=20, pady=5, borderwidth=0, relief="flat", command=root.destroy)
close_button.pack(pady=10)
close_button.configure(cursor="hand2")  # Hand cursor effect

root.mainloop()
