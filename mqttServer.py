#!/usr/bin/python
import paho.mqtt.client as paho
from pymongo import MongoClient
import datetime

def mqtt_on_connect(mqttc, obj, rc):
    print("rc: " +str(rc))
    
def mqtt_on_message(mqttc, obj, msg):
    print(msg.topic + " => " + str(msg.payload))
    post = {"topic": msg.topic,
            "message": msg.payload,
            "time": datetime.datetime.utcnow()}
    postId = mqttCollection.insert(post)
    print("Inserted " + str(postId) + ": " + str(post))
    

def mqtt_on_publish(mqttc, obj, mid):
    print("mid: " +str(mid))

def mqtt_on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed to: " +str(mid)+" "+str(granted_qos))
    
def mqtt_on_log(mqttc, obj, level, string):
    print(string)
    
    
mqttc = paho.Client()
mqttc.on_message = mqtt_on_message
mqttc.on_connect = mqtt_on_connect
mqttc.on_publish = mqtt_on_publish
mqttc.on_subscribe = mqtt_on_subscribe


mongo = MongoClient()
database = mongo.dashboard_database
mqttCollection = database.mqtt_collection


mqttc.connect("jsutton.co.uk", 1883, 60)
mqttc.subscribe("/#", 0)
while True:
    mqttc.loop()

