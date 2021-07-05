#!/usr/bin/env python3
import rospy
import sys
from std_msgs.msg import String
import os

def say(data):
    os.system('espeak -p 0 -s150 "' + data.data + '"')

def init():
    rospy.init_node("synthesizer", anonymous=True)
    rospy.Subscriber("chat_output", String, say)

def synthesizer():
    rospy.spin()

if __name__ == '__main__':
    init()
    synthesizer()
