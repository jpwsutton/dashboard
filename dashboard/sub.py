#!/usr/bin/python
import paho.mqtt.client as paho
from pymongo import MongoClient
from datetime import datetime
import threading
import Queue

debug = False

def printText(text, level):
    now = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    timeString = "[" + now + "] "
    if (level is 1):
        if(debug):
            print(timeString + "DEBUG: " + text)
    else:
        print(timeString + "INFO: " + text)



class mqttClient:
    """
    This class that manages the Main MQTT Subscriber thread
    """

    def __init__(self, host, topic):
        self.host = host
        self.topic = topic
        self.incoming_queue = Queue.Queue()
        self.command_queue = Queue.Queue()
        self.thread = mqttThread(self.host, self.topic, 
                self.incoming_queue, self.command_queue)
        self.thread.setDaemon(False)
        self.thread.start()
        self.incoming_queue.join()
        self.command_queue.join()

    def stop_client(self):
        """
        Tells the mqttThread to stop
        """
        self.command_queue.put("stop")



class mqttThread(threading.Thread):
    """
    This class is the main MQTT Subscriber thread
    """

    def __init__(self, host, topic, incoming_queue, command_queue):
        """
        Initializes the thread
        """
        threading.Thread.__init__(self)
        self.host = host
        self.topic = topic
        self.incoming_queue = incoming_queue
        self.command_queue = command_queue

        self._mqttc = paho.Client()
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe

        # Mongo Stuff
        self.mongo_client = MongoClient()
        self.mongo_database = self.mongo_client.dashboard_database
        self.mongo_collection = self.mongo_database.mqtt_collection

        


    def mqtt_on_connect(self, mqttc, obj, rc):
        """MQTT PAHO Callback for on connect"""
        pass

    def apply_rules(self, msg):
        printText("Applying rules for topic: " + str(msg.topic), 1)
        post = {"topic": msg.topic,
                "message": msg.payload,
                "time": datetime.utcnow()}
        return post

    def mqtt_on_message(self, mqttc, obj, msg):
        """MQTT PAHO Callback for message recieved"""
        printText(msg.topic + " => " + str(msg.payload), 0)
        post = self.apply_rules(msg)
        printText("Inserting post: " + str(post), 1)
        postId = self.mongo_collection.insert(post)
        

    def mqtt_on_publish(self, mqttc, obj, mid):
        """MQTT PAHO Callback for message published"""
        pass

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        """MQTT PAHO Callback for topic subscribed"""
        pass
    

    def run(self):
        """
        The main loop function that keeps this thread going
        untill it is no longer required
        """
        self._mqttc.connect(self.host, 1883, 60)
        self._mqttc.subscribe(self.topic, 0)
        while True:
            self._mqttc.loop()

            # Check command Queue
            if(not self.command_queue.empty()):
                command = self.command_queue.get()
                if command == "stop":
                    break
