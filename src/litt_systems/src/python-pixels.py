#!/usr/bin/env python3
import rospy
from std_msgs.msg import Byte
import os.path
from os import path
import time
import board
import neopixel
import signal
import sys

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
pixels = neopixel.NeoPixel(board.D10, 8)
frames = [
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,1 ],
        [ 0,0,0,0,0,0,1,0 ],
        [ 0,0,0,0,0,1,0,0 ],
        [ 0,0,0,0,1,0,0,0 ],
        [ 0,0,0,1,0,0,0,0 ],
        [ 0,0,1,0,0,0,0,0 ],
        [ 0,1,0,0,0,0,0,0 ],
        [ 1,0,0,0,0,0,0,0 ],
        [ 1,0,0,0,0,0,0,0 ],
        [ 0,1,0,0,0,0,0,0 ],
        [ 0,0,1,0,0,0,0,0 ],
        [ 0,0,0,1,0,0,0,0 ],
        [ 0,0,0,0,1,0,0,0 ],
        [ 0,0,0,0,0,1,0,0 ],
        [ 0,0,0,0,0,0,1,0 ],
        [ 0,0,0,0,0,0,0,1 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0 ]
        ]
animation = [ 0,0,0,0,0,0,0,0 ]
color = [ 155,255,155 ]
off = [ 0,20,0 ]
counter = 0
pixelStates = [
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ],
            [ 0,0,0 ]
        ]
dimRate = 64
delay = 0.1
iAnimate = True
animationTimer = 0
animationRate = 10
brightness = 0.05
level=0 
def volume_cb(data):
    global level
    if data.data != '':
        level = int(data.data)

def litt():
    global animation
    global color
    global counter
    global animationTimer
    global off
    global brightness
    global delay
    rospy.init_node('scanLED', anonymous=True)
    rospy.Subscriber('audioLevel', Byte, volume_cb)
    while True:
        if path.exists("/var/www/html/litt.config"):
            config = open('/var/www/html/litt.config')
            settings = config.readlines()
            for setting in settings:
                if 'r=' in setting:
                    color[0] = int(setting[2:])
                if 'g=' in setting:
                    color[1] = int(setting[2:])
                if 'b=' in setting:
                    color[2] = int(setting[2:])
                if 'r1=' in setting:
                    off[0] = int(setting[3:])
                if 'g1=' in setting:
                    off[1] = int(setting[3:])
                if 'b1=' in setting:
                    off[2] = int(setting[3:])
                if 'animate' in setting:
                    if 'true' in setting:
                        iAnimate = True
                    else:
                        iAnimate = False
                if 'brightness' in setting:
                    brightness = float(setting[11:])
                if 'delay' in setting:
                    delay = float(setting[6:])
        if (iAnimate):
            animationTimer += 1
            if animationTimer > animationRate:
                counter += 1
                if counter >= 24:
                    counter = 0
                    animationTimer = 0
                animation = frames[counter]
                for i in range(8):
                    if animation[i] == 1:
                        pixelStates[i] = color
                    else:
                        pixelStates[i] = off
                for n in range(8):
                    if pixelStates[n] > pixels[n]:
                        pixels[n] = pixelStates[n]
                    else:
                        pixels[n] = [ 
                            max(pixels[n][0] - dimRate, off[0]),
                            max(pixels[n][1] - dimRate, off[1]),
                            max(pixels[n][2] - dimRate, off[2])
                        ]
            pixels.brightness = brightness
        else:
            for i in range(8):
                pixelStates[i] = color
        time.sleep(delay)

if __name__ == "__main__":
    litt()
