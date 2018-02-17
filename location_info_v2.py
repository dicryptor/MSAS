"""TriviaL example using the thread triumvirate
        agps_thread = AGPS3mechanism()
        agps_thread.stream_data()
        agps_thread.run_thread()
    imported from the agps3threaded.py class AGPS3mechanism.  The unordered associative array
    from the gpsd is then exposed as attributes of that 'data_stream'
"""
from time import sleep
from gps3.agps3threaded import AGPS3mechanism
import datetime
import pytz

class GPS3():
    ''' gps3 asynchronous communication module '''

    def __init__(self):
        self.agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
        self.agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
        self.agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default 0.2 second, default daemon=True
        self.mytimezone = pytz.timezone("Asia/Singapore")


    def getlatlon(self):
        if self.agps_thread.data_stream.lat != "n/a" and self.agps_thread.data_stream.lon != "n/a":
            return self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon

        return None, None

    def gettime(self):
        if self.agps_thread.data_stream.time != "n/a":
            return self.agps_thread.data_stream.time
        return None

    def getspeed(self):
        return self.agps_thread.data_stream.speed

    def gettrack(self):
        return self.agps_thread.data_stream.track

    def getmovement(self):
        self.speed = self.getspeed()
        self.track = self.gettrack()

        if self.speed != "n/a" and self.speed != None and self.track != None:
            if self.speed > .1:
                return float(self.speed), float(self.track)

        return None, None

    def getdatetime(self, dt):
        if dt is not None:
            self.DT = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ") # convert string to dt object
            self.DT = self.DT.replace(tzinfo=pytz.UTC) # add in UTC time zone info
            self.DTZ = self.DT.astimezone(self.mytimezone) #  convert to local timezone
            self.tdelta = self.timedelta(self.DT) # get the time difference in seconds
            return self.DTZ, self.tdelta
        return None, None

    def timedelta(self, dt):
        FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.dt1 = datetime.datetime.utcnow()
        self.dt1 = self.dt1.replace(tzinfo=pytz.UTC)
        self.dt2 = dt
        self.tdelta = self.dt1 - self.dt2
        return self.tdelta.seconds



if __name__ == "__main__":
    gps3 = GPS3()

    while True:  # All data is available via instantiated thread data stream attribute.
        print("System date time is now: {}".format(datetime.datetime.now()))
        print("GPS datetime is now: {} Time difference is {!s:>5} seconds".format(*gps3.getdatetime(gps3.gettime())))
        print("Latitude: {!s:15} Longitude: {!s:15}".format(*gps3.getlatlon()))
        print("Speed   : {!s:15}   Track: {!s:15}".format(*gps3.getmovement()))
        print("{:30}".format("-" * 30))
        print("{:30}".format("-" * 30))
        # # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
        # print('---------------------')
        # print(                   agps_thread.data_stream.time)
        # print('Lat:{}   '.format(agps_thread.data_stream.lat))
        # print('Lon:{}   '.format(agps_thread.data_stream.lon))
        # print('Speed:{} '.format(agps_thread.data_stream.speed))
        # print('Course:{}'.format(agps_thread.data_stream.track))
        # print('---------------------')
        sleep(2)  # Sleep, or do other things for as long as you like.
