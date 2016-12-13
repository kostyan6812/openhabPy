#import the library
import subprocess
import paho.mqtt.client as paho
import time

#variable
PIPE = subprocess.PIPE

#start 433 MHz sniffer
cmd = './rc -x rx -i 1'

#create MQTT client

def on_connect(client, userdata, flags, mid):
    print('CONNACK received with code %d.' + str(mid))

client = paho.Client(client_id='12',clean_session=False, protocol=paho.MQTTv31)
client.on_connect = on_connect
client.connect('127.0.0.1', '1883')
client.loop_start()

#get RC data 
while True:
	p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, close_fds=True)
	while True:
    	 s = p.stdout.readline()
	 sstart = s.find(':')
	 send = s.find(',')
	 s = s[sstart+1:send] 
    	 if not s: break
    	 print s,
	 rc = client.publish("main/flowSensor", str(s))
	 if rc.is_published() == 0:
	    print('Message is not yet published.', str(rc))
 	    rc.wait_for_publish()

 
