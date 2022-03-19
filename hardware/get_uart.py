import serial
from time import sleep, time
import io
import PIL.Image as Image

class UART_controller():
    ser = None
    def __init__(self):
        self.ser = serial.Serial ("/dev/ttyAMA0", 115200)    #Open port with baud rate
    
    def receive(self):
        received_data = self.ser.read()              #read serial port
        sleep(0.03)
        data_left = self.ser.inWaiting()             #check for remaining byte
        received_data += self.ser.read(data_left)
        return received_data

    def receive_time(self, dt):
        time_end = time() + dt

        received_data = self.ser.read()
        sleep(0.03)
        data_left = self.ser.inWaiting()             #check for remaining byte
        received_data += self.ser.read(data_left)
        while time()<time_end:
            received_data += self.ser.read()              #read serial port
            sleep(0.03)
            data_left = self.ser.inWaiting()             #check for remaining byte
            received_data += self.ser.read(data_left)

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

    ser = serial.Serial ("/dev/ttyAMA0", 115200)    #Open port with baud rate
    print("Configure UART Success!")
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)                   #print received data
        # ser.write(received_data)                #transmit data serially 