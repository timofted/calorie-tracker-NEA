import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import subprocess
import sys
from PIL import Image, ImageTk
import json, os
import time
from datetime import datetime

SESSION_FILE = "session.json"

current_time = int(time.time())
window = tk.Tk()
window.title("Log in")
window.config(bg = "#d7e9fa")

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

Heading = tk.Label(title, text = "Data representation")
Heading.config(bg = "#d7e9fa", width = 20, font = ("Comic sans MS", 20), height = 1)
Heading.grid(column = 0, row = 1, columnspan = 4,pady=10,padx=20,sticky="ew")

setting_img= Image.open("setting.png")
settings_resize= setting_img.resize((30,30))
img2= ImageTk.PhotoImage(settings_resize)


def go_to_setting():
    window.destroy()  
    subprocess.Popen([sys.executable, "settings.py"]) 

setting_label= tk.Button(title,image=img2)
setting_label.config(bg="white",font=("Comic sans MS",14),\
                     width=30,height=30,highlightthickness=0,command=go_to_setting)
setting_label.grid(column=3, row=0, pady=3, columnspan=1, sticky="ew")

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

##

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

user_id=load_session()

def weight_graph():
    timeframe=timeframe_input.get()
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Weight,Time
         FROM tblWeight
         WHERE User_ID=?"""
        
        cursor.execute(sql, (user_id,))
        rows=cursor.fetchall()
    weight_array=[]
    date_array=[]
    if timeframe=="day":
        for row in rows:
            if str(datetime.fromtimestamp(row[1]).date())[8:]==str(datetime.fromtimestamp(current_time).date())[8:]:
                weight_array.append(row[0])
                date_array.append(str(datetime.fromtimestamp(row[1]).strftime("%H:%M")))
    if timeframe=="month":
        for row in rows:
            if str(datetime.fromtimestamp(row[1]).date())[:4]==str(datetime.fromtimestamp(current_time).date())[:4]:
                weight_array.append(row[0])
                date_array.append(str(datetime.fromtimestamp(row[1]).strftime("%d %b")))
    if timeframe=="year":
        for row in rows:
            if str(datetime.fromtimestamp(row[1]).date())[5:7]==str(datetime.fromtimestamp(current_time).date())[5:7]:
                weight_array.append(row[0])
                date_array.append(str(datetime.fromtimestamp(row[1]).strftime("%b %Y")))
    
    weight= np.array(weight_array)
    plt.title("Nutritional Information")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.grid()

    plt.plot(weight,marker="s")
    plt.xticks(range(len(weight)), date_array, rotation=45, ha="right")

    plt.show()

def nutrition_graph():
    timeframe=timeframe_input.get()
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Proteins,Carbohydrates,Fats,Time
         FROM tblFood
         WHERE User_ID=?"""
        
        cursor.execute(sql, (user_id,))
        rows=cursor.fetchall()
    protein_array=[]
    carb_array=[]
    fat_array=[]
    date_array=[]
    if timeframe=="day":
        for row in rows:
            if str(datetime.fromtimestamp(row[3]).date())[8:]==str(datetime.fromtimestamp(current_time).date())[8:]:
                protein_array.append(row[0])
                carb_array.append(row[1])
                fat_array.append(row[2])
                date_array.append(str(datetime.fromtimestamp(row[3]).strftime("%H:%M")))
    if timeframe=="month":
        for row in rows:
            if str(datetime.fromtimestamp(row[3]).date())[:4]==str(datetime.fromtimestamp(current_time).date())[:4]:
                protein_array.append(row[0])
                carb_array.append(row[1])
                fat_array.append(row[2])
                date_array.append(str(datetime.fromtimestamp(row[3]).strftime("%d %b")))
        
    if timeframe=="year":
        for row in rows:
            if str(datetime.fromtimestamp(row[3]).date())[5:7]==str(datetime.fromtimestamp(current_time).date())[5:7]:
                protein_array.append(row[0])
                carb_array.append(row[1])
                fat_array.append(row[2])
                date_array.append(str(datetime.fromtimestamp(row[3]).strftime("%b %Y")))
    
    protein= np.array(protein_array)
    carbs=np.array(carb_array)
    fats=np.array(fat_array)

    plt.title("Nutritional Information")
    plt.xlabel("Items logged")
    plt.ylabel("Grams (g)")
    plt.grid()

    plt.plot(protein,marker="s",label="Protein")
    plt.plot(carbs,marker="s",label="Carbohydrates")
    plt.plot(fats,marker="s",label="Fats")
    plt.xticks(range(len(protein)), date_array, rotation=45, ha="right")
    plt.legend(loc="upper right")

    plt.show()

radio_frame = tk.Frame(title, bg="white")
radio_frame.grid(row=7, column=0, columnspan=4, pady=5,padx=20, sticky="ew")

timeframe_input= tk.StringVar(value="day")

radio_frame.grid_columnconfigure(0, weight=1)

inner_frame = tk.Frame(radio_frame, bg="white")
text_frame= tk.Frame(radio_frame, bg="white")
inner_frame.pack()
text_frame.pack()

daily = tk.Radiobutton(inner_frame, bg="white",variable=timeframe_input,value="day")
daily.pack(side="left", padx=50)

monthly= tk.Radiobutton(inner_frame, bg="white",variable=timeframe_input,value="month")
monthly.pack(side="left", padx=50)

yearly = tk.Radiobutton(inner_frame, bg="white",variable=timeframe_input,value="year")
yearly.pack(side="left", padx=50)

Heading = tk.Label(text_frame, text = "Past day")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 10), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text = "Past month")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 10), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text ="Past year")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 10), height = 1)
Heading.pack(side="left",padx=10)

weight_button= tk.Button(title, text="Weight Graph", command=lambda:weight_graph())
weight_button.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
weight_button.grid(column=0, row=5, columnspan= 2, pady=10,padx=20,sticky="ew")

nutrition_button= tk.Button(title, text="Nutrition Graph", command=lambda:nutrition_graph())
nutrition_button.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
nutrition_button.grid(column=2, row=5, columnspan= 2, pady=10,padx=20,sticky="ew")

tk.mainloop()