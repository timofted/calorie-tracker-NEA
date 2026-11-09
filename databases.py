import sqlite3

def create_account_info_table():

    with sqlite3.connect("CalorieTracker.db") as db:
        cursor = db.cursor()

        sql = """   	CREATE TABLE IF NOT EXISTS
                    	tblUsers
                    	(User_ID INTEGER Primary Key AUTOINCREMENT,
                        Username TEXT,
                        Email TEXT UNIQUE,
                        PasswordHash TEXT,
                        Weight REAL,
                        Height INTEGER,
                        Gender TEXT,
                        Age INTEGER)                    """
    
        cursor.execute(sql)

    with sqlite3.connect("CalorieTracker.db") as db:
        cursor = db.cursor()

        sql = """   	CREATE TABLE IF NOT EXISTS
                    	tblFood
                    	(Food_ID INTEGER Primary Key AUTOINCREMENT,
                        User_ID INTEGER ,
                        Food TEXT,
                        Calories REAL,
                        Proteins REAL,
                        Carbohydrates REAL,
                        Fats REAL,
                        Quantity REAL,
                        Time INTEGER,   
                        FOREIGN KEY (User_ID) REFERENCES users(User_ID))
                                            """
    
        cursor.execute(sql)

    with sqlite3.connect("CalorieTracker.db") as db:
        cursor = db.cursor()

        sql = """   	CREATE TABLE IF NOT EXISTS
                    	tblWeight
                    	(Weight_ID INTEGER Primary Key AUTOINCREMENT,
                        User_ID INTEGER,
                        Weight REAL,
                        Time INTEGER,   
                        FOREIGN KEY (User_ID) REFERENCES users(User_ID))
                                            """
    
        cursor.execute(sql)



create_account_info_table()



