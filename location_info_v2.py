from gps3 import agps3


class GPS3():
    """ GPS module to communicate with GPS receiver using gpsd """

    def __init__(self):
        gpsd.connect()
        self.all_data = None
        

    def get_data(self):
        self.all_data = gpsd.get_current()

    def del_data(self):
        self.all_data = None

    def get_mode(self):
        return self.all_data.mode

    def get_time(self):
        return self.all_data.time

    def get_lat(self):
        return self.all_data.lat

    def get_lon(self):
        return self.all_data.lon

    def get_track(self):
        return self.all_data.track

    def get_speed(self):
        return self.all_data.speed()




if __name__ == "__main__":
    import time
    gps = GPSD()
    while True:
        try:
            gps.get_data()
            if gps.get_mode() > 2:
                print("Time: {}, Latitude: {}, Longitude: {}, Track: (), Speed: {}".format(
                    gps.get_time(), gps.get_lat(), gps.get_lon(), gps.get_track(), gps.get_speed()))
            time.sleep(1)
            # gps.del_data()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("User stopped the process")
            break
