#!/usr/bin/python

#import the library
import sys
import os
import time
import paho.mqtt.client as mqtt

MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1883
MQTT_CLIENT = '433Mhz'
PATH = '/root/openhabPy/tmp/'

#file operations
def save_file(key, data):
 	file = PATH+key+'.txt'
        f = open(file, 'w')
        f.write(key+str(data)+'\n')
        f.close()

def read_file(key):
	file = PATH+key+'.txt'
        global string
        f = open(file, 'r')
        string = f.readline().rstrip()
        string = str(string.strip(key))
        return string
        f.close()

def on_message(client, obj, msg):
        daymsg = str(msg.payload)
        print daymsg

#create MQTT client
mqttc = mqtt.Client(MQTT_CLIENT)
mqttc.connect(MQTT_HOST, MQTT_PORT)

#Main code
param = sys.argv
proc = os.popen('ps ax | pgrep 433Mhzrecive.py').read()
os.popen('kill -9 '+proc).read()
print proc
if len (sys.argv) > 1:
	for param in sys.argv:
		if param == 'day':
			read_file('day')
			daystr = string
			read_file('week')
			weekstr = string
			print daystr, weekstr
			res = int(daystr) + int(weekstr)
			save_file('week', str(res))
			save_file('day', int(0))
			mqttc.publish('main/week/flowSensor', str(res))
		if param == 'week':
			read_file('week')
			weekstr = string
			read_file('month')
			monthstr = string
			print weekstr, monthstr
			res = int(weekstr) + int(monthstr)
			save_file('month', str(res))
			save_file('week', int(0))
			mqttc.publish('main/week/flowSensor', int(0))
			mqttc.publish('main/month/flowSensor', str(res))
		if param == 'month':
			read_file('year')
			yearstr = string
			read_file('month')
			monthstr = string
			print yearstr, monthstr
			res = int(yearstr) + int(monthstr)
			save_file('month', int(0))
			save_file('year', int(res))
			mqttc.publish('main/month/flowSensor', int(0))
			mqttc.publish('main/year/flowSensor', str(res))
		if param == 'year':
			save_file('year', int(0))
			mqttc.publish('main/year/flowSensor', int(0))
else: 
	print 'Period nor defined'
time.sleep(1)
os.popen('sudo /root/openhabPy/433Mhzrecive.py &')
exit()
	

