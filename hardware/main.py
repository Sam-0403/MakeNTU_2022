from time import sleep
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager
from user_screen import UserScreen
from login_screen import LoginScreen

from kivy.clock import Clock
from functools import partial

# import RPi.GPIO as GPIO
# from get_rfid import read_RFID
from classify import Decide
from get_uart import UART_controller
from threading import Thread
import os

Config.set('graphics', 'resizable', True)

typeList = ['Garbage', 'Paper', 'Plastic', 'Metal', 'Glass', 'Organic', 'Other']

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

currentUser = "Sam Cheng"

class ClassificationApp(App):
    user = ''
    ai_model = None
    uart_controller = None
    def build(self):
        self.ai_model = Decide("0319_best.pth")
        self.uart_controller = UART_controller()
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(self.on_login, name="LoginScreen"))
        # self.user = UserScreen(currentUser, 100, self.on_submit, name="UserScreen")
        # self.sm.add_widget(self.user)

        return self.sm

    def switch_to_user(self, name, email, *largs):
        if self.user != '':
            self.sm.remove_widget(self.user)
        self.write_start()
        # self.save_image()
        self.sm.add_widget(self.user)
        self.sm.current = "UserScreen"
        sleep(5)
        # self.ai_model.image_loader("S__10313763.jpg")
        # self.ai_model.image_loader(r"/media/pi/_s_W_Ma_/example.jpg")
        os.chdir('/media/pi/_s_W_Ma_1')
        answer = self.ai_model.image_loader(os.path.abspath('example.jpg'))
        self.user = UserScreen(name, 100, self.on_submit, answer, email, name="UserScreen")
        # print(os.getcwd())

    def switch_to_login(self):
        self.sm.current = "LoginScreen"

    def on_login(self, name, email):
        Clock.schedule_once(partial(self.switch_to_user, name, email), 1)

    def on_submit(self):
        self.switch_to_login()

    def check_received(self, dt):
        print(self.uart_controller.receive())

    def write_start(self):
        self.uart_controller.write(b'S')

    # def save_image(self):
        # t = Thread(target=self.uart_controller.receive_time, args=(b'S',))
        # set daemon to true so the thread dies when app is closed
        # t.daemon = True
        # # start the thread
        # t.start()

    # def on_start(self):
    #     Clock.schedule_interval(partial(self.check_received), 1)


if __name__ == '__main__':
    Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    Window.clearcolor = (0x6a/0xff, 0x5a/0xff, 0xcd/0xff, 1)
    classificationApp = ClassificationApp()
    classificationApp.run()
        