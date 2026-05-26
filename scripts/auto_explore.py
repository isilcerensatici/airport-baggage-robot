#!/usr/bin/env python3

import rospy, math, time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

pub = None
cmd = Twist()
last_turn_time = 0

def clean(values):
    vals = [v for v in values if not math.isinf(v) and not math.isnan(v)]
    return min(vals) if vals else 10.0

def scan_callback(msg):
    global cmd, last_turn_time

    front = clean(msg.ranges[0:25] + msg.ranges[-25:])
    left  = clean(msg.ranges[50:120])
    right = clean(msg.ranges[240:310])

    cmd = Twist()

    # Çok yakına girdiyse: geri kaç + dön
    if front < 0.45:
        cmd.linear.x = -0.10
        cmd.angular.z = 1.0
        return

    # Ön kapalıysa daha boş tarafa dön
    if front < 0.85:
        cmd.linear.x = 0.0
        if right > left:
            cmd.angular.z = -0.9
        else:
            cmd.angular.z = 0.9
        return

    # Sağ taraf çok yakınsa hafif sola kaç
    if right < 0.45:
        cmd.linear.x = 0.10
        cmd.angular.z = 0.5
        return

    # Sol taraf çok yakınsa hafif sağa kaç
    if left < 0.45:
        cmd.linear.x = 0.10
        cmd.angular.z = -0.5
        return

    # Normal ilerle
    cmd.linear.x = 0.18
    cmd.angular.z = 0.0

rospy.init_node("auto_explore")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
rospy.Subscriber("/scan", LaserScan, scan_callback)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    pub.publish(cmd)
    rate.sleep()
