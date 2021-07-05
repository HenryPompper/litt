#!/usr/bin/env python3
import rospy
from std_msgs.msg import Byte
import os.path
from os import path
import pygame
from datetime import datetime
import signal
import sys

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

size = (800,480)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
intLevels = 0
configColor = [ 155,255,40 ]
color = [ 0,0,0 ]
configBGColor = [ 20,20,0 ]
interfaceRate = 1 
frameCounter = 0
level = 0

def volume_cb(data):
    global level
    if data.data != '':
        level = int(data.data)

def load_config():
    global configColor
    global configBGColor
    if path.exists('/var/www/html/litt.config'):
        config = open('/var/www/html/litt.config')
        settings = config.readlines()
        for setting in settings:
            if 'r=' in setting:
                configColor[0] = int(setting[2:])
            if 'g=' in setting:
                configColor[1] = int(setting[2:])
            if 'b=' in setting:
                configColor[2] = int(setting[2:])
            if 'r1=' in setting:
                configBGColor[0] = int(setting[3:])
            if 'g1=' in setting:
                configBGColor[1] = int(setting[3:])
            if 'b1=' in setting:
                configBGColor[2] = int(setting[3:])

def litt_animation(_level):
    global intLevels
    global color
    global configColor
    intLevel = 0
    if _level != '':
        try:
            intLevels = int(_level) * 1
        except ValueError:
            print('intLevel is invalid.  Only integers are acceptable')
    num_blocks = 20
    block_height = size[1] / (num_blocks + 2)
    vertical_space = block_height / 6
    block_width = block_height * 2.5
    vertical_position = block_height
    horizontal_space = 20
    for i in range(num_blocks):
        intLevel = intLevels
        if i == 0:
            intLevel *= 1
        if i == 1:
            intLevel *= 2 
        if i == 2:
            intLevel *= 3
        if i == 3:
            intLevel *= 4
        if i == 4:
            intLevel *= 5
        if i == 5:
            intLevel *= 6
        if i == 6:
            intLevel *= 7
        if i == 7:
            intLevel *= 8
        if i == 8:
            intLevel *= 9
        if i == 9:
            intLevel *= 10
        if i == 10:
            intLevel *= 10
        if i == 11:
            intLevel *= 9
        if i == 12:
            intLevel *= 8 
        if i == 13:
            intLevel *= 7
        if i == 14:
            intLevel *= 6
        if i == 15:
            intLevel *= 5
        if i == 16:
            intLevel *= 4
        if i == 17:
            intLevel *= 3
        if i == 18:
            intLevel *= 2
        if i == 19:
            intLevel *= 1
        color[0] = configColor[0]
        color[1] = configColor[1]
        color[2] = configColor[2]
        color[0] = max(min(color[0] * (intLevel * 0.01), 255),0)
        color[1] = max(min(color[1] * (intLevel * 0.01), 255),0)
        color[2] = max(min(color[2] * (intLevel * 0.01), 255),0)
        pygame.draw.rect(screen, (color[0], color[1], color[2]), [(size[0] / 2)-block_width/2,vertical_position * (i+1),block_width,block_height - vertical_space],0)
    for i in range(num_blocks - 4):
        intLevel = intLevels
        if i == 0:
            intLevel *= 1
        if i == 1:
            intLevel *= 2 
        if i == 2:
            intLevel *= 3
        if i == 3:
            intLevel *= 4
        if i == 4:
            intLevel *= 5
        if i == 5:
            intLevel *= 6
        if i == 6:
            intLevel *= 7
        if i == 7:
            intLevel *= 8
        if i == 8:
            intLevel *= 8
        if i == 9:
            intLevel *= 7
        if i == 10:
            intLevel *= 6 
        if i == 11:
            intLevel *= 5
        if i == 12:
            intLevel *= 4 
        if i == 13:
            intLevel *= 3
        if i == 14:
            intLevel *= 2
        if i == 15:
            intLevel *= 1
        color[0] = configColor[0]
        color[1] = configColor[1]
        color[2] = configColor[2]
        color[0] = max(min(color[0] * (intLevel * 0.01), 255),0)
        color[1] = max(min(color[1] * (intLevel * 0.01), 255),0)
        color[2] = max(min(color[2] * (intLevel * 0.01), 255),0)
        pygame.draw.rect(screen, (color[0], color[1], color[2]), [(size[0] / 2)-block_width/2 - block_width - (block_width*0.25),vertical_position * (i+3),block_width,block_height - vertical_space],0)
        color[0] = configColor[0]
        color[1] = configColor[1]
        color[2] = configColor[2]
        color[0] = max(min(color[0] * (intLevel * 0.01), 255),0)
        color[1] = max(min(color[1] * (intLevel * 0.01), 255),0)
        color[2] = max(min(color[2] * (intLevel * 0.01), 255),0)
        pygame.draw.rect(screen, (color[0], color[1], color[2]), [(size[0] / 2)+block_width/2 + (block_width*0.25),vertical_position * (i+3),block_width,block_height - vertical_space],0)

def visualizer():
    global color
    global configColor
    global configBGColor
    global level
    play = True
    color[0] = configColor[0]
    color[1] = configColor[1]
    color[2] = configColor[2]
    levelDisplayStr = "0"
    global frameCounter
    rospy.init_node('visualizer', anonymous=True)
    rospy.Subscriber("audioLevel", Byte, volume_cb)
    while play:
        load_config()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        screen.fill(configBGColor)
        litt_animation(level)
        font = pygame.font.SysFont("sans-serif", 32)
        fontSmall = pygame.font.SysFont("sans-serif", 26)
        fontClock = pygame.font.SysFont("sans-serif", 56)
        frameCounter = frameCounter + 1
        if frameCounter > interfaceRate:
            frameCounter = 0
            levelDisplayStr = str(level)
            if levelDisplayStr == '':
                levelDisplayStr = "0"
        titleTxt = font.render("K.I.T.T. v0.1", 1, configColor)
        visTxt = fontSmall.render("Visualizer Input: " + str(levelDisplayStr), 1, configColor)
        clockTxt = fontClock.render(datetime.now().strftime("%H:%M:%S"), 1, configColor)
        screen.blit(titleTxt, (10,10))
        screen.blit(visTxt, (20,36))
        screen.blit(clockTxt, (570,223))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def init():
    pygame.init()
    pygame.display.set_caption("K.I.T.T. Visualizer")

if __name__ == "__main__":
    init()
    visualizer()
