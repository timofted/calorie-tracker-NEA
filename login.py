import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import subprocess
import sys
import json, os

SESSION_FILE = "session.json"
window = tk.Tk()
window.title("Log in")
window.config(bg = "#d7e9fa")

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_session(user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def on_close():
    clear_session()
    window.destroy()

def search():
    email=email_entry.get()
    password=password_entry.get()
    hashed_password=hash_password(password)
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Email, PasswordHash, User_ID
         FROM tblUsers
         WHERE Email = ? AND PasswordHash = ?"""
        
        cursor.execute(sql,(email,hashed_password))
        row=cursor.fetchone()
        
    if row:
        user_id=row[2]
        save_session(user_id)#save user id in a session to know which user is logged in

        window.destroy()
        print("Login Successful")
        subprocess.Popen([sys.executable, "menu.py"])
    else:
        messagebox.showerror(
            "Error",
            "Email or password incorrect!",
            parent=title)
        
def go_signup():
    window.destroy()
    subprocess.Popen([sys.executable, "signup.py"])

def go_login():
    window.destroy()
    subprocess.Popen([sys.executable, "login.py"])


state=tk.BooleanVar(value=False)

def hide():
    showing=state.get()
    if showing==True:
        password_button.config(text="Show")
        password_entry.config(show="*")
        state.set(False)
    if showing==False:
        password_button.config(text="Hide")
        password_entry.config(show="")
        state.set(True)

Heading = tk.Label(title, text = "Account login")
Heading.config(bg = "#d7e9fa", width = 15, font = ("Comic sans MS", 20), height = 1)
Heading.grid(column = 0, row = 0, columnspan = 4,pady=10)

Heading = tk.Label(title, text = "Enter email:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height = 1)
Heading.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Heading.grid(column = 0, row = 1, pady = 2, columnspan = 4)

email_entry = tk.Entry(title)
email_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32)
email_entry.grid(column = 0, row = 2, pady = 3, columnspan = 4, sticky="ew")

Heading = tk.Label(title, text = "Enter password:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height =1)
Heading.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Heading.grid(column = 0, row = 3, pady = 2, columnspan = 4)

password_entry = tk.Entry(title)
password_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32,show="*")
password_entry.grid(column = 0, row = 4, pady = 3, columnspan = 4, sticky="ew")

signupbutton = tk.Button(title, text = "Don't have an account?\n Sign up")
signupbutton.config(bg = "white", fg = "black", font = ("Comic sans MS", 14),\
                width = 12, height = 1,command=go_signup)
signupbutton.grid(column = 0, row = 5, pady = 8, columnspan = 4, sticky = "ew")

login_button = tk.Button(title, text = "Login")
login_button.config(bg = "#6279A8", fg = "white", font = ("Comic sans MS", 14),\
                width = 5, height = 1, command=search)
login_button.grid(column = 1, row = 6, pady = 2, columnspan = 2, sticky = "ew")

password_button = tk.Button(title, text = "Show")
password_button.config(bg = "white", fg = "black", font = ("Comic sans MS", 7),\
                width = 4, height = 1,command=hide)
password_button.grid(column = 4, row =4, pady = 2, columnspan = 1, sticky = "ew")



tk.mainloop()