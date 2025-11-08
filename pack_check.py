import mysql.connector


mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="30102004",
    database="XpenseTrack"  
)

cursor=mydb.cursor()

cursor.execute(f"""
SELECT * FROM hasan_add ORDER BY id DESC LIMIT 1;
            """)
lastrow=cursor.fetchone()

print(lastrow[3])