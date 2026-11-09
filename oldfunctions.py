# def display():
#     with sqlite3.connect("CalorieTracker.db") as db:

#         cursor = db.cursor()

#         sql = """SELECT Calories,Proteins,Carbohydrates,Fats,Time
#          FROM tblFood
#          WHERE User_ID=?"""
        
#         cursor.execute(sql, (user_id,))
#         row=cursor.fetchall()
#     update_calories(row[0])
#     update_protein(row[1])
#     update_carbs(row[2])
#     update_fats(row[3])


#NEW FUNCTION:

# def display():
#     with sqlite3.connect("CalorieTracker.db") as db:

#         cursor = db.cursor()

#         sql = """SELECT Calories,Proteins,Carbohydrates,Fats,Time
#          FROM tblFood
#          WHERE User_ID=?"""
        
#         cursor.execute(sql, (user_id,))
#         rows=cursor.fetchall()
#     for row in rows:
#         if datetime.fromtimestamp(row[4]).date()==datetime.fromtimestamp(current_time).date():
#             update_calories(row[0])
#             update_protein(row[1])
#             update_carbs(row[2])
#             update_fats(row[3])


#OLD FUNCTION:


# def update_data(username,email,hashed_password,height,weight,gender,age,time):

#     with sqlite3.connect("CalorieTracker.db", timeout=3) as db:

#         cursor = db.cursor()
              
#         sql = """
#             UPDATE tblUsers
#             SET 
#             Email = ?,PasswordHash = ?,Height = ?,Weight = ?,Gender = ?,Username=?, Age=?
#             WHERE User_ID = ?
#             """
#         cursor.execute(sql, (email, hashed_password, height, weight, gender, username,age,user_id))

    
#     with sqlite3.connect("CalorieTracker.db") as db:

#         cursor=db.cursor()

#         sql = """   INSERT OR IGNORE INTO
#                     	tblWeight
#                     	(User_ID, Weight, Time)
#                     	VALUES
#                     	(?,?,?)"""
#         cursor.execute(sql,(user_id,weight,time))







# Heading = tk.Label(text_frame, text = "Sedentary\n (Little or no exercise)")
# Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
# Heading.pack(side="left",padx=10)

# Heading = tk.Label(text_frame, text = "Lightly Active\n (Light exercise 1-3 days/week)")
# Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
# Heading.pack(side="left",padx=10)

# Heading = tk.Label(text_frame, text ="Moderately active\n (Light to moderate exercise 4-5 days/week)")
# Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
# Heading.pack(side="left",padx=10)

# Heading = tk.Label(text_frame, text ="Active\n (Moderate exercise 6-7 days/week)\n (Intense exercise 3-4 times/week)")
# Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
# Heading.pack(side="left",padx=10)

# Heading = tk.Label(text_frame, text ="Very Active\n (Intense exercise 6-7 days/week)\n (Sports training or physical job)")
# Heading.config(bg = "#d7e9fa", width = 14, font = ("Comic sans MS", 8), height = 1)
# Heading.pack(side="left",padx=10)