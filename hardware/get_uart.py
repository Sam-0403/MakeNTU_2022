import serial
from time import sleep

class UART_controller():
    ser = None
    def __init__(self):
        self.ser = serial.Serial ("/dev/ttyAMA0", 115200)    #Open port with baud rate
    
    def receive(self):
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        return received_data


if __name__ == "__main__":

    ser = serial.Serial ("/dev/ttyAMA0", 115200)    #Open port with baud rate
    print("Configure UART Success!")
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)                   #print received data
        # ser.write(received_data)                #transmit data serially 