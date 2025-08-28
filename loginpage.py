from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess
import mysql.connector
from connection import connect_db  # Import the database connection function

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

icon = PhotoImage(file="icon.png")
root.iconphoto(True, icon)

def sign_up():
    root.destroy()
    subprocess.run(["python", "signup.py"])

def login():
    username = user.get()
    password = code.get()

    db = connect_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        root.destroy()
        subprocess.run(["python", "home.py"])
    else:
        messagebox.showerror("Invalid", "Invalid username or password")

    db.close()

# UI Code
image = Image.open("login.png")
image = image.resize((925, 500), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo, bg='white')
label.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Login in', bg='white', fg='black', font=('Microsoft Yahei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    if user.get() == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    if code.get() == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11), show="*")
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=login).place(x=35, y=204)

label = Label(frame, text="Don't have an account?", fg="black", bg='white', font=('Microsoft Yahei UI Light', 9))
label.place(x=75, y=270)

signup = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='black', command=sign_up)
signup.place(x=215, y=270)

root.mainloop()

























# from tkinter import *
# from PIL import Image, ImageTk
# from tkinter import messagebox

# from tkinter import PhotoImage
# import subprocess

# root = Tk()
# root.title('Login')
# root.geometry('925x500+300+200')
# root.configure(bg="#fff")
# root.resizable(False, False)

# icon=PhotoImage(file="icon.png")
# root.iconphoto(True,icon)


# def sign_up():
#     root.destroy()  # Close main.py window
#     subprocess.run(["python", "signup.py"])
       

# def login():
#     username=user.get()
#     password=code.get()

#     if username=='admin' and password=='1234':
#         # print('login successfull')
#         # screen=Toplevel(root)
#         # screen.title("App")
#         # screen.geometry('925x500+300+200')
#         # screen.config(bg='white')


#         # label=Label(screen,text='Hello Everyone!',bg='#fff',font=('Microsoft Yahei UI Light',50,'bold'))
#         # label.pack(expand=TRUE)

#         # screen.mainloop()
#         # root.destroy()

#         # employee.open_employee_window()
#         root.destroy()  # Close main.py window
#         subprocess.run(["python", "home.py"])  # Open home.py


#     elif username!='admin' and password!='1234':
#         messagebox.showerror("Invalid","invalid credentials")

#     elif password!='1234':
#          messagebox.showerror("Invalid","invalid password")
#     elif username!='admin':
#          messagebox.showerror("Invalid","invalid username")

# image = Image.open("login.png")
# image = image.resize((925, 500), Image.Resampling.LANCZOS) 
# photo = ImageTk.PhotoImage(image)
# label = Label(root, image=photo, bg='white')
# label.place(x=0, y=0, relwidth=1, relheight=1) 


# frame=Frame(root,width=350,height=350,bg="white")
# frame.place(x=480,y=70)

# heading=Label(frame,text='Login in',bg='white',fg='black',font=('Microsoft Yahei UI Light',23,'bold'))
# heading.place(x=100,y=5)

# ##################username#########################

# def on_enter(e):
#     user.delete(0,'end')

# def on_leave(e):
#     name=user.get()
#     if name=='':
#         user.insert(0,'Username')

# user=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft Yahei UI Light',11))
# user.place(x=30,y=80)
# user.insert(0,'Username')
# user.bind('<FocusIn>',on_enter)
# user.bind('<FocusOut>',on_leave)

# Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

# ##################password#########################
# def on_enter(e):
#     code.delete(0,'end')

# def on_leave(e):
#     name=code.get()
#     if name=='':
#         code.insert(0,'password')

# code=Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft Yahei UI Light',11))
# code.place(x=30,y=150)
# code.insert(0,'Password')
# code.bind('<FocusIn>',on_enter)
# code.bind('<FocusOut>',on_leave)

# Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# ####################################################

# Button(frame,width=39,pady=7,text='Login in',bg='#57a1f8',fg='white',border=0,command=login).place(x=35,y=204)
# ##for sending for signup
# label=Label(frame,text="Don't have an account?",fg="black",bg='white',font=('Microsoft Yahei UI Light',9))
# label.place(x=75,y=270)

# signup=Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='black',command=sign_up)
# signup.place(x=215,y=270)

# root.mainloop()

