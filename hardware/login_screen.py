from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
from send_data import send_data
from kivy.clock import Clock
from functools import partial
from get_rfid import read_RFID

# login_url = 'http://127.0.0.1:8000/userLogin'
# register_url = 'http://127.0.0.1:8000/userRegister'
login_url = 'https://sam-cheng-user-auth.herokuapp.com/userLogin'
register_url = 'https://sam-cheng-user-auth.herokuapp.com/userRegister'

Builder.load_file("login_screen.kv")

class RFIDInput(BoxLayout):
    label = ObjectProperty()
    input = ObjectProperty()
    def __init__(self, onText, **kwargs):
        super(RFIDInput, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        # self.padding = [20, 20, 20, 20]
        self.label = Label(text='ID Card: ',font_size='30sp')
        self.input = TextInput(password=True, hint_text='Connect Your ID Card', font_size='20sp')
        self.ids['rfidInput'] = self.input
        self.on_text = onText
        self.input.bind(text=self.onText)
        self.add_widget(self.label)
        self.add_widget(self.input)
    def onText(self):
        self.on_text()
    
    # def on_parent(self, widget, parent):
    #     self.add_widget(self.rfidInput)

class LoginScreen(Screen):
    userName = StringProperty('None')
    state = StringProperty('Login')
    email = ''
    password = ''
    rfid = ''
    rfidInput = ObjectProperty()
    def __init__(self, onLogin, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.onLogin = onLogin
        self.userName = "Sam Cheng"
        Clock.schedule_interval(self.rfid_read, 1)

    def rfid_read(self, dt):
        read_RFID()

    def on_login(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        user = send_data(login_url, data).json()
        self.userName = user['name']
        if self.userName!="None":
            self.email = ''
            self.ids.emailInput.text = ''
            self.password = ''
            self.ids.passwordInput.text = ''
            self.onLogin(self.userName)

    def on_register(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        user = send_data(login_url, data).json()
        self.userName = user['name']
        if self.userName!="None":
            self.email = ''
            self.ids.emailInput.text = ''
            self.password = ''
            self.ids.passwordInput.text = ''
            self.onLogin(self.userName)

    # def on_start(self):
    #     Clock.schedule_interval(partial(read_RFID), 1)
        
    def on_state_change(self):
        if self.state == 'Login':
            self.state = 'Register'
            if self.rfidInput==None:
                self.rfidInput = RFIDInput(self.on_rfid_text)
            # self.ids.emailLayout.padding = [20, 20, 20, 20]
            # self.ids.passwordLayout.padding = [20, 20, 20, 20]
            self.ids.inputForm.add_widget(self.rfidInput)
        else:
            self.state = 'Login'
            if self.rfidInput!=None:
                # self.ids.emailLayout.padding = [50, 50, 50, 50]
                # self.ids.passwordLayout.padding = [50, 50, 50, 50]
                self.ids.inputForm.remove_widget(self.rfidInput)
    
    def on_email_text(self):
        self.email = self.ids.emailInput.text

    def on_password_text(self):
        self.password = self.ids.passwordInput.text

    def on_rfid_text(self):
        self.rfid = self.rfidInput.ids.rfidInput.text

