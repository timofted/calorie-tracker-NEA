import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import subprocess, sys
import json,os
import sqlite3
import time
from datetime import datetime

current_time = int(time.time())
window = tk.Tk()
window.title("Home")
window.config(bg = "#d7e9fa")

window.grid_columnconfigure(0, weight=1)

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

SESSION_FILE = "session.json"

setting_img= Image.open("setting.png")
settings_resize= setting_img.resize((30,30))
img2= ImageTk.PhotoImage(settings_resize)

def go_to_setting():
    window.destroy() 
    print("Visited Settings!")
    subprocess.Popen([sys.executable, "settings.py"]) 

setting_label= tk.Button(title,image=img2)
setting_label.config(bg="white",font=("Comic sans MS",14),\
                     width=30,height=30,highlightthickness=0,command=go_to_setting)
setting_label.grid(column=4, row=0, pady=3, columnspan=1, sticky="ew")

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None

def go_info():
    window.destroy() 
    print("Visited Info page!")
    subprocess.Popen([sys.executable, "activityinfo.py"])


user_id=load_session()

def display():
    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Calories,Proteins,Carbohydrates,Fats,Time
         FROM tblFood
         WHERE User_ID=?"""
        
        cursor.execute(sql, (user_id,))
        rows=cursor.fetchall()
    for row in rows:
        if datetime.fromtimestamp(row[4]).date()==datetime.fromtimestamp(current_time).date():
            update_calories(row[0])
            update_protein(row[1])
            update_carbs(row[2])
            update_fats(row[3])


def calculate():
    global CALORIE_GOAL,FAT_GOAL,CARB_GOAL,PROTEIN_GOAL
    level=activity.get()
    status=goal.get()
    multiplier=1
    if level=="sedentary":
        multiplier=1.2
    if level=="light":
        multiplier=1.375
    if level=="moderate":
        multiplier=1.55
    if level=="active":
        multiplier=1.725
    if level=="intense":
        multiplier=1.9
    if status=="losing":
        multiplier=multiplier*0.8
    if status=="gaining":
        multiplier=multiplier*1.1

    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """SELECT Weight,Height,Age,Gender
         FROM tblUsers
         WHERE User_ID=?"""
              
        cursor.execute(sql, (user_id,))
        row=cursor.fetchone()

    weight=row[0]
    height=row[1]
    age=row[2]
    gender=row[3]
    
    if gender=="female":
        expenditure=((10*weight) + (6.25*height)-(5*age)-161)*multiplier
    else:
        expenditure= ((10*weight) + (6.25*height)-(5*age) + 5)*multiplier
        
    CALORIE_GOAL=expenditure
    PROTEIN_GOAL= (expenditure * 0.25) / 4
    CARB_GOAL= (expenditure * 0.5) / 4
    FAT_GOAL= (expenditure * 0.25) / 9

    progresscal.config(maximum=CALORIE_GOAL)
    progresscarb.config(maximum=CARB_GOAL)
    progressfats.config(maximum=FAT_GOAL)
    progressprotein.config(maximum=PROTEIN_GOAL)

    subbutton.config(state="disabled")

    display()

        
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        
def on_close():
    clear_session()
    window.destroy() 

window.protocol("WM_DELETE_WINDOW", on_close)

Heading = tk.Label(title, text = "Home")
Heading.config(bg = "#d7e9fa", width = 5, font = ("Comic sans MS", 20), height = 1)
Heading.grid(column = 0, row = 1, columnspan = 5,pady=10,padx=20,sticky="ew")

CALORIE_GOAL=0
PROTEIN_GOAL=0
CARB_GOAL=0
FAT_GOAL=0

protein_consumed=tk.IntVar(value=0)
total_protein=0 

carbs_consumed=tk.IntVar(value=0)
total_carbs=0 

fats_consumed=tk.IntVar(value=0)
total_fats=0

calories_consumed=tk.IntVar(value=0)
total_cal=0

#CALORIE PROGRESS BAR
progresscal=ttk.Progressbar(title, orient="horizontal",length=300,mode="determinate",
                         maximum=CALORIE_GOAL)      #FIRST BAR#
 
progresscal.grid(column=0, row=2, columnspan= 2, pady=10,padx=20)

remainingcal_label=tk.Label(title, text=f"Calories Remaining: {CALORIE_GOAL}")
remainingcal_label.config(bg = "#d7e9fa", width = 25, font = ("Comic sans MS", 14), height = 1)
remainingcal_label.grid(column = 4, row = 2, columnspan = 4,pady=10,padx=20)

def update_calories(calories):
    global total_cal

    total_cal+=calories
    progresscal["value"]=total_cal #Sum of the calories consumed in one day set to progress value

    calories_remaining= CALORIE_GOAL-total_cal
    remainingcal_label.config(text=f"Calories Remaining: {round(calories_remaining,1)}")

#############

progressprotein=ttk.Progressbar(title, orient="horizontal",length=300,mode="determinate",
                         maximum=PROTEIN_GOAL)

progressprotein.grid(column=0, row=3, columnspan= 2, pady=10,padx=20)

remainingprotein_label=tk.Label(title, text=f"Protein Remaining: {PROTEIN_GOAL}")
remainingprotein_label.config(bg = "#d7e9fa", width = 25, font = ("Comic sans MS", 14), height = 1)
remainingprotein_label.grid(column = 4, row = 3, columnspan = 4,pady=10,padx=20)

def update_protein(proteins):
    global total_protein

    total_protein+=proteins
    progressprotein["value"]=total_protein #Sum of the protein consumed in one day set to progress value

    protein_remaining= PROTEIN_GOAL-total_protein
    remainingprotein_label.config(text=f"Protein Remaining: {round(protein_remaining,1)}")

##############

progresscarb=ttk.Progressbar(title, orient="horizontal",length=300,mode="determinate",
                         maximum=CARB_GOAL)

progresscarb.grid(column=0, row=4, columnspan= 2, pady=10,padx=20)

remainingcarb_label=tk.Label(title, text=f"Carbohydrates Remaining: {CARB_GOAL}")
remainingcarb_label.config(bg = "#d7e9fa", width = 25, font = ("Comic sans MS", 14), height = 1)
remainingcarb_label.grid(column = 4, row = 4, columnspan = 4,pady=10,padx=20)

def update_carbs(carbohydrates):
    global total_carbs

    total_carbs+=carbohydrates
    progresscarb["value"]=total_carbs #Sum of the carbs consumed in one day set to progress value

    carbs_remaining= CARB_GOAL-total_carbs
    remainingcarb_label.config(text=f"Carbohydrates Remaining: {round(carbs_remaining,1)}")

#################

progressfats=ttk.Progressbar(title, orient="horizontal",length=300,mode="determinate",
                         maximum=FAT_GOAL)
progressfats.grid(column=0, row=5, columnspan= 2, pady=10,padx=20)

remainingfats_label=tk.Label(title, text=f"Fats Remaining: {FAT_GOAL}")
remainingfats_label.config(bg = "#d7e9fa", width = 25, font = ("Comic sans MS", 14), height = 1)
remainingfats_label.grid(column = 4, row = 5, columnspan = 4,pady=10,padx=20)

def update_fats(fats):
    global total_fats

    total_fats+=fats
    progressfats["value"]=total_fats #Sum of the fats consumed in one day set to progress value

    fats_remaining= FAT_GOAL-total_fats
    remainingfats_label.config(text=f"Fats Remaining: {round(fats_remaining,1)}")

def log_food():
    window.withdraw() 
    subprocess.Popen([sys.executable, "loggingfood.py"]) #go logging menu

def go_datarep():
    window.destroy()
    print("Visited Data representation!")
    subprocess.Popen([sys.executable, "datarep.py"])

def reset():
    #gets current day, then converts to time into a timestamp

    today_date = time.strftime("%Y-%m-%d")
    today_struct = time.strptime(today_date, "%Y-%m-%d")
    today_start = int(time.mktime(today_struct)) 
    today_end=today_start+86400 #seconds in a day

    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """DELETE
         FROM tblFood
         WHERE User_ID=? AND Time BETWEEN ? AND ?"""
              
        cursor.execute(sql, (user_id,today_start,today_end))
    
    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])
    

infobutton= tk.Button(title, text="Activity information", command=lambda:go_info())
infobutton.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
infobutton.grid(column=0, row=12, columnspan= 2, pady=10,padx=20,sticky="ew")

subbutton= tk.Button(title, text="Log activity", command=lambda:calculate())
subbutton.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
subbutton.grid(column=0, row=13, columnspan= 2, pady=10,padx=20,sticky="ew")

######

navbutton= tk.Button(title, text="Logging menu", command=lambda:log_food())
navbutton.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
navbutton.grid(column=3, row=12, columnspan= 2, pady=10,padx=20,sticky="ew")

repbutton= tk.Button(title, text="Data Representation", command=lambda:go_datarep())
repbutton.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
repbutton.grid(column=3, row=13, columnspan= 2, pady=10,padx=20,sticky="ew")

delete_button= tk.Button(title, text="Reset daily log", command=lambda:reset())
delete_button.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 15))
delete_button.grid(column=0, row=14, columnspan= 5, pady=10,padx=20,sticky="ew")

radio_frame = tk.Frame(title, bg="white")
radio_frame.grid(row=8, column=0, columnspan=5, pady=5,padx=20, sticky="ew")

radio_frame2 = tk.Frame(title, bg="white")
radio_frame2.grid(row=10, column=0, columnspan=5, pady=5,padx=20, sticky="ew")

activity= tk.StringVar(value="Sedentary")
goal= tk.StringVar(value="maintain")

radio_frame.grid_columnconfigure(0, weight=1)
radio_frame2.grid_columnconfigure(0, weight=1)


Heading = tk.Label(title, text = "Please select an activity level:")
Heading.config(bg = "#d7e9fa", width = 40, font = ("Comic sans MS", 15), height = 1)
Heading.grid(row=7,column=0, columnspan = 5,pady=10, padx=30)

activity_frame = tk.Frame(radio_frame, bg="white")
text_frame= tk.Frame(radio_frame, bg="white")

Heading = tk.Label(title, text = "Please select a weight goal:")
Heading.config(bg = "#d7e9fa", width = 40, font = ("Comic sans MS", 15), height = 1)
Heading.grid(row=9,column=0, columnspan = 5,pady=10,padx=30)

goal_frame = tk.Frame(radio_frame2, bg="white")
text_frame2= tk.Frame(radio_frame2, bg="white")

activity_frame.pack()
text_frame.pack()


goal_frame.pack()
text_frame2.pack()

sedentary = tk.Radiobutton(activity_frame, bg="white",variable=activity,value="sedentary")
sedentary.pack(side="left", padx=50)

light = tk.Radiobutton(activity_frame, bg="white",variable=activity,value="light")
light.pack(side="left", padx=50)

moderate = tk.Radiobutton(activity_frame, bg="white",variable=activity,value="moderate")
moderate.pack(side="left", padx=50)

active = tk.Radiobutton(activity_frame, bg="white",variable=activity,value="active")
active.pack(side="left", padx=50)

intense = tk.Radiobutton(activity_frame, bg="white",variable=activity,value="intense")
intense.pack(side="left", padx=50)


Heading = tk.Label(text_frame, text = "Sedentary")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text = "Lightly Active")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text ="Moderately active")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text ="Active")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame, text ="Very Active")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

losing = tk.Radiobutton(goal_frame, bg="white",variable=goal,value="losing")
losing.pack(side="left", padx=50)

maintain = tk.Radiobutton(goal_frame, bg="white",variable=goal,value="light")
maintain.pack(side="left", padx=50)

maintain = tk.Radiobutton(goal_frame, bg="white",variable=goal,value="moderate")
maintain.pack(side="left", padx=50)

Heading = tk.Label(text_frame2, text ="Losing Weight")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame2, text ="Maintaining Weight")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

Heading = tk.Label(text_frame2, text ="Gaining weight")
Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
Heading.pack(side="left",padx=10)

for i in range(5):
    title.grid_columnconfigure(i, weight=3) #make every column same length


tk.mainloop()