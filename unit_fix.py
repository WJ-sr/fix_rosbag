import rosbag
from geometry_msgs.msg import Twist, Accel
from sensor_msgs.msg import PointCloud2
import os, os.path
import math

DIR = './rosbags'
A_DIR = './fixed_rosbags'

def degps_to_radps(degps):
    radps = math.radians(degps)
    return radps


for i in range(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])):
    bag = rosbag.Bag(os.path.join(DIR, os.listdir(DIR)[i]))
    
    with rosbag.Bag(os.path.join(A_DIR, os.listdir(DIR)[i]), 'w') as outbag:
        for topic, msg, t in bag.read_messages():
            fix_velocity_msg = Twist()
            accel_msg = Accel()
            pointcloud_msg = PointCloud2()
            if topic == "/velocity":
                fix_velocity_msg.linear.x = msg.linear.x
                fix_velocity_msg.linear.y = msg.linear.y
                fix_velocity_msg.linear.z = msg.linear.z
                fix_velocity_msg.angular.z = degps_to_radps(msg.angular.z)
                outbag.write('/velocity', fix_velocity_msg, t)
            elif topic == "/acceleration":
                accel_msg = msg
                outbag.write('/acceleration', accel_msg, t)
            else:
                pointcloud_msg = msg
                outbag.write('/sr_perception1/pandar', pointcloud_msg, t)
    bag.close()