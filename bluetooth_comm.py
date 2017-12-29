import os
import glob
import time
from bluetooth import *

class BluetoothComm():
    """ module for bluetooth communication with android smartphone """
    def __init__(self):
        self.UUID = "f9b4f58d-63ea-4d6e-831b-271a6ad0e5e2"
        try:
            self.server_sock = BluetoothSocket(RFCOMM)
            self.server_sock.bind(("", PORT_ANY))
            self.server_sock.listen(1)
            self.port = self.server_sock.getsockname()[1]
            advertise_service(self.server_sock, "MSAS",
                              service_id = self.UUID,
                              service_classes = [self.UUID, SERIAL_PORT_CLASS],
                              profiles = [SERIAL_PORT_PROFILE])
        except:
            print("Unable to create bluetooth service")


    def accept_connection(self):
        """ starting of bluetooth service to listen for connections """
        self.client_sock, self.client_info = self.server_sock.accept()
        return self.client_sock, self.client_info

    def recv_data(self):
        """ receive data from connected device """
        try:
            self.data = self.client_sock.recv(1024)
            if len(self.data) == 0:
                return "Nothing received from client" + self.client_info
            else:
                return self.data
        except IOError:
            return "Nothing connected/sending data"

if __name__ == "__main__":
    bluetooth = BluetoothComm()
    try:
        while True:
            client_sock, client_info = bluetooth.accept_connection()
            print("Accepted connection from {}".format(client_info))
            connected = True
            while connected == True:
                try:
                    data = bluetooth.recv_data()
                    print("Received: {}".format(data))
                    if data.decode('UTF-8') == "disconnect":
                        print("Client request to disconnect")
                        break
                    else:
                        reply = "You sent me this: " + data
                        client_sock.send(reply)
                except IOError:
                    print("IO error detected")
                    connected = False
                except KeyboardInterrupt:
                    print("User cancelled operation")
                    connected = False
            client_sock.close()
    except KeyboardInterrupt:
        print("User cancelled operation")
        bluetooth.server_sock.close()


