from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager
from user_screen import UserScreen
from login_screen import LoginScreen

from kivy.clock import Clock
from functools import partial

import RPi.GPIO as GPIO

Config.set('graphics', 'resizable', True)

typeList = ['Garbage', 'Paper', 'Plastic', 'Metal', 'Glass', 'Organic', 'Other']

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

currentUser = "Sam Cheng"

class ClassificationApp(App):
    user = ''
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(self.on_login, name="LoginScreen"))
        # self.user = UserScreen(currentUser, 100, self.on_submit, name="UserScreen")
        # self.sm.add_widget(self.user)

        return self.sm

    def switch_to_user(self, name, *largs):
        if self.user != '':
            self.sm.remove_widget(self.user)
        self.user = UserScreen(name, 100, self.on_submit, name="UserScreen")
        self.sm.add_widget(self.user)
        self.sm.current = "UserScreen"

    def switch_to_login(self):
        self.sm.current = "LoginScreen"

    def on_login(self, name):
        Clock.schedule_once(partial(self.switch_to_user, name), 1)

    def on_submit(self):
        self.switch_to_login()


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.OUT)
    Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    Window.clearcolor = (0x6a/0xff, 0x5a/0xff, 0xcd/0xff, 1)
    classificationApp = ClassificationApp()
    classificationApp.run()
        