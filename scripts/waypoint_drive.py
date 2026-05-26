#!/usr/bin/env python3

import rospy, math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

x = y = yaw = 0.0

def odom_callback(msg):
    global x, y, yaw
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    q = msg.pose.pose.orientation
    _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

def ang(a):
    while a > math.pi: a -= 2 * math.pi
    while a < -math.pi: a += 2 * math.pi
    return a

rospy.init_node("waypoint_drive")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
rospy.Subscriber("/odom", Odometry, odom_callback)

rate = rospy.Rate(10)
rospy.sleep(2)

# SADECE GÜVENLİ BOŞ ALANDA DOLAŞIR
waypoints = [
    (0.5, 0.0),
    (1.0, 0.0),
    (1.0, -0.8),
    (0.2, -0.8),
    (0.2, 0.0),
]

for gx, gy in waypoints:
    while not rospy.is_shutdown():
        dx = gx - x
        dy = gy - y
        dist = math.sqrt(dx*dx + dy*dy)

        target = math.atan2(dy, dx)
        err = ang(target - yaw)

        cmd = Twist()

        if dist < 0.15:
            break

        if abs(err) > 0.15:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5 if err > 0 else -0.5
        else:
            cmd.linear.x = 0.12
            cmd.angular.z = 0.2 * err

        pub.publish(cmd)
        rate.sleep()

    pub.publish(Twist())
    rospy.sleep(0.5)

pub.publish(Twist())
