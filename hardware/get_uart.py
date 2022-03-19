import serial
from time import sleep, time
import io
import PIL.Image as Image

class UART_controller():
    ser = None
    def __init__(self):
        # self.ser = serial.Serial ("/dev/ttyAMA0", 115200, timeout=10)    #Open port with baud rate
        self.ser = serial.Serial ("/dev/ttyAMA0", 115200)
    
    def receive(self):
        received_data = self.ser.read()              #read serial port
        sleep(0.03)
        data_left = self.ser.inWaiting()             #check for remaining byte
        received_data += self.ser.read(data_left)
        return received_data

    def receive_time(self, message):
        print("Writing Data!")
        self.ser.write(message)
        print("Receiving Data!")

        # received_data = self.ser.read()
        # sleep(0.03)
        # data_left = self.ser.inWaiting()             #check for remaining byte
        # received_data += self.ser.read(data_left)
        # print("First Receive")
        # while time()<time_end:
        #     print("Looping")
        #     received_data += self.ser.read()              #read serial port
        #     sleep(0.03)
        #     data_left = self.ser.inWaiting()             #check for remaining byte
        #     received_data += self.ser.read(data_left)
        # print("Receiving Data Finish!")
        sleep(10)
        received_data = self.ser.read_all()
        print(len(received_data))
        print("Receiving Data Finish!")
        try:
            image = Image.open(io.BytesIO(received_data))
            image.save('temp.jpg')
            print("Save Success")
        except:
            print("Save Error")
        # return received_data

    def write(self, message):
        self.ser.write(message)


if __name__ == "__main__":

    ser = serial.Serial ("/dev/ttyAMA0", 115200)
    # ser = serial.Serial ("/dev/ttyAMA0", 115200, timeout=10)    #Open port with baud rate
    print("Configure UART Success!")
    ser.write(b'S')

    # sleep(5)
    # received_data = ser.read_all()
    # print(len(received_data))
    # print("Receiving Data Finish!")

    # sleep(30)
    # received_data = ser.read_all()
    # print (received_data)

    while True:
        # received_data = ser.read(153600)              #read serial port
        ser.write(b'S')
        received_data = ser.read()
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)                   #print received data
        # ser.write(received_data)                #transmit data serially 