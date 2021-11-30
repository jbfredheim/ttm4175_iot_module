from microbit import *
import random
import music

song = [
    "C","C","D","C","F","E","R",
    "C","C","D","C","G","E","R",
    "C","C","C","A","E","D","R",
    "A#","A#","A","F","G","F"
    ]
songs = [song, music.NYAN, music.ENTERTAINER]
while True:
    if pin_logo.is_touched():
        display.show(Image.HEART)
        music.play(random.choice(songs))
    else:
        display.show(Image.SAD)