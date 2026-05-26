#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import time

rospy.init_node("route_drive")

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
time.sleep(1)

def move(linear, angular, duration):
    cmd = Twist()
    cmd.linear.x = linear
    cmd.angular.z = angular

    start = time.time()
    rate = rospy.Rate(10)

    while time.time() - start < duration and not rospy.is_shutdown():
        pub.publish(cmd)
        rate.sleep()

    stop()

def stop():
    cmd = Twist()
    pub.publish(cmd)
    time.sleep(0.5)

# Havaalanı koridor rotası
move(0.18, 0.0, 5)      # ileri git
move(0.0, 0.7, 2.2)     # sola dön
move(0.18, 0.0, 4)      # ileri git
move(0.0, -0.7, 2.2)    # sağa dön
move(0.18, 0.0, 5)      # ileri git
move(0.0, -0.7, 2.2)    # sağa dön
move(0.18, 0.0, 4)      # ileri git
move(0.0, 0.7, 2.2)     # sola dön
move(0.18, 0.0, 5)      # ileri git

stop()
