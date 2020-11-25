#!/usr/bin/env python
import sys
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
rows = 0
cols = 0
channels = 0

def callback(data):
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    m = cv_image[:,:,0] > 200
    c = np.argwhere(m == True)
    k = c.shape[0]
    sum = c.sum(axis = 0)
    x = sum[0]
    y = sum[1]
    coord_x = x/k
    coord_y = y/k
    done = False
    cv_image[coord_x][coord_y] = (0,0,255)
    if (coord_x < 130 and coord_x > 100 and coord_y < 130 and coord_y > 100):
        done = True
    if (done):
        cv2.rectangle(cv_image,(100,100),(230,230),(0,255,0),3)
    else:
        cv2.rectangle(cv_image,(100,100),(230,230),(0,0,255),3)
    image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    done_pub.publish(Bool(done))

rospy.init_node('node_camera', anonymous=True)

image_pub = rospy.Publisher("image_topic_2",Image, queue_size=100)
done_pub = rospy.Publisher("isDone", Bool, queue_size=100)
image_sub = rospy.Subscriber("/robot/camera1/image_raw", Image, callback)
rate = rospy.Rate(50)

rospy.spin()
