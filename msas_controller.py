import sys
import time
from datetime import datetime as dt
import blindspot
import led_notification
import lsm303
import location_info_v2
import bluetooth_comm
from threading import Thread
from queue import Queue

## Threshold for blindspot detection
DETECT = 20
RIGHT_LED = 20
LEFT_LED = 21

left_front = blindspot.USensor(0x71)
right_front = blindspot.USensor(0x70)
left_back = blindspot.USensor(0x72)
right_back = blindspot.USensor(0x73)
lsm303 = lsm303.LSM303(scale=16) #init accelerometer
gps3 = location_info_v2.GPS3() #int GPS module
bluetooth = bluetooth_comm.BluetoothComm()
sms_msg = {"type": None, "lat": None, "lon": None, "speed": None, "track": None}
q = Queue(maxsize=1) # to share message with bluetooth thread

print("Initializing notification LEDs..")
led_notification.cleanUp() # all pins are set to default status
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)


def trigger_front():
    left_front.rrange()
    right_front.rrange()


def trigger_back():
    left_back.rrange()
    right_back.rrange()

def msg_builder():
    pass


def main_loop():
    global sms_msg
    vals = [0, 0, 0, 0]
    vehicle_ok = True
    print("Starting detection cycle")
    try:
        while vehicle_ok == True:
            trigger_front()
            time.sleep(0.07)
            vals[0] = left_front.rread()
            vals[1] = right_front.rread()
            trigger_back()
            time.sleep(0.07)
            vals[2] = left_back.rread()
            vals[3] = right_back.rread()

            print("{:30}".format("-" * 60))
            print("System datetime is now: {}".format(dt.now()))
            print("{:>6.2f} | {:>6.2f} | {:>6.2f} | {:>6.2f} |".format(*vals))

            if vals[0] > DETECT and vals[2] < DETECT:
                leftLed.ledOn()
            else:
                leftLed.ledOff()

            if vals[1] > DETECT and vals[3] < DETECT:
                rightLed.ledOn()
            else:
                rightLed.ledOff()


            lat, lon = gps3.getlatlon()
            speed, track = gps3.getmovement()
            gpstime, timedelta = gps3.getdatetime(gps3.gettime())
            print("GPS datetime is now: {} Time difference is {!s:>5} seconds".format(gpstime, timedelta))
            print("Latitude: {!s:15} Longitude: {!s:15} Speed: {!s:15} Track: {!s:15}".format(lat, lon, speed, track))

            sms_msg["type"] = None
            sms_msg["lat"] = lat
            sms_msg["lon"] = lon
            sms_msg["speed"] = speed
            sms_msg["track"] = track

            accel = lsm303.getRealAccel()
            if not lsm303.past_accel:  # if first time running copy current readings to past readings
                lsm303.past_accel = accel
            compare_accel = [abs(i - j) for i, j in zip(accel, lsm303.past_accel)]  # compare current and previous readings
            if any(i > 1 for i in compare_accel):  # if any value changes more than 1G, we want to know about it
                sms_msg["type"] = "COLLISION detected"
                q.put(sms_msg)
                acc_x, acc_y, acc_z = accel
                print('{}: X= {:>6.3f}G,  Y= {:>6.3f}G,  Z= {:>6.3f}G'.format(dt.now().isoformat(), acc_x, acc_y, acc_z))
                print("Are you involved in an accident at {},{}. Do you require assistance?".format(lat, lon))
                time.sleep(30)
            else:  # if values are not fluctuating more than 1G, get the angle. Maybe bike has fallen over
                lsm303.angle_filtered = lsm303.sma.nextVal(lsm303.get_angle(accel))
                print("Tilt angle is {:>3.3f}{}".format(lsm303.angle_filtered, lsm303.deg_sym))
                if lsm303.angle_filtered > 45 or lsm303.angle_filtered < -45:
                    vehicle_ok = False

                while vehicle_ok == False:
                    sms_msg["type"] = "FALL over detected"
                    q.put(sms_msg)
                    print("{} Bike has fallen over at {},{} Do you need assistance?".format(dt.now().isoformat(), lat, lon))
                    time.sleep(30)
                    accel = lsm303.getRealAccel()
                    lsm303.angle_filtered = lsm303.sma.nextVal(lsm303.get_angle(accel))
                    if -45 <= lsm303.angle_filtered <= 45:
                        vehicle_ok = True
                    time.sleep(0.2)
            print("{:30}".format("-" * 60))
    except KeyboardInterrupt:
        led_notification.cleanUp()
        t1.join()


def btcomm_loop():
    try:
        while True:
            print("Waiting for connection...")
            client_sock, client_info = bluetooth.accept_connection()
            print("Accepted connection from {}".format(client_info))
            connected = True
            # msg = {}
            while connected == True:
                try:
                    data = bluetooth.recv_data()
                    if not q.empty():
                        msg = q.get()
                        print("Got message from queue...")
                        q.task_done()
                        if msg["type"] == ("COLLISION detected" or "FALL over detected"):
                            reply = "{}. At https://maps.google.com/?ll={},{} Speed is {}. Heading is {}.".format(
                                msg["type"],
                                msg.get("lat", "Unknown"),
                                msg.get("lon", "location"),
                                msg.get("speed", "unknown"),
                                msg.get("track", "unknown"))
                            client_sock.send(reply)
                            print("Message sent: {}".format(reply))

                    if len(data) > 0:
                        print("Received: {}".format(data))
                        if data.decode('UTF-8') == "disconnect":
                            print("Client request to disconnect")
                            break
                        elif data.decode('UTF-8') == "TEST COLLISION":
                            time.sleep(1)
                            client_sock.send("COLLISION detected!")
                        elif data.decode('UTF-8') == "TEST FALL":
                            time.sleep(1)
                            client_sock.send("FALL detected!")
                        # else: # for debugging only
                            # reply = "You sent me this: {}".format(data.decode('UTF-8'))
                            # client_sock.send(reply)
                except IOError:
                    print("IO error detected")
                    connected = False
                except AttributeError as e:
                    print(e)
                    connected = False
                except KeyboardInterrupt:
                    print("User cancelled operation")
                    connected = False
            client_sock.close()
    except KeyboardInterrupt:
        print("User cancelled operation")
        bluetooth.server_sock.close()
        t2.join()

# main_loop()
t1 = Thread(target=main_loop)
t2 = Thread(target=btcomm_loop)

t1.start()
t2.start()

# t1.join()
# t2.join()