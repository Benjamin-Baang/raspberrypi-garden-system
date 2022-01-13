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


'''
Read all sensors except for camera
'''
def read_sensors():
	# To be done later
	return None


'''
Take and read image from camera
'''
def camera_sensor():
	original = cv2.imread('park.png')
	ndvi.display(original, 'Original')
	return original


'''
Calculate average NDVI value
'''
def average_ndvi(image):
	ndvi.calc_ndvi(image)
	total_sum = 0
	count = 0
	for row in image:
		for col in row:
			total_sum = col
			count += 1
	return total_sum / count # Value does not matter right now


'''
Check to activate system
'''
def sys_activate(values):
	# To be done later
	return False


'''
Update database with values
'''
def add_database():
	with sqlite3.connect(r'test.db') as database:
		database.row_factory = sqlite3.Row
		cursor = database.cursor()
		cursor.execute("select * from sensor_values")
		rows = cursor.fetchall()
		for row in rows:
			print(row['temperature'], row['ndvi'])
	return None


'''
Main function
'''
def main():
	read_sensors()
	original = camera_sensor()
	# avg = average_ndvi(original)
	add_database()


if __name__ == '__main__':
	main()
