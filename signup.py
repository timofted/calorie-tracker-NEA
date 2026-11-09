import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import sqlite3
import hashlib
import json, os
import sys
import subprocess
import time

current_time = int(time.time())
SESSION_FILE = "session.json"

window = tk.Tk()
window.title("Sign up")
window.config(bg = "#d7e9fa")

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None

def save_session(user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)


def validation():
    username=name_entry.get()
    email=email_entry.get()
    password=password_entry.get()
    height=height_entry.get()
    weight=weight_entry.get()
    gender=gender_option.get()
    age=age_entry.get()

    if username=='': #return if empty
         messagebox.showerror(
            title="Error",
            message="Username is missing!",
            parent=title  
        )
         return
    if not validate_email(email): #if not matching email
        messagebox.showerror(
            "Error",
            "Invalid email format! \n Contain '@' with text before and after \n No spaces \n Domain must have at least one dot",
            parent=title)
        return
    if validate_password(password)==False:
        messagebox.showerror(
            "Error",
            "Invalid password! \n Must have 8 characters \n Uppercase and lowercase letters \n Special characters",
            parent=title)
        return
    if validate_height(height)==False:
        messagebox.showerror(
            "Error",
            "Invalid height! \n Must be within a feasible range \n Must be an integer",
            parent=title)
        return
    if validate_weight(weight)==False:
        messagebox.showerror(
            "Error",
            "Invalid weight! \n Must be within a feasible range \n Must be a float/decimal number",
            parent=title)
        return
    if validate_age(age)==False:
        messagebox.showerror(
            "Error",
            "Invalid age! \n Please enter a correct age",
            parent=title)
        return

    hashed_password=hash_password(password)
    add_data(username,email,hashed_password,height,weight,gender,age,current_time)


    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])
    


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_data(username,email,hashed_password,height,weight,gender,age,time):
    #adds some data
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """   INSERT OR IGNORE INTO
                    	tblUsers
                    	(Username, Email, PasswordHash, Height, Weight, Gender, Age)
                    	VALUES
                    	(?,?,?,?,?,?,?)"""
                
        cursor.execute(sql,(username,email,hashed_password,height,weight,gender, age))


    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Email, User_ID
         FROM tblUsers
         WHERE Email = ?"""
        
        cursor.execute(sql,(email,))
        row=cursor.fetchone()
        
    user_id=row[1]  
    save_session(user_id)


    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """   INSERT OR IGNORE INTO
                    	tblWeight
                    	(User_ID, Weight, Time)
                    	VALUES
                    	(?,?,?)"""
        cursor.execute(sql,(user_id,weight,time))
    

def validate_email(email):
    #regex: uses a pattern to check email against a set criteria:
    #contain exactly one @ having text before and after
    #no spaces and domain having at least one dot.
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return(re.match(pattern, email))

def validate_password(password):
    #must have 8 characters
    #uppercase and lower case letters
    #special character
    formatted=True
    length=len(password)
    if bool(re.search(r'[a-z]',password)) == True and bool(re.search(r'[A-Z]',password))== True:
        formatted=True
    else:
        formatted=False
    if length <8:
        formatted=False
    if bool(re.search(r'[^a-zA-Z0-9]', password)) == False: #using regex patterns to check for special character
        formatted=False
    
    return formatted

def validate_height(height):
    formatted=True
    try:
        height = int(height)
    except ValueError:
        return False
    if height<140 or height>200:
        formatted=False

    return formatted

def validate_weight(weight):
    formatted=True
    try:
        weight = float(weight)
    except ValueError:
        return False
    if weight<40 or weight>175:
        formatted=False

    return formatted

def validate_age(age):
    formatted=True
    try:
        age=int(age)
    except ValueError:
        return False
    if age<18 and age>0:
        messagebox.showerror(
            "Error",
            "You must be 18 or above to use this application!",
            parent=title)
        formatted=False
    if age<0 or age>124:
        formatted=False

    return formatted

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
    
Heading = tk.Label(title, text = "Account Registration")
Heading.config(bg = "#d7e9fa", width = 20, font = ("Comic sans MS", 20), height = 1)
Heading.grid(column = 0, row = 0, columnspan = 5,pady=10)

Heading = tk.Label(title, text = "Username:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height = 1)
Heading.grid(column = 0, row = 1, pady = 2, columnspan = 5)

name_entry= tk.Entry(title) #username
name_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32)
name_entry.grid(column = 0, row = 2, pady = 3, columnspan = 5, sticky="ew")

Heading = tk.Label(title, text = "Enter email:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height = 1)
Heading.grid(column = 0, row = 3, pady = 2, columnspan = 5)

email_entry = tk.Entry(title) #email
email_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32)
email_entry.grid(column = 0, row = 4, pady = 3, columnspan = 5, sticky="ew")

Heading = tk.Label(title, text = "Enter password:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height =1)
Heading.grid(column = 0, row = 5, pady = 2, columnspan = 4)

password_entry = tk.Entry(title,show="*") #password
password_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32)
password_entry.grid(column = 0, row = 6, pady = 3, columnspan = 4, sticky="ew")
#HEIGHT
Heading = tk.Label(title, text = "Height: (cm)")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 11, height =1)
Heading.grid(column = 0, row = 7, pady = 2, columnspan = 1,sticky="w")

height_entry = tk.Entry(title)
height_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
height_entry.grid(column = 1, row = 7, pady = 3, columnspan = 1, sticky="ew")
#WEIGHT
Heading = tk.Label(title, text = "Weight: (kg)")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 11, height =1)
Heading.grid(column = 2, row = 7, pady = 2, columnspan = 1,sticky="ew")

weight_entry = tk.Entry(title)
weight_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
weight_entry.grid(column = 3, row = 7, pady = 3, columnspan = 1, sticky="ew")

#######
Heading = tk.Label(title, text = "Gender:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 0, row = 8, pady = 2, columnspan = 1,sticky="ew")

gender_option = tk.StringVar()
gender_box = ttk.Combobox(title, textvariable=gender_option, state="readonly")
gender_box['values'] = ("Male", "Female")
gender_box.current(0)
gender_box.grid(column = 1, row = 8, pady = 3, columnspan = 1, sticky="ew")

Heading = tk.Label(title, text = "Age:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 2, row = 8, pady = 2, columnspan = 1,sticky="ew")

age_entry = tk.Entry(title)
age_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
age_entry.grid(column = 3, row = 8, pady = 3, columnspan = 1, sticky="ew")

loginbutton = tk.Button(title, text = "Already have an account?\n Log in")
loginbutton.config(bg = "white", fg = "black", font = ("Comic sans MS", 14),\
                width = 5, height = 1,command=go_login)
loginbutton.grid(column = 0, row = 9, pady = 2, columnspan = 5, sticky = "ew")


signup_button = tk.Button(title, text = "Sign up")
signup_button.config(bg = "#6279A8", fg = "white", font = ("Comic sans MS", 14),\
                width = 5, height = 1,command=validation)
signup_button.grid(column = 1, row =10, pady = 2, columnspan = 2, sticky = "ew")

password_button = tk.Button(title, text = "Show")
password_button.config(bg = "white", fg = "black", font = ("Comic sans MS", 7),\
                width = 4, height = 1,command=hide)
password_button.grid(column = 4, row =6, pady = 2, columnspan = 1, sticky = "ew")



tk.mainloop()