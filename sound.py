#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pygame
import os

pause = 1
letterPause = 3
A=[0,1]
B=[1,0,0,0]
C=[1,0,1,0]
D=[1,0,0,0]
E=[0]
F=[0,0,1,0]


def playLetter(L):
  for i in L:
    if i == 0:
      pygame.mixer.Channel(0).play(ding, maxtime=3000)
      while pygame.mixer.Channel(0).get_busy() == True:
        continue
    elif i == 1:
      pygame.mixer.Channel(1).play(ding, maxtime=10000)
      while pygame.mixer.Channel(1).get_busy() == True:
        continue
      time.sleep(pause)
  time.sleep(letterPause)
    



        
# initialize
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

# start playing the background music
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'ambiance_underwater.wav'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)  # loop forever

pygame.display.set_mode()

ding = pygame.mixer.Sound("sounds/radar_ping_lent.wav")
pygame.mixer.Channel(0).set_volume(0.9)
pygame.mixer.Channel(1).set_volume(0.5)
pygame.mixer.Channel(0).set_endevent()
pygame.mixer.Channel(1).set_endevent()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                playLetter(A)
            if event.key == pygame.K_g:
                playLetter(B)






# # play a sound on channel 0 with a max time of 600 milliseconds
# pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound\gun_fire.wav'), maxtime=600)

# # you can play a longer sound on another channel and they won't conflict
# pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound\death.wav"), maxtime=2000)