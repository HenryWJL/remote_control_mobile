from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from socket import *

root = Builder.load_string("""
FloatLayout:

    canvas.before:

        Rectangle: 
            size: self.size
            source: './data/background.png'
               
    ActionButton:
        icon: './data/icons/up_arrow.png'
        center: root.width / 2, root.height / 2 -100
        on_press: app.go_forward()
        on_release: app.stop()
        
    ActionButton:
        icon: './data/icons/down_arrow.png'
        center: root.width / 2, root.height / 2 -200
        on_press: app.go_backward()
        on_release: app.stop()
        
    ActionButton:
        icon: './data/icons/left_arrow.png'
        center: root.width / 2 - 50, root.height / 2 - 150
        on_press: app.go_left()
        on_release: app.stop()

    ActionButton:
        icon: './data/icons/right_arrow.png'
        center: root.width / 2 + 50, root.height / 2 - 150
        on_press: app.go_right()
        on_release: app.stop()
        
    ActionButton:
        icon: './data/icons/circle.png'
        center: root.width / 2, root.height / 2 - 150
        on_press: app.grasp()
        on_release: app.stop()
""")


# class Interface(FloatLayout):
#     command = StringProperty('stop')
#     dataSocket = socket(AF_INET, SOCK_STREAM)
#     on_connection = True
#     try:
#         dataSocket.connect(('127.0.0.1', 8000))
#     except ConnectionError:
#         on_connection = False
        

#     def send_message(self, *args):
#         self.dataSocket.send(self.command.encode())


#     def go_forward(self, *args):
#         self.command = 'forward'
            
    
#     def go_backward(self, *args):
#         self.command = 'backward'
            
            
#     def go_left(self, *args):
#         self.command = 'left'
            
            
#     def go_right(self, *args):
#         self.command = 'right'
            
    
#     def grasp(self, *args):
#         self.command = 'grasp'
        
    
#     def stop(self, *args):
#         self.command = 'stop'

# class Interface(FloatLayout):
#     pass


class RemoteControlApp(App):
    command = StringProperty('stop')
    dataSocket = socket(AF_INET, SOCK_STREAM)
    on_connection = True
    try:
        dataSocket.connect(('127.0.0.1', 8000))
    except ConnectionError:
        on_connection = False
        
        
    def build(self):
        Clock.schedule_interval(self.send_message, 1.0)
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
