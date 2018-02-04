from gps3 import agps3
import time

class AGPS():
    ''' Module for GPS communication using gpsd '''

    def __init__(self):
        self.gpsd_socket = agps3.GPSDSocket()
        self.gpsd_socket.connect()
        self.gpsd_socket.watch()
        self.data_stream = agps3.DataStream()
        self.location_info = {"time": None, "lat": None, "lon": None, "speed": None, "track": None}
        self.timestamp = None


    def shutdown(self):
        self.gpsd_socket.close()


    def get_new_data(self):
        ''' check for new data in data stream '''
        for new_data in self.gpsd_socket:
            if new_data:
                self.data_stream.unpack(new_data)
                if self.timestamp == None: self.timestamp = self.data_stream.time
                if self.data_stream.lat != "n/a" and self.data_stream.lon != "n/a":
                    self.location_info["lat"] = self.data_stream.lat
                    self.location_info["lon"] = self.data_stream.lon
                    self.location_info["time"] = self.data_stream.time
                if self.data_stream.speed != "n/a": self.location_info["speed"] = self.data_stream.speed
                if self.data_stream.track != "n/a": self.location_info["track"] = self.data_stream.track
                return
            else:
                time.sleep(0.3)
                # self.data = None
                #print(self.data_stream)



if __name__ == '__main__':
    gps = AGPS()

    try:
        while True:
            # gps_data = gps.get_new_data()
            gps.get_new_data()
            if gps.timestamp != None and gps.timestamp != "n/a":
                print(gps.location_info)
                gps.timestamp = gps.location_info["time"]
    except KeyboardInterrupt:
        gps.shutdown()
