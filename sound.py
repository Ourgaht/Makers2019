#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pygame
import os

A=[0,1]
B=[1,0,0,0]
C=[1,0,1,0]
D=[1,0,0,0]
E=[0]
F=[0,0,1,0]

def playLetter(L):
  for i in L:
    if i == 0:
      pygame.mixer.Channel(0).play(court)
      while pygame.mixer.Channel(0).get_busy() == True:
        continue
    elif i == 1:
      pygame.mixer.Channel(1).play(long)
      while pygame.mixer.Channel(1).get_busy() == True:
        continue
        
    
def playEE():
    pygame.mixer.Channel(1).play(EE)
    vol = 0.6
    i = 0
    while pygame.mixer.Channel(1).get_busy() == True:
        i = i + 1
        if (i%1000000 == 0) and vol != 0:
            vol = vol - 0.05
            pygame.mixer.music.set_volume(vol)
    i = 0
    while vol != 0.6:
        i = i + 1
        if i%100000 == 0:
            vol = vol + 0.05
            pygame.mixer.music.set_volume(vol)
    
            
# initialize
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

# start playing the background music
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'ambiance_underwater.wav'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)  # loop forever

pygame.display.set_mode()

court = pygame.mixer.Sound("sounds/Court.wav")
long = pygame.mixer.Sound("sounds/Long.wav")
EE = pygame.mixer.Sound("sounds/EE.wav")

pygame.mixer.Channel(0).set_volume(1.0)
pygame.mixer.Channel(1).set_volume(1.0)
pygame.mixer.Channel(0).set_endevent()
pygame.mixer.Channel(1).set_endevent()

ee = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ee = 0
                playLetter(A)
            if event.key == pygame.K_b:
                ee = 0
                playLetter(B)
            if event.key == pygame.K_e:
                ee = ee + 1
                if ee == 2:
                    ee = 0
                    playEE()
                    
                






# # play a sound on channel 0 with a max time of 600 milliseconds
# pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound\gun_fire.wav'), maxtime=600)

# # you can play a longer sound on another channel and they won't conflict
# pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound\death.wav"), maxtime=2000)