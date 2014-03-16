import sub
import time


myClient = sub.mqttClient("jsutton.co.uk", "/home/#")





blah = raw_input("Press enter to close dashboard")
print("Sending kill signal")
myClient.stop_client()
time.sleep(2)
print("Now finishing")
