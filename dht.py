#!/usr/bin/python

import subprocess
import paho.mqtt.client as mqtt
import time

#variable
PIPE = subprocess.PIPE
MQTT_HOST = '127.0.0.1'
MQTT_PORT = 1883
MQTT_CLIENT = 'DHT'

#create MQTT client
mqttc = mqtt.Client(MQTT_CLIENT)
mqttc.connect(MQTT_HOST, MQTT_PORT)

#start DHT read
cmd = 'sudo /root/openhabPy/dht'
res = 0
while True:
        p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, close_fds=True)
        s = p.stdout.readline()
	print s
        if str(s) == '':
                print ""
#                print "No DHT messages"
        else:
                sstart = s.find('H')
                send = s.find('*')
		hstart = s.find('H')
		hend = s.find('%')
		h = str(s[hstart+5:hend])
                s = str(s[sstart+17:send])
                mqttc.publish('main/dhtt/inhome', s)
                mqttc.publish('main/dhth/inhome', h)
