import rospy
from geometry_msgs.msg import Twist
from socket import *


if __name__ == '__main__':
    try:
        rospy.init_node("server", anonymous=True)
        publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        listenSocket = socket(AF_INET, SOCK_STREAM)
        listenSocket.bind(('127.0.0.1', 8000))
        listenSocket.listen(1)
        print('The server has already started')
        dataSocket, address = listenSocket.accept()
        print('Connected to ', address)
        
        while True:
            data = dataSocket.recv(512)
            if not data:
                break
            
            command = data.decode('utf-8')
            print(command)
            
            if command == 'stop':
                message = Twist()
                publisher.publish(message)
            
            elif command == 'forward':
                message = Twist()
                message.linear.x = 1.5
                publisher.publish(message)
                
            elif command == 'backward':
                message = Twist()
                message.linear.x = -1.5
                publisher.publish(message)
                
            elif command == 'left':
                message = Twist()
                message.angular.z = 0.5
                publisher.publish(message)
                
            elif command == 'right':
                message = Twist()
                message.angular.z = -0.5
                publisher.publish(message)
                
            elif command == 'grasp':
                pass
                
            dataSocket.send(data)
        
        dataSocket.close()
        listenSocket.close()
        
    except ConnectionError:
        print('Connection failed')
