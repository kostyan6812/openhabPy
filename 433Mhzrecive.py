#!/usr/bin/python

#import the library
import subprocess
import paho.mqtt.client as mqtt
import time


#variable
PIPE = subprocess.PIPE
MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1883
MQTT_CLIENT = '433Mhz'
FILE_DAY = '/root/openhabPy/tmp/day.txt'
res = 0

#start 433 MHz sniffer
cmd = 'sudo /root/openhabPy/rc -x rx -i 1'

#get message from channel
def on_message(client, obj, msg):
	daymsg = str(msg.payload)
	print daymsg	

def save_file(file, key, data):
	key == 'day'
	f = open(file, 'w')
	f.write(key+str(data)+'\n')
	f.close()

def read_file(file, key):
	global string
	f = open(file, 'r')
	string = f.readline().rstrip()
        string = str(string.strip(key))
	return string
	f.close()

#create MQTT client
mqttc = mqtt.Client(MQTT_CLIENT)
mqttc.connect(MQTT_HOST, MQTT_PORT)


#get RC data 
i = 0
#read save file with last date
read_file(FILE_DAY, 'day')
if int(string) > 0:
	res = int(string)
else: res = 0
mqttc.publish('main/day/flowSensor', str(int(res)))

while True:
	#get date
	p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, close_fds=True)
    	s = p.stdout.readline()
	if str(s) == '':
		print "No 433 messages"
	else:
		sstart = s.find(':')
		send = s.find(',')
		s = int(s[sstart+1:send])
		rID = str(s)
		litres = s - (int(rID[0])*10000)
		i += 1
		#check result from file
		if int(s) == 0: 
			litres = res
		else : litres
		litres = litres / 1000
		res += litres
		#save new result in file
		save_file(FILE_DAY, 'day', res)
#	    	if not s: break
		mqttc.publish('main/day/flowSensor', str(float(res)))

	
