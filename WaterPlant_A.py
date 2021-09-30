#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'WaterPlant_A'
__author__ = 'Robert Chen'


## WaterPlant_A is based on the WaterPlant_Test. The major diffirences between two program is that WaterPlant_A can upload moisture after test the moisture of soil and record the time point that water the planet

import time
import datetime
import grovepi
import leancloud

humidity = 100
WaterSystemStatus = True
timepoint = str(1)
watered = 0
humidity_need_water = 100

# Test the moisture of soil
def humidity_test():
    global humidity
    humidity_read_1 = grovepi.analogRead(humidity_sensor)
    time.sleep(3)
    humidity_read_2 = grovepi.analogRead(humidity_sensor)
    time.sleep(3)
    humidity_read_3 = grovepi.analogRead(humidity_sensor)
    humidity = (humidity_read_1 + humidity_read_2 + humidity_read_3)/3
    #humidity = 400
    return humidity

# Set the motor and sensor
motor = 4
humidity_sensor = 0

grovepi.pinMode(motor, 'OUTPUT')
grovepi.pinMode(humidity_sensor, 'INPUT')

def water_plant():
    # Send HIGH to switch on
    grovepi.digitalWrite(motor, 1)
    # Water plant for 2s
    time.sleep(2)
    # Send LOW to swtich off
    grovepi.digitalWrite(motor, 0)
    # Just wait
    time.sleep(90)

 
# Either it is time to water the plant
def WaterSystemStatus_judge():
    global WaterSystemStatus
    time = datetime.datetime.now().strftime("%H:%M")
    if ((time > "08:30") and (time < "20:30")):
        WaterSystemStatus = True
    else:
        WaterSystemStatus = False
    return WaterSystemStatus


print('Go')
# Water the plant
WaterSystemStatus_judge()
## Log time
timepoint = str(datetime.datetime.now().isoformat())
## count water times
water_count = 0
humidity_test()
while WaterSystemStatus == True:
    humidity_test()
    if humidity <= humidity_need_water and water_count < 10:
        water_plant()
        # Log water status
        watered = 1
        water_count += 1
    else:
        break
## Upload data to the database
print(timepoint,WaterSystemStatus,humidity,watered,water_count)
### Conect to the cloud database and initial it
leancloud.init("1QLftUJY9V1rRlHgrfKPUecN-gzGzoHsz", "RRMv01ndikMOsMPkdvhSMh1Q")
Plant_a_build = leancloud.Object.extend('Plant_a')
Plant_a = Plant_a_build()
Plant_a.set('Time', timepoint)
Plant_a.set('System_Status', WaterSystemStatus)
Plant_a.set('Mositure', humidity)
Plant_a.set('is_Watered', watered)
Plant_a.save()
