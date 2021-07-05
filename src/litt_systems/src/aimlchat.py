#!/usr/bin/env python3

# # # # # # # # # #
#  ┏━┓ ╻ ┏┳┓ ╻    #
#  ┣━┫ ┃ ┃┃┃ ┃    #
#  ╹ ╹╹╹╹╹ ╹╹┗━╸╹ #
# # # # # # # # # # 

import aiml
import os
import rospy
from std_msgs.msg import String
from os import path

bot = aiml.Kernel()
response_publisher = rospy.Publisher("chat_output",String,queue_size=1)

def cli_input(data):
    respond(data.data)

def respond(intext):
    global bot
    print('USER: ', intext)
    response = bot.respond(intext)
    print('L.I.T.T.: ', response)
    response_publisher.publish(response)

def init():
    global bot
    path = os.path.dirname(os.path.realpath(__file__))
    bot.learn(path + "/aiml/brain.aiml")
    bot.learn(path + "/aiml/charname.aiml")
    bot.learn(path + "/aiml/kirk.aiml")
    bot.learn(path + "/aiml/update.aiml")
    bot.learn(path + "/aiml/kirk-update1.aiml")
    rospy.init_node('chatbot', anonymous=True)
    rospy.Subscriber("chat_input",String,cli_input)

web_input = ''

def check_web_input():
    global web_input
    if path.exists('/var/www/html/litt.chat'):
        web_input_file = open('/var/www/html/litt.chat')
        data = web_input_file.readline()
        if web_input != data:
            web_input = data
            respond(web_input)

def chatbot():
    while True:
        check_web_input()

if __name__ == '__main__':
    init()
    chatbot()
