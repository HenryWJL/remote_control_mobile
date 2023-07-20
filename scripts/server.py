import rospy
import cv2
import numpy as np
import time
from math import pi
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from swiftpro.msg import position
from socket import *
from cv_bridge import CvBridge


def callback(data):
    global dataSocket
    global moving_publisher
    global grasping_publisher
    global on_connection
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(data, "bgr8")

    data = dataSocket.recv(512)
    if not data:
        rospy.logwarn('No data received!')
        time.sleep(2)
    else:
        command = data.decode('utf-8')
        if command == 'stop':
            message = Twist()
            moving_publisher.publish(message)

        elif command == 'forward':
            message = Twist()
            message.linear.x = 1.5
            moving_publisher.publish(message)
            
        elif command == 'backward':
            message = Twist()
            message.linear.x = -1.5
            moving_publisher.publish(message)
            
        elif command == 'left':
            message = Twist()
            message.angular.z = 0.5
            moving_publisher.publish(message)
            
        elif command == 'right':
            message = Twist()
            message.angular.z = -0.5
            moving_publisher.publish(message)
            
        elif command == 'grasp':
            message = position()
            message.x = 300
            message.z = -45
            grasping_publisher.publish(message)
        
        elif command == 'withdraw':
            message = position()
            message.x = 120
            grasping_publisher.publish(message)

        # Pre-processing and sending the image data
        encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 8]
        result, image_encode = cv2.imencode('.png', image, encode_params)
        data = np.array(image_encode)
        data = data.tobytes()
        dataSocket.send(str(len(data)).ljust(16).encode())
        dataSocket.send(data)
            

if __name__ == '__main__':
    dataSocket = None
    moving_publisher = None
    grasping_publisher = None
    try:
        rospy.init_node("server", anonymous=True)
        
        listenSocket = socket(AF_INET, SOCK_STREAM)
        listenSocket.bind(('10.27.250.165', 8000))
        listenSocket.listen(1)
        rospy.loginfo('The server has already started')
        dataSocket, address = listenSocket.accept()
        rospy.loginfo('Connected to the remote control')
        
        moving_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        grasping_publisher = rospy.Publisher('/position_write_topic', position, queue_size=10)
        image_topic = rospy.get_param("/image_topic", default="/camera/color/image_raw")
        rospy.Subscriber(image_topic, Image, callback, queue_size=10)
        
        rospy.spin()        
        
    except (ConnectionError, OSError):
        rospy.logerr('Connection failed')
        dataSocket.close()
        listenSocket.close()
        
