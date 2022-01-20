import sqlite3
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
import random

#currentDateTime=datetime.datetime.now()
#currentDateTime=datetime.date.today()
unix=time.time()
currentDateTime=str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
#or
#reading_time=int(time.time())

#Add Data
data=[
    ["80", "45.7", "72.6", "0.66", currentDateTime],
    ["60", "51.2", "87.8", "0.55",currentDateTime],
    ["90", "71.2", "76.3", "1.0",currentDateTime],
    # ["100", "81.0", "49.8", "0.33",currentDateTime],
    # ["100", "81.0", "49.8", "0.33",currentDateTime]
 ]
# value1=random.random()
# value2=random.random()
# value3=random.random()
# value4=random.random()
# data=[
#     [value1,  value2,  value3,  value4, currentDateTime]
#  ]

#create a  database or connect to one 
con=sqlite3.connect("sensors.db")
#create a cursor
cur=con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS sensors (
    soil REAL,
    temperature REAL, 
    humidity REAL, 
    camera REAL,
    DateTaken TIMESTAMP
    )""")
    #TIMESTAMP
    #Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  #this is how we create this


#add data to table
for record in data:
    cur.execute("INSERT INTO sensors VALUES (:soil,:temperature,:humidity,:camera,:DateTaken)", 
    {
    'soil': record[0],
    'temperature': record[1],
    'humidity': record[2],
    'camera': record[3],
    'DateTaken': record[4]
    }
    )
    # cur.execute("INSERT INTO sensor (soil,temperature,humidity,camera,DateTaken) VALUES (?,?,?,?,?)", 
    #     (soil,temperature,humidity,camera,DateTaken))

    #print("data successfully added  \n")

# cur.execute("SELECT * FROM sensors")
  
# result = cur.fetchall()
  
# for row in result:
#     print(row)
#     print("\n")

con.commit()
con.close()
