import numpy as np
import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from socket import *

root = Builder.load_string("""
FloatLayout:

    prompt: label
    image: real_time_image

    canvas.before:

        Rectangle: 
            size: self.size
            source: './data/background.png'
        
    Image:
        id: real_time_image
        source: 'data/image.png'
        size: self.texture_size
        center: self.width / 2, self.height / 2 + 105
               
    Button:
        background_normal: './data/icons/up_arrow.png'
        size_hint: .1, .1
        center: root.width / 2, root.height / 2 - 100
        on_press: app.go_forward()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/down_arrow.png'
        size_hint: .1, .1
        center: root.width / 2, root.height / 2 - 250
        on_press: app.go_backward()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/left_arrow.png'
        size_hint: .1, .1
        center: root.width / 2 - 75, root.height / 2 - 175
        on_press: app.go_left()
        on_release: app.stop()

    Button:
        background_normal: './data/icons/right_arrow.png'
        size_hint: .1, .1
        center: root.width / 2 + 75, root.height / 2 - 175
        on_press: app.go_right()
        on_release: app.stop()
        
    Button:
        background_normal: './data/icons/circle.png'
        size_hint: .1, .1
        center: root.width / 2, root.height / 2 - 175
        on_press: app.grasp()
        on_release: app.withdraw()

    Label:
        id: label
        font_size: 50  
        color: 1, 0, 0, 1
        center: self.center
""")


class RemoteControlApp(App):
    command = StringProperty('stop')
    image = StringProperty('data/image.png')
    dataSocket = socket(AF_INET, SOCK_STREAM)
    on_connection = True
    try:
        dataSocket.connect(('10.27.250.165', 8000))  
    except (ConnectionError, OSError):
        on_connection = False
        
        
    def build(self):
        send_event = Clock.schedule_interval(self.send_message, 1.0)
        receive_event = Clock.schedule_interval(self.receive_message, 1.0)
        if not self.on_connection:
            send_event.cancel()
            receive_event.cancel()
            root.prompt.text = 'Connection Failed!'
        return root
    
    
    def send_message(self, *args):
        self.dataSocket.send(self.command.encode())
    
    
    def receive(self, length):
        buffer = b''
        while length:
            data = self.dataSocket.recv(length)
            if not data:
                return None
            buffer += data
            length -= len(data)
        return buffer    
        
        
    def receive_message(self, *args):
        length = self.receive(16)
        data = self.receive(int(length))
        if not data:
            self.dataSocket.close()
            root.prompt.text = 'Connection is Lost!'
        else:
            data = np.frombuffer(data, dtype='uint8')
            image_decode = cv2.imdecode(data, cv2.IMREAD_COLOR)
            cv2.imwrite('data/image.png', image_decode)
            root.image.reload()
            

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


    def withdraw(self, *args):
        self.command = 'withdraw'
        
    
    def stop(self, *args):
        self.command = 'stop'


if __name__ == '__main__':
    RemoteControlApp().run()

        
