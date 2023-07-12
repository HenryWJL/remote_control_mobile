from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from socket import *

root = Builder.load_string("""
FloatLayout:

    prompt: label

    canvas.before:

        Rectangle: 
            size: self.size
            source: './data/background.png'
               
    Button:
        background_normal: './data/icons/up_arrow.png'
        size_hint: .234, .108
        center: root.width / 2, root.height / 2 - 100
        on_press: app.go_forward()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/down_arrow.png'
        size_hint: .234, .108
        center: root.width / 2, root.height / 2 - 250
        on_press: app.go_backward()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/left_arrow.png'
        size_hint: .234, .108
        center: root.width / 2 - 75, root.height / 2 - 175
        on_press: app.go_left()
        on_release: app.stop()

    Button:
        background_normal: './data/icons/right_arrow.png'
        size_hint: .234, .108
        center: root.width / 2 + 75, root.height / 2 - 175
        on_press: app.go_right()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/circle.png'
        size_hint: .234, .108
        center: root.width / 2, root.height / 2 - 175
        on_press: app.grasp()
        on_release: app.stop()
        
    Label:
        id: label
        font_size: 50  
        color: 1, 0, 0, 1
        center: self.center
""")


class RemoteControlApp(App):
    command = StringProperty('stop')
    dataSocket = socket(AF_INET, SOCK_STREAM)
    on_connection = True
    try:
        dataSocket.connect(('172.17.239.255', 8000))  
    except (ConnectionError, OSError):
        on_connection = False
        
        
    def build(self):
        event = Clock.schedule_interval(self.send_message, 1.0)
        if not self.on_connection:
            event.cancel()
            root.prompt.text = 'Connection Failed!'
        return root
    
    
    def send_message(self, *args):
        self.dataSocket.send(self.command.encode())


    def go_forward(self, *args):
        self.command = 'forward'
            
    
    def go_backward(self, *args):
        self.command = 'backward'
            
            
    def go_left(self, *args):
        self.command = 'left'
            
            
    def go_right(self, *args):
        self.command = 'right'
            
    
    def grasp(self, *args):
        self.command = 'grasp'
        
    
    def stop(self, *args):
        self.command = 'stop'


if __name__ == '__main__':
    RemoteControlApp().run()

        
