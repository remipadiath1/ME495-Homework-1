#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import math
import turtlesim
import sys




def turtle_control(T):
	global pub
	pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	rospy.init_node("turtle_velocity", anonymous=True)
	twist = Twist()

	rospy.wait_for_service('turtle1/teleport_absolute')
#	test = rospy.ServiceProxy('turtle1/teleport_absolute', turtlesim/TeleportAbsolute)
#	test(0,0,0)
	r = rospy.Rate(100)
	i= 0.1
	T=T*1
	while not rospy.is_shutdown():
#	while i>=T:
		x, z = find_velocity(i,T)
		twist.linear.x = x
		twist.angular.z = z
		pub.publish(twist)
		i = i+1
		r.sleep()
	#rospy.spin()



def find_velocity(newt,T):
	T = T
	t=newt
	xd = 3*math.sin((4*math.pi*t)/T)
	yd = 3*math.sin((2*math.pi*t)/T)
	xddot = ((12*math.pi)/(T))*math.cos((4*math.pi*t)/T)
	yddot = ((6*math.pi)/(T))*math.cos((2*math.pi*t)/T)
	v = math.sqrt((xddot*xddot)+(yddot*yddot))
	theta = math.atan2(xddot,yddot)
#I really don't know how to find out theta dot here. My mathematica does not work
	w = v/(math.sqrt((xd*xd)+(yd*yd)))
	return v,w



if __name__ == '__main__':
	if len(sys.argv) == 2:
		T = int(sys.argv[1])
	else:
		T = 5
	turtle_control(T)


