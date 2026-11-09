import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os
import sqlite3
import re
import hashlib
from tkinter import ttk
import time
import subprocess, sys

current_time = int(time.time())
SESSION_FILE = "session.json"

window = tk.Tk()
window.title("Settings")
window.config(bg = "#d7e9fa")

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

home_img = Image.open("home.png")
resized_image = home_img.resize((50, 50))
img = ImageTk.PhotoImage(resized_image)

def go_to_home():
    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])

image_label = tk.Button(title, image=img)
image_label.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height =40,highlightthickness=0, command=go_to_home)
image_label.grid(column = 0, row = 0, pady = 3, columnspan = 1, sticky="ew")

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        
def on_close():
    clear_session()
    window.destroy() 

window.protocol("WM_DELETE_WINDOW", on_close)


def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None


tk_user_id=tk.StringVar(value=load_session()) #user id to be used by tkinter
user_id=load_session() #user id to be used for sqlite


def retrieve_data():
     with sqlite3.connect("CalorieTracker.db") as db:
        

        cursor = db.cursor()

        sql = """SELECT *
         FROM tblUsers
         WHERE User_ID=?"""
        
        cursor.execute(sql,(user_id,))
        row=cursor.fetchone()
        return row

def validation():
    username=Username_input.get()
    email=Email_input.get()
    password=new_password_input.get()
    old_pass=old_password_input.get()
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
    if not validate_email(email):
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
    if check_old(hash_password(old_pass))== False:
        messagebox.showerror(
            "Error",
            "Old password is incorrect!",
            parent=title)
        return
    if validate_age(age)==False:
        messagebox.showerror(
            "Error",
            "Invalid age! \n Please enter a correct age",
            parent=title)
        return
        
    hashed_password=hash_password(password)
    update_data(username,email,hashed_password,height,weight,gender,age,current_time)
    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])

def check_old(old_pass):
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT PasswordHash
         FROM tblUsers
         WHERE User_ID=?"""
        
        cursor.execute(sql,(user_id,))
        row=cursor.fetchone()
    
    hash=row[0]
    if hash!=old_pass:
        return False

    
def hash_password(password): 
    return hashlib.sha256(password.encode()).hexdigest()


def update_data(username,email,hashed_password,height,weight,gender,age,time):

    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()
              
        sql = """
            UPDATE tblUsers
            SET 
            Email = ?,PasswordHash = ?,Height = ?,Weight = ?,Gender = ?,Username=?, Age=?
            WHERE User_ID = ?
            """
        cursor.execute(sql, (email, hashed_password, height, weight, gender, username,age,user_id))

    
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor=db.cursor()

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
    if height<0 and height>270:
        formatted=False

    return formatted

def validate_weight(weight):
    formatted=True
    try:
        weight = float(weight)
    except ValueError:
        return False
    if weight<0 and weight>650:
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

def bmi_calculation():
    height=float(height_entry.get())
    weight=float(weight_entry.get())
    bmi = round(weight / ((height / 100) ** 2),1)
    category=None
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    bmi_label.config(text=category)


username=tk.StringVar(value=retrieve_data()[1])
email=tk.StringVar(value=retrieve_data()[2])
passwordhash=tk.StringVar(value=retrieve_data()[3])
weight=tk.StringVar(value=retrieve_data()[4])
height=tk.StringVar(value=retrieve_data()[5])
gender=tk.StringVar(value=retrieve_data()[6])
age=tk.StringVar(value=retrieve_data()[7])


#USER ID
Heading = tk.Label(title, text = "User_ID:")
Heading.config(bg = "white", width = 15, font = ("Comic sans MS", 14))
Heading.grid(column = 0, row = 1, columnspan = 1, pady=10, sticky="w")

User_ID = tk.Entry(title,textvariable=tk_user_id)
User_ID.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, state="disabled")
User_ID.grid(column = 1, row = 1, pady = 3,padx=5, columnspan = 2, sticky="ew")


#USERNAME
Heading = tk.Label(title, text = "Username:")
Heading.config(bg = "white", width = 15, font = ("Comic sans MS", 14))
Heading.grid(column = 0, row = 2, columnspan = 1, pady=10, sticky="w")

Username_input = tk.Entry(title, textvariable=username)
Username_input.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 15)
Username_input.grid(column = 1, row = 2, pady = 3, columnspan = 2, sticky="ew")

#EMAIL
Heading = tk.Label(title, text = "Email:")
Heading.config(bg = "white", width = 15, font = ("Comic sans MS", 14))
Heading.grid(column = 0, row = 3, columnspan = 1, pady=10, sticky="w")

Email_input = tk.Entry(title, textvariable=email)
Email_input.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 15)
Email_input.grid(column = 1, row = 3, pady = 3, columnspan = 2, sticky="ew")

#NEW PASSWORD

Heading = tk.Label(title, text = "New password:")
Heading.config(bg = "white", width = 15, font = ("Comic sans MS", 14))
Heading.grid(column = 0, row = 4, columnspan = 1, pady=10, sticky="w")

new_password_input = tk.Entry(title)
new_password_input.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 15)
new_password_input.grid(column = 1, row = 4, pady = 3, columnspan = 2, sticky="ew")

#OLD PASSWORD

Heading = tk.Label(title, text = "Old password:")
Heading.config(bg = "white", width = 15, font = ("Comic sans MS", 14))
Heading.grid(column = 0, row = 5, columnspan = 1, pady=10, sticky="w")

old_password_input = tk.Entry(title)
old_password_input.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 15)
old_password_input.grid(column = 1, row = 5, pady = 3, columnspan = 2, sticky="ew")

#HEIGHT

Heading = tk.Label(title, text = "Height: (cm)")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 0, row = 6, pady = 2, columnspan = 1,sticky="ew")

height_entry = tk.Entry(title, textvariable=height)
height_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
height_entry.grid(column = 1, row = 6, pady = 3, columnspan = 2, sticky="ew")

#WEIGHT
Heading = tk.Label(title, text = "Weight: (kg)")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 0, row = 7, pady = 2, columnspan = 1,sticky="ew")

weight_entry = tk.Entry(title,textvariable=weight)
weight_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
weight_entry.grid(column = 1, row = 7, pady = 3, columnspan = 2, sticky="ew")

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

Heading = tk.Label(title, text = "Gender:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 0, row = 9, pady = 2, columnspan = 1,sticky="ew")

Heading = tk.Label(title, text = "Age:")
Heading.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 8, height =1)
Heading.grid(column = 0, row = 9, pady = 2, columnspan = 1,sticky="ew")

age_entry = tk.Entry(title,textvariable=age)
age_entry.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 4)
age_entry.grid(column = 1, row = 9, pady = 3, columnspan = 2, sticky="ew")

######


convert_button = tk.Button(title, text = "Save changes")
convert_button.config(bg = "#6279A8", fg = "white", font = ("Comic sans MS", 14),\
                width = 5, height = 1,command= validation)
convert_button.grid(column = 0, row = 11, pady = 2, columnspan = 2, sticky = "ew")

bmi_button = tk.Button(title, text = "Check BMI status")
bmi_button.config(bg = "#6279A8", fg = "white", font = ("Comic sans MS", 14),\
                width = 14, height = 1,command= bmi_calculation)
bmi_button.grid(column = 1, row = 10, pady = 2, columnspan = 1,padx=20, sticky = "ew")

bmi_label = tk.Label(title, text = "Category:")
bmi_label.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 14, height =1)
bmi_label.grid(column = 0, row = 10, pady = 2, columnspan = 1,padx=20,sticky="ew")

state_old=tk.BooleanVar(value=False)
state_new=tk.BooleanVar(value=False)

def hide_old():
    showing=state_old.get()
    if showing==True:
        old_password_button.config(text="Show")
        old_password_input.config(show="*")
        state_old.set(False)
    if showing==False:
        old_password_button.config(text="Hide")
        old_password_input.config(show="")
        state_old.set(True)

def hide_new():
    showing=state_new.get()
    if showing==True:
        new_password_button.config(text="Show")
        new_password_input.config(show="*")
        state_new.set(False)
    if showing==False:
        new_password_button.config(text="Hide")
        new_password_input.config(show="")
        state_new.set(True)

old_password_button = tk.Button(title, text = "Show")
old_password_button.config(bg = "white", fg = "black", font = ("Comic sans MS", 7),\
                width = 4, height = 1,command=hide_old)
old_password_button.grid(column = 4, row =5, pady = 2, columnspan = 1, sticky = "ew")

new_password_button = tk.Button(title, text = "Show")
new_password_button.config(bg = "white", fg = "black", font = ("Comic sans MS", 7),\
                width = 4, height = 1,command=hide_new)
new_password_button.grid(column = 4, row =4, pady = 2, columnspan = 1, sticky = "ew")

tk.mainloop()