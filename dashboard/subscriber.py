#!/usr/bin/python
import paho.mqtt.client as paho
from pymongo import MongoClient
from datetime import datetime


##############################
#         Variables
##############################
debug = True 


##############################
#       Misc Functions
##############################

def printText(text, level):
    now = datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S")
    timeString = "[" + now + "] "
    if(level is 1):
        if(debug):
            print(timeString + "DEBUG: " + text)
    else:
        print(timeString + "INFO: " + text)

##############################
#      MQTT Functions
##############################

def mqtt_initialise(host, topic):
    mqttc = paho.Client()
    mqttc.on_message = mqtt_on_message
    mqttc.on_connect = mqtt_on_connect
    mqttc.on_publish = mqtt_on_publish
    mqttc.on_subscribe = mqtt_on_subscribe
    mqttc.connect(host, 1883, 60)
    mqttc.subscribe(topic, 0)
    return mqttc
	
def mqtt_on_connect(mqttc, obj, rc):
    printText("rc: " +str(rc),1)
    
def mqtt_on_message(mqttc, obj, msg):
    printText(msg.topic + " => " + str(msg.payload), 0)
    post = applyRules(msg)
    printText("Inserting post: " + post['topic'], 1)
    postId = mqttCollection.insert(post)
    
def mqtt_on_publish(mqttc, obj, mid):
    printText("mid: " +str(mid),1)

def mqtt_on_subscribe(mqttc, obj, mid, granted_qos):
    printText("Subscribed to: " +str(mid)+" "+str(granted_qos),1)
    
def mqtt_on_log(mqttc, obj, level, string):
    printText(string,1)
    
    
##############################
#        Rule Functions
##############################
def applyRules(msg):
    printText("Applying rules for topic: " + str(msg.topic),1 )
    post = {"topic": msg.topic,
            "message": msg.payload,
            "time": datetime.utcnow()}
    return post
    
 
##############################
#       Cron Functions
##############################






mqttc = mqtt_initialise("jsutton.co.uk", "/#")
mongo = MongoClient()
database = mongo.dashboard_database
mqttCollection = database.mqtt_collection
printText("Dashboard Subscription Service has started", 0)


while True:
    mqttc.loop()




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
