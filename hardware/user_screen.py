from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from send_data import send_data

typeList = ['Garbage', 'Paper', 'Plastic', 'Metal', 'Glass', 'Organic', 'Other']

Builder.load_file("user_screen.kv")

class TypeDropDown(BoxLayout):
    def __init__(self, **kwargs):
        super(TypeDropDown, self).__init__(**kwargs)
        self.dropdown = DropDown()
        for garbage_type in typeList:

            btn = Button(text=garbage_type, size_hint_y=None, height=80)
            btn.font_size = '30sp'

            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))

            self.dropdown.add_widget(btn)

        self.mainbutton = Button(text='Hello')
        self.mainbutton.font_size = '35sp'

        self.mainbutton.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
    
    def on_parent(self, widget, parent):
        self.add_widget(self.mainbutton)

class UserScreen(Screen):
    userName = StringProperty('')
    userPoint = NumericProperty(0)
    typeDropDown = ObjectProperty()

    def __init__(self, userName, userPoint, onSubmit, type, email, **kwargs):
        super(UserScreen, self).__init__(**kwargs)
        data  = {
            "type": type,
            "email": email
        }
        send_data('https://sam-cheng-user-auth.herokuapp.com/sendData', {"type": type, "email": email})
        self.userName = userName
        self.userPoint = userPoint
        self.switch_to_login = onSubmit
        self.typeDropDown.add_widget(TypeDropDown())

    def on_Submit(self):
        self.switch_to_login()