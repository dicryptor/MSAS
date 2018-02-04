import sys
import time
from datetime import datetime as dt
import blindspot
import led_notification
import lsm303
import location_info_v2

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

print("Initializing notification LEDs..")
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)


def trigger_front():
    left_front.rrange()
    right_front.rrange()


def trigger_back():
    left_back.rrange()
    right_back.rrange()


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

        print("{} | {:>6.2f} | {:>6.2f} | {:>6.2f} | {:>6.2f} |".format(dt.now().isoformat(), *vals))

        if vals[0] > DETECT and vals[2] < DETECT:
            leftLed.ledOn()
        else:
            leftLed.ledOff()

        if vals[1] > DETECT and vals[3] < DETECT:
            rightLed.ledOn()
        else:
            rightLed.ledOff()

        lat, lon = gps3.getlatlon()
        print("Latitude: {!s:15} Longitude: {!s:15}".format(lat, lon))

        accel = lsm303.getRealAccel()
        if not lsm303.past_accel:  # if first time running copy current readings to past readings
            lsm303.past_accel = accel
        compare_accel = [abs(i - j) for i, j in zip(accel, lsm303.past_accel)]  # compare current and previous readings
        if any(i > 1 for i in compare_accel):  # if any value changes more than 1G, we want to know about it
            acc_x, acc_y, acc_z = accel
            print('{}: X= {:>6.3f}G,  Y= {:>6.3f}G,  Z= {:>6.3f}G'.format(dt.now().isoformat(), acc_x, acc_y, acc_z))
            print("Are you involved in an accident? Do you require assistance?")
            time.sleep(10)
        else:  # if values are not fluctuating more than 1G, get the angle. Maybe bike has fallen over
            lsm303.angle_filtered = lsm303.sma.nextVal(lsm303.get_angle(accel))
            print("{} Tilt angle is {:>3.3f}{}".format(dt.now().isoformat(), lsm303.angle_filtered, lsm303.deg_sym))
            if lsm303.angle_filtered > 45 or lsm303.angle_filtered < -45:
                vehicle_ok = False

            while vehicle_ok == False:
                print("{} Bike has fallen over. Do you need assistance?".format(dt.now().isoformat()))
                accel = lsm303.getRealAccel()
                lsm303.angle_filtered = lsm303.sma.nextVal(lsm303.get_angle(accel))
                if -45 <= lsm303.angle_filtered <= 45:
                    vehicle_ok = True
                time.sleep(0.2)
except KeyboardInterrupt:
    led_notification.cleanUp()
