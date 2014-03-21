# dashboard

A web and RESTful frontend dashboard for an mqtt broker.

The idea of dashboard is fairly simple. It subscribes to an MQTT topic,
then whenever a message is published to that topic or any sub-topics
it will be stored in a MongoDB collection.

You can then query the Web frontend or the REST interface for the topics
that have been recorded and the latest data published to them.

The driving idea behind this is to have a way to nicely present MQTT
 sensor data without having to wait for it on the client end.
 The server handles 
recording and storing it and then the client just has to query for
 what is available.

## Current State

* Basic MQTT subscription service is storing any messages in the 
collection
* Basic Flask interface is querying the database for the data 
published to recorded topics

## To Do
* When updating the collection with messages, the script should
check the topic collection for various settings, e.g. Keep history,
 how long, Average over time etc..
* The Flask side of things should do everything from the json rest
 interface including basic auth.


# REST Interface

|      URI      |     Function       | Example |        Status      |
|---------------|--------------------|---------|--------------------|
| /json         | Get list of topics | /json   | :heavy_check_mark: |
| /json/<topic path> | Return json for topic | /json/home/bedroom/temp | :heavy_check_mark: |
|
