from gps3 import agps3
import time

class AGPS():
    ''' Module for GPS communication using gpsd '''

    def __init__(self):
        self.gpsd_socket = agps3.GPSDSocket()
        self.gpsd_socket.connect()
        self.gpsd_socket.watch()
        self.data_stream = agps3.DataStream()


    def shutdown(self):
        self.gpsd_socket.close()


    def get_new_data(self):
        ''' check for new data in data stream '''
        for new_data in self.gpsd_socket:
            if new_data:
                self.data = self.data_stream.unpack(new_data)
            else:
                time.sleep(0.3)
                self.data = None
            return self.data

    def get_latlon(self, data):
        ''' Check and get latitude and longitude '''
        pass


if __name__ == '__main__':
    gps = AGPS()

    try:
        while True:
            gps_data = gps.get_new_data()
            print(gps_data)
    except KeyboardInterrupt:
        gps.shutdown()