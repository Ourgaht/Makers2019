#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import pygame
import math

# MORSE caracter
A=[0,1]
B=[1,0,0,0]
C=[1,0,1,0]
D=[1,0,0,0]
E=[0]
F=[0,0,1,0]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PI = 3.141592653

# Initialize the game engine
pygame.init()
clock = pygame.time.Clock()
# Hide the mouse cursor
pygame.mouse.set_visible(0)
# Set the height and width of the screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
center = [int(screen.get_width()/2), int(screen.get_height()/2)-30]

# ---------------------------- SOUND init
pygame.mixer.pre_init()
pygame.mixer.init()
# start playing the background music
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'ambiance_underwater.wav'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)  # loop forever
court = pygame.mixer.Sound("sounds/Court.wav")
long = pygame.mixer.Sound("sounds/Long.wav")
EE = pygame.mixer.Sound("sounds/EE.wav")

pygame.mixer.Channel(0).set_volume(0.4)
pygame.mixer.Channel(1).set_volume(0.7)
pygame.mixer.Channel(0).set_endevent()
pygame.mixer.Channel(1).set_endevent()
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


# ---------------------------- RADAR init
radar_radius = int(center[1]-50)
radar_center = [radar_radius + 50, center[1]]
angle = 0
def draw_radar_point(screen, center, radius, angle, point_angle, color):
  x = int(center[0] + radius * math.sin(point_angle))
  y = int(center[1] + radius * math.cos(point_angle))
  if(angle > point_angle):
    new_angle = angle-point_angle
  else:
    new_angle = angle-point_angle+2*PI
  color_ratio = (2*PI-new_angle)/(2*PI)
  new_color = (int(color[0]*color_ratio), int(color[1]*color_ratio), int(color[2]*color_ratio))
  pygame.draw.circle(screen, new_color, (x,y), 4, 0)
    


# ---------------------------- MORSE init
# Speed in pixels per frame
x_speed = 0
y_speed = 0
color = GREEN
morse_window = (center[0]+20, 10)
# Current position
x_coord = morse_window[0]
y_coord = morse_window[1]
def draw_cursor(screen, x, y, color):
    pygame.draw.rect(screen, color, [x, y, 1, 5], 0)
    if x != 0:
        x -= 1
    pygame.draw.rect(screen, BLACK, [x, y+7, 5, 2], 0)
    pygame.draw.rect(screen, GREEN, [x+1, y+7, 5, 2], 0)


# Loop until the user clicks the close button.
done = False
# Set the screen background
screen.fill(BLACK)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            done = True
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
    # ------------- MORSE event ---------------
          if event.key == pygame.K_SPACE:
            x_speed = 1
            color = GREEN
        elif event.type == pygame.KEYUP:
          if event.key == pygame.K_SPACE:
            color = BLACK

    # ------------- MORSE code ---------------
    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if x_coord > center[0]*2-20:
        pygame.draw.rect(screen, BLACK, [x_coord-1, y_coord+7, 5, 2], 0)
        pygame.draw.rect(screen, BLACK, [morse_window[0], y_coord+20, center[0], 14], 0)
        y_coord += 20
        x_coord = morse_window[0]
    if y_coord > 50:    
    # if y_coord > center[1]*2-20:
        y_coord = morse_window[1]
        pygame.draw.rect(screen, BLACK, [morse_window[0], y_coord, center[0], 14], 0)
    draw_cursor(screen, x_coord, y_coord, color)


    #----------------- RADAR -----------------
    # Circles
    pygame.draw.circle(screen, BLACK, radar_center, radar_radius, 0)
    pygame.draw.circle(screen, GREEN, radar_center, radar_radius, 2)
    pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.7), 2)
    pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.4), 2)    
    # Sweep
    x = radar_center[0] + radar_radius * math.sin(angle)
    y = radar_center[1] + radar_radius * math.cos(angle)
    pygame.draw.line(screen, GREEN, radar_center, [x, y], 2)
    angle = angle + .03
    # If we have done a full sweep, reset the angle to 0
    if angle > 2 * PI:
        angle = angle - 2 * PI
    # Rdar Points
    draw_radar_point(screen, radar_center, radar_radius*0.8, angle, 1, GREEN)

    pygame.display.flip()
    clock.tick(2000)
pygame.quit()
