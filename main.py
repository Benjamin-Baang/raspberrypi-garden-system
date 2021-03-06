import ndvi
import cv2
import numpy as np
from picamera import PiCamera
import picamera.array
import psycopg2, psycopg2.extras
from config_db import config
import sensors
import datetime
import time
import states
from states import Automated, Manual, Scheduler, Admin, Context
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

class Task:
    def __init__(self):
        self.duration = 0
        self.elapsed_time = 0
        self.funct = None
          
def read_sensors():
    '''
    Read all sensors except for camera
    '''
    return sensors.read_data()
    # return 70, 10, 3.3


def camera_sensor():
    '''
    Take and read image from camera
    '''
    original = ndvi.take_picture()
    # original = cv2.imread('test.png')
#	ndvi.display(original, 'Original')
#	original = cv2.imread('park.png')
    return average_ndvi(original)
   # return original


def average_ndvi(image):
    '''
    Calculate average NDVI value
    '''
    im = ndvi.contrast_stretch(image)
    im,avg,p2 = ndvi.calc_ndvi(im)
   # total_sum = 0
   # count = 0
   # for row in im:
       # for col in row:
           # total_sum = col
           # count += 1
   # return total_sum / count # Value does not matter right now
    return avg

def update_database(soil_moisture, temperature, humidity, camera):
    '''
    Update database with values
    '''
    with psycopg2.connect(**config()) as database:
        cursor = database.cursor()
        if camera == -2:
            cursor.execute("select camera from sensors order by datetaken desc limit 5")
            camera = cursor.fetchone()
        cursor.execute("insert into sensors (soil, temperature, humidity, camera, DateTaken) VALUES(%s, %s, %s, %s, %s)", (soil_moisture, temperature, humidity, camera, currentDateTime))
    return None

def process_sensors(context: Context):
    global currentDateTime
    currentDateTime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    random.seed()
    # temperature = random.randint(50, 100)
    # humidity = random.randint(30, 80)
    # soil_moisture = round(random.uniform(1, 10), 1)
    temperature, humidity, soil_moisture = read_sensors()
    # avg = camera_sensor()
    update_database(soil_moisture, temperature, humidity, -2)

    
def process_sensors_with_camera(context: Context):
    global currentDateTime
    currentDateTime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    random.seed()
    # temperature = random.randint(50, 100)
    # humidity = random.randint(30, 80)
    # soil_moisture = round(random.uniform(1, 10), 1)
    temperature, humidity, soil_moisture = read_sensors()
    # avg = round(random.uniform(0,1),2)
    avg = camera_sensor()
    update_database(soil_moisture, temperature, humidity, avg)


def app_listen(context: Context):
    with psycopg2.connect(**config()) as db:
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('select exists(select 1 from app_user where id=%s)', (1,))
        user = cursor.fetchone()
        if user[0]:
            cursor.execute('select * from app_user where id=%s', (1,))
        else:
            cursor.execute('select * from app_user where id=%s', (0,))
        user = cursor.fetchone()
        if user[1] == 'automated':
            context.set_state(Automated())
        elif user[1] == 'manual':
            context.set_state(Manual())
        elif user[1] == 'timer':
            context.set_state(Scheduler())
        elif user[1] == 'admin':
            context.set_state(Admin())
    s_flag = context.request()
    # print(s_flag)
    if s_flag:
        print("System activates!\n")
        GPIO.output(26, False)
        GPIO.output(20, True)
    else:
        print("System shuts down...\n")
        GPIO.output(26, True)
        GPIO.output(20, False)

def main():
    '''
    Main function
    '''
    task1 = Task()
    task1.duration = 5
    task1.elapsed_time = 5
    task1.funct = process_sensors
    task2 = Task()
    task2.duration = 30
    task2.elapsed_time = 30
    task2.funct = process_sensors_with_camera
    task3 = Task()
    task3.duration = 1
    task3.elapsed_time = 0
    task3.funct = app_listen
    
    tasks = [task1, task2, task3]
    
    context = Context(Automated())
    
    while True:
        for task in tasks:
            if task2.elapsed_time == 30:
                task1.elapsed_time = -1
            if task.elapsed_time >= task.duration - 1:
                task.funct(context)
                task.elapsed_time = 0
            else:
                task.elapsed_time += 1
        time.sleep(1)
    
    
    # while (1):
    #     global currentDateTime
    #     currentDateTime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #     random.seed()
    #     temperature = random.randint(50, 100)
    #     humidity = random.randint(30, 80)
    #     soil_moisture = round(random.uniform(1, 10), 1)
    #     avg = round(random.uniform(0, 1), 2)
    #     update_database(soil_moisture, temperature, humidity, avg)
    #     with psycopg2.connect(**config()) as db:
    #         cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #         cursor.execute('select * from app_user where id=%s', (1,))
    #         user = cursor.fetchone()
    #         if user[1] == 'automated':
    #             context.set_state(Automated())
    #         elif user[1] == 'manual':
    #             context.set_state(Manual())
    #         elif user[1] == 'scheduler':
    #             context.set_state(Scheduler())
    #     s_flag = context.request()
    #     print(s_flag)
    #     if s_flag:
    #         print('System is activated!')
    #     else:
    #         print('System is turned off...')
    #     time.sleep(10)


if __name__ == '__main__':
	main()
