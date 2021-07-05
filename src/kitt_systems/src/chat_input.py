#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import time

input_publisher = rospy.Publisher("chat_input",String,queue_size=1)

def init():
    rospy.init_node('text_input', anonymous=True)

def text_input():
    in_text = input("Input: ")
    if in_text == 'exit':
        exit()
    else:
        input_publisher.publish(in_text)
    time.sleep(1)
    text_input()
    
if __name__ == '__main__':
    init()
    text_input()
