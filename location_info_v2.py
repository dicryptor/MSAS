"""TriviaL example using the thread triumvirate
        agps_thread = AGPS3mechanism()
        agps_thread.stream_data()
        agps_thread.run_thread()
    imported from the agps3threaded.py class AGPS3mechanism.  The unordered associative array
    from the gpsd is then exposed as attributes of that 'data_stream'
"""
from time import sleep
from gps3.agps3threaded import AGPS3mechanism

class GPS3():
    ''' gps3 asynchronous communication module '''

    def __init__(self):
        self.agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
        self.agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
        self.agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default 0.2 second, default daemon=True


    def getlatlon(self):
        return self.agps_thread.data_stream.lat, self.agps_thread.data_stream.lon

    def gettime(self):
        return self.agps_thread.data_stream.time

    def getspeed(self):
        return self.agps_thread.data_stream.speed

    def gettrack(self):
        return self.agps_thread.data_stream.track

    def getmovement(self):
        self.speed = float(self.getspeed())
        self.track = float(self.gettrack())

        if self.speed > 1:
            return self.speed, self.track


if __name__ == "__main__":
    gps3 = GPS3()

    while True:  # All data is available via instantiated thread data stream attribute.
        print(gps3.getlatlon())
        print(gps3.gettime())
        print(gps3.getmovement())
        # # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
        # print('---------------------')
        # print(                   agps_thread.data_stream.time)
        # print('Lat:{}   '.format(agps_thread.data_stream.lat))
        # print('Lon:{}   '.format(agps_thread.data_stream.lon))
        # print('Speed:{} '.format(agps_thread.data_stream.speed))
        # print('Course:{}'.format(agps_thread.data_stream.track))
        # print('---------------------')
        sleep(2)  # Sleep, or do other things for as long as you like.