from microbit import *
import random

while True:                                #Run everything inside this block on repeat
    if accelerometer.was_gesture('shake'): #If microbit detects it was shook
        display.show(random.randint(1,6))  #Display a random number from a dice