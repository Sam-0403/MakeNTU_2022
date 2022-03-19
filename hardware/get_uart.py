import serial
from time import sleep

if __name__ == "__main__":

    ser = serial.Serial ("/dev/serial0", 115200)    #Open port with baud rate
    while True:
        # received_data = ser.read()              #read serial port
        sleep(0.03)
        # data_left = ser.inWaiting()             #check for remaining byte
        # received_data += ser.read(data_left)
        print (ser.read())                   #print received data
        # ser.write(received_data)                #transmit data serially 