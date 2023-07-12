import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from socket import *
from cv_bridge import CvBridge


def callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    

if __name__ == '__main__':
    image = None
    try:
        rospy.init_node("server", anonymous=True)
        image_topic = rospy.get_param("image_topic", default="/camera/color/image_raw")
        rospy.Subscriber(image_topic, Image, callback, queue_size=10)
        publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        listenSocket = socket(AF_INET, SOCK_STREAM)
        listenSocket.bind(('10.27.250.165', 8000))
        listenSocket.listen(1)
        rospy.loginfo('The server has already started')
        dataSocket, address = listenSocket.accept()
        rospy.loginfo('Connected to ', address)
        
        while not rospy.is_shutdown():
            if not image:
                rospy.logwarn('No image data available!')
                continue
                
            data = dataSocket.recv(512)
            if not data:
                rospy.loginfo('Connection is lost')
                break
            
            command = data.decode('utf-8')
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
                
            encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 8]
            result, image_encode = cv2.imencode('.png', image, encode_params)
            data = np.array(image_encode)
            data = data.tobytes()
            dataSocket.send(str(len(data)).ljust(16).encode())
            dataSocket.send(data)
        
        dataSocket.close()
        listenSocket.close()
        
    except (ConnectionError, OSError):
        rospy.logerr('Connection failed')
