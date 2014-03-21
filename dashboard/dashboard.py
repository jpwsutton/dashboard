import subscriber
import time
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import sys

app = Flask(__name__)

myClient = subscriber.mqttClient("jsutton.co.uk", "/home/#")

mongo_client = MongoClient()
mongo_database = mongo_client.dashboard_database
mqtt_collection = mongo_database.mqtt_collection
topic_collection = mongo_database.topic_collection

app.config.update(dict(
    DEBUG=True
    ))


def shutdown_server():
    myClient.stop_client()
    time.sleep(2)
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not Running with the Werkzeug Server')
    func()
    print("Goodbye!")

@app.route("/shutdown", methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/topics")
def list_topics():
    topic_list = []
    topics = topic_collection.find()
    for topic in topics:
        topic_list.append(topic['topic'])
    return render_template('list_topics.html', topic_list=topic_list)

@app.route("/<path:topic>")
def catch_topic(topic):
    topic_path = "/" + topic
    topic_count = mqtt_collection.find({'topic' : topic_path}).count()

    return "You are looking at: %s, there are %s entries." % (topic_path, topic_count) 

@app.route("/json/<path:topic>")
def json_topic(topic):
    topic_path = "/" +topic
    entry = mqtt_collection.find_one({'topic': topic_path})
    return jsonify(topic=entry['topic'],
                   message=entry['message'],
                   time=entry['time'])



if __name__ == "__main__":
    app.run()
    print("Goodbye")
    sys.exit()
