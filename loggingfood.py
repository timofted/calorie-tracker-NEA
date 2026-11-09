import tkinter as tk
from PIL import Image, ImageTk
import requests
import subprocess
import sys
import json,os
import sqlite3
import time


current_time = int(time.time())

window = tk.Tk()
window.title("Calorie tracker")
window.config(bg = "#d7e9fa")


title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

SESSION_FILE = "session.json"

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        
def on_close():
    clear_session()
    window.destroy() 

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as session:
            return json.load(session).get("user_id")
    return None


user_id=load_session()


window.protocol("WM_DELETE_WINDOW", on_close)

Heading = tk.Label(title, text = "Logging menu")
Heading.config(bg = "#d7e9fa", width = 10, font = ("Comic sans MS", 20), height = 1)
Heading.grid(column = 0, row = 0, columnspan = 4,pady=10)


#go to functions:

def go_to_setting():
    window.destroy()  
    subprocess.Popen([sys.executable, "settings.py"]) 

def go_to_home():
    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])

#IMAGES SECTION

home_img = Image.open("home.png")
resized_image = home_img.resize((50, 50))
img = ImageTk.PhotoImage(resized_image)

setting_img= Image.open("setting.png")
settings_resize= setting_img.resize((30,30))
img2= ImageTk.PhotoImage(settings_resize)
#
image_label = tk.Button(title, image=img)
image_label.config(bg = "white", font = ("Comic sans MS", 14),\
                width = 32, height =40,highlightthickness=0, command=go_to_home)
image_label.grid(column = 0, row = 1, pady = 3, columnspan = 4, sticky="ew")

setting_label= tk.Button(title,image=img2)
setting_label.config(bg="white",font=("Comic sans MS",14),\
                     width=30,height=30,highlightthickness=0,command=go_to_setting)
setting_label.grid(column=2, row=0, pady=3, columnspan=4, sticky="ew")
##SEARCHING MENUS

API_KEY = "YOUR API KEY HERE"
SEARCH_URL="https://api.nal.usda.gov/fdc/v1/foods/search"

foods = {}
selected_food_name = None

#FUNCTIONS:

    
def search_food():
    global selected_food_name 
    query = search_entry.get().strip() #Retrieve data from search entry when button pressed.
    if not query:
        return #return if empty 

    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 50
    }

    #Recieve data from the API and convert to python
    response = requests.get(SEARCH_URL, params=params).json()

    foods.clear() #Clear any previous foods
    listbox.delete(0, tk.END) 
    output_label.config(text="")
    selected_food_name = None

    seen = set() #Set to remove duplicates
    for food in response.get("foods", []):
        name = food["description"].title()
        if name in seen:
            continue
        seen.add(name)

        nutrients = {
            n["nutrientName"]: n.get("value", 0)
            for n in food.get("foodNutrients", [])
        }

        foods[name] = nutrients
        listbox.insert(tk.END, name)


    if foods:
        listbox.focus_set()
        listbox.selection_set(0)
        listbox.activate(0)


def submit_food():
    global selected_food_name

    selection = listbox.curselection()
    if not selection:
        output_label.config(text="Please select a food.")
        return

    selected_food_name = listbox.get(selection[0])


def show_nutrition():
    nutrients = foods[selected_food_name]
    try:
        grams = float(grams_entry.get())
        if grams <= 0: #ensure that the input is both positive and of the float data type
            raise ValueError
    except ValueError: 
        output_label.config(text="Enter a valid gram amount.")
        return


    def scale(val): #Change my value of the nutrient dependent on input quantity.
        return round((val / 100) * grams, 2)

    output_label.config(
        text=f"""Food: {selected_food_name}
Quantity: {grams} g

Calories: {scale(nutrients.get("Energy", 0))} kcal
Protein: {scale(nutrients.get("Protein", 0))} g
Carbs: {scale(nutrients.get("Carbohydrate, by difference", 0))} g
Fat: {scale(nutrients.get("Total lipid (fat)", 0))} g
"""
    )#Output formatting
    log_button.config( text="Log the food?",
                bg = "#6279A8", fg = "white", font = ("Comic sans MS", 14),\
                width = 5, height = 1)


def log_food():
    selection = listbox.curselection()
    selected_food_name=listbox.get(selection[0])
    nutrients = foods[selected_food_name]

    try:
        grams = float(grams_entry.get())
        if grams <= 0: #ensure that the input is both positive and of the float data type
            raise ValueError
    except ValueError: 
        output_label.config(text="Enter a valid gram amount.")
        return

    def scale(val): #Change my value of the nutrient dependent on input quantity.
        return round((val / 100) * grams, 2)
    
    calories=scale(nutrients.get("Energy", 0))
    proteins=scale(nutrients.get("Protein", 0))
    carbohydrates=scale(nutrients.get("Carbohydrate, by difference", 0))
    fats=scale(nutrients.get("Total lipid (fat)", 0))
    values = (calories,proteins,carbohydrates,fats,current_time,
    selected_food_name,grams,user_id)

    with sqlite3.connect("CalorieTracker.db") as db:

        cursor = db.cursor()

        sql = """   INSERT OR IGNORE INTO
                    	tblFood
                    	(Calories, Proteins, Carbohydrates, Fats, Time, Food, Quantity, User_ID)
                    	VALUES
                    	(?,?,?,?,?,?,?,?)"""
        
        cursor.execute(sql,values)
    
    window.destroy()
    subprocess.Popen([sys.executable, "loggingfood.py"])



#HEADING
tk.Label(title, text="Search food:").grid(row=2, column=0, padx=10)

#ENTRY
search_entry = tk.Entry(title, width=30)
search_entry.grid(row=2, column=1)

#SEARCH BUTTON
tk.Button(title, text="Search", command=search_food).grid(row=2, column=2)

#DROPDOWN MENUS
frame = tk.Frame(title)
frame.grid(row=3, column=0, columnspan=3, pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    frame,
    width=50,
    height=10,
    selectmode=tk.SINGLE,
    activestyle="dotbox",
    exportselection=False,
    yscrollcommand=scrollbar.set
)
listbox.pack(side=tk.LEFT)
scrollbar.config(command=listbox.yview)

listbox.bind("<Double-Button-1>", lambda e: submit_food())

#QUANTITY 
tk.Label(title, text="Quantity (grams):").grid(row=4, column=0)

grams_entry = tk.Entry(title, width=10)
grams_entry.insert(1, "100")
grams_entry.grid(row=4, column=1, sticky="w")

tk.Button(title, text="Submit", width=20, command=show_nutrition).grid(
    row=5, column=0, columnspan=3, pady=10
)

log_button = tk.Button(title, text = "")
log_button.config(bg = "white", fg = "white", font = ("Comic sans MS", 14),\
                width = 5, height = 1,command=log_food)
log_button.grid(column = 1, row = 7, pady = 2, columnspan = 2, sticky = "ew")


#RESULTS
output_label = tk.Label(title, justify="left", font=("Arial", 11))
output_label.grid(row=6, column=0, columnspan=3, pady=10)

tk.mainloop()
