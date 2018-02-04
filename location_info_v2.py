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
        agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
        agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
        agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default 0.2 second, default daemon=True


    def getlatlon(self):
        return agps_thread.data_stream.lat, agps_thread.data_stream.lon

    def gettime(self):
        return agps_thread.data_stream.time


if __name__ == "__main__":
    gps3 = GPS3()

    while True:  # All data is available via instantiated thread data stream attribute.
        print(gps3.getlatlon())
        # # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
        # print('---------------------')
        # print(                   agps_thread.data_stream.time)
        # print('Lat:{}   '.format(agps_thread.data_stream.lat))
        # print('Lon:{}   '.format(agps_thread.data_stream.lon))
        # print('Speed:{} '.format(agps_thread.data_stream.speed))
        # print('Course:{}'.format(agps_thread.data_stream.track))
        # print('---------------------')
        sleep(2)  # Sleep, or do other things for as long as you like.