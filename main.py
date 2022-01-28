#####    Pseudocode    #####
# Read sensor values
# Convert sensor readings to acceptable values
# Take picture with camera
# Calculate average NDVI value(s) from picture
# Use values to determine activation
# Send values to database

##### TODO Later #####
# Incorporate different modes of operations

import ndvi
import cv2
import numpy as np
from picamera import PiCamera
import picamera.array
import sqlite3
import sensors
import datetime
import time
import test
from test import Automated, Manual, Scheduler
import random

unix=time.time()
#currentDateTime=str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
#currentDateTime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


'''
Read all sensors except for camera
'''
def read_sensors():
#	return sensors.read_data()
	return 70, 10, 3.3

'''
Take and read image from camera
'''
def camera_sensor():
#	ndvi.take_picture()
	original = cv2.imread('test.png')
#	ndvi.display(original, 'Original')
#	original = cv2.imread('park.png')
	return original


'''
Calculate average NDVI value
'''
def average_ndvi(image):
	im = ndvi.contrast_stretch(image)
	im = ndvi.calc_ndvi(im)
	total_sum = 0
	count = 0
	for row in im:
		for col in row:
			total_sum = col
			count += 1
	return total_sum / count # Value does not matter right now


'''
Update database with values
'''
def update_database(soil_moisture, temperature, humidity, camera):
#	with sqlite3.connect(r'sensors.db') as database:
#		database.row_factory = sqlite3.Row
#		cursor = database.cursor()
#		cursor.execute("select * from sensors")
#		rows = cursor.fetchall()
#		for row in rows:
#			print(row['soil'], row['temperature'], row['humidity'], row['camera'], row['DateTaken'])
	with sqlite3.connect(r'sensors.db') as database:
		database.row_factory = sqlite3.Row
		cursor = database.cursor()
		cursor.execute("insert into sensors (soil, temperature, humidity, camera, DateTaken) VALUES(?, ?, ?, ?, ?)", (soil_moisture, temperature, humidity, camera, currentDateTime))
	return None


'''
Main function
'''
def main():
    context = test.Context(Automated())
    while (1):
        global currentDateTime
        currentDateTime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	    #temperature, humidity, soil_moisture = read_sensors()
	    #original = camera_sensor()
	    #avg = average_ndvi(original)
	    #print(avg)
        random.seed()
        temperature = random.randint(50, 100)
        humidity = random.randint(30, 80)
        soil_moisture = round(random.uniform(1, 10), 1)
        avg = round(random.uniform(0, 1), 2)
        update_database(soil_moisture, temperature, humidity, avg)
        with sqlite3.connect(r'sensors.db') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute('select * from user where id=?', (1,))
            user = cursor.fetchone()
            if user['State'] == 'automated':
                context.set_state(Automated())
            elif user['State'] == 'manual':
                context.set_state(Manual())
            elif user['State'] == 'scheduler':
                context.set_state(Scheduler())
        s_flag = context.request()
        print(s_flag)
        if s_flag:
            print('System is activated!')
        else:
            print('System is turned off...')
        time.sleep(30)


if __name__ == '__main__':
	main()
