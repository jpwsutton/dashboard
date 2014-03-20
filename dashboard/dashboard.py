import subscriber
import time
from flask import Flask, request, render_template
from pymongo import MongoClient

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
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not Running with the Werkzeug Server')
    func()
    myClient.stop_client()
    time.sleep(2)
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
    return "You are looking at: %s" % topic



if __name__ == "__main__":
    app.run()
