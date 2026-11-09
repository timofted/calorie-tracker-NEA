import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess,sys
import json,os


SESSION_FILE = "session.json"

window = tk.Tk()
window.title("Log in")
window.config(bg = "#d7e9fa")

title = tk.Frame(window)
title.config(bg = "white")
title.grid(column = 0, row = 0, padx = 20, pady = 20)

home_img = Image.open("home.png")
resized_image = home_img.resize((50, 50))
img = ImageTk.PhotoImage(resized_image)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def on_close():
    clear_session()
    window.destroy() 

window.protocol("WM_DELETE_WINDOW", on_close)


def go_to_home():
    window.destroy()
    subprocess.Popen([sys.executable, "menu.py"])

Heading = tk.Label(title, text = "Sedentary\n (Little or no exercise)")
Heading.config(bg = "#d7e9fa", width = 35, font = ("Comic sans MS", 14), height = 3)
Heading.pack(padx=10,pady=10)

Heading = tk.Label(title, text = "Lightly Active\n (Light exercise 1-3 days/week)")
Heading.config(bg = "#d7e9fa", width = 35, font = ("Comic sans MS", 14), height = 3)
Heading.pack(padx=10,pady=10)

Heading = tk.Label(title, text ="Moderately active\n (Light to moderate exercise 4-5 days/week)")
Heading.config(bg = "#d7e9fa", width = 35, font = ("Comic sans MS", 14), height = 3)
Heading.pack(padx=10,pady=10)

Heading = tk.Label(title, text ="Active\n (Moderate exercise 6-7 days/week)\n (Intense exercise 3-4 times/week)")
Heading.config(bg = "#d7e9fa", width = 35, font = ("Comic sans MS", 14), height = 3)
Heading.pack(padx=10,pady=10)

Heading = tk.Label(title, text ="Very Active\n (Intense exercise 6-7 days/week)\n (Sports training or physical job)")
Heading.config(bg = "#d7e9fa", width = 35, font = ("Comic sans MS", 14), height = 3)
Heading.pack(padx=10,pady=10)

image_label = tk.Button(title, image=img)
image_label.config(bg = "white", font = ("Comic sans MS", 20),\
                width = 32, height =40,highlightthickness=0, command=go_to_home)
image_label.pack(padx=10,pady=10)


tk.mainloop()