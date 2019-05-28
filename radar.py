#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import pygame
import math
import random

boot_time = -1000000000

# ---------- Physical button on the rasp ----------
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
last_morse = 100000000000
state = 0
GPIO_event = 0
def button_callback(channel):
    global GPIO_event
    global state
    global boot_time
    if boot_time < 0 :
       boot_time = time.time()
    if GPIO.input(10) == 0:
      if state == 1:
        GPIO_event = 1
      state = 0
    else:
      if state == 0:
        GPIO_event = 1  
      state = 1
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.BOTH,callback=button_callback) # Setup event on pin 10 rising edge

# ---------- SOCKET connection with the central table ----------
import threading
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65441        # The port used by the server
unlocked = False
time.sleep(2)

def threaded_client():
  global unlocked  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while not unlocked:
      data = s.recv(1024).decode()
      data = data.rstrip()
      print("client received :")
      print(data)
      if data == "CMD_DEBLOCK":
        print("TEST SUCCEEDED")
        unlocked = True
      time.sleep(2)

threading.Thread(target=threaded_client).start()

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

# Initialize Sounds
pygame.mixer.pre_init()
pygame.mixer.init()
court = pygame.mixer.Sound("sounds/Court.wav")
long = pygame.mixer.Sound("sounds/Long.wav")
EE = pygame.mixer.Sound("sounds/EE.wav")
pygame.mixer.Channel(0).set_volume(0.4)
pygame.mixer.Channel(1).set_volume(0.7)
pygame.mixer.Channel(0).set_endevent()
pygame.mixer.Channel(1).set_endevent()
# start playing the background music (white noise at first)
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'whitenoise.wav'))
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(loops=-1)  # loop forever

# the two next functions served to play any letter in the format [0,1,1,0] representing their morse code
# In this project the code is always the same and was simply added over the background sound
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

#-------------- GENERAL GUI --------------
border_width = 30
to_tuch_the_circle = border_width * 0.5*math.sqrt(2)
tlcorner = (60,60)
trcorner = (screen.get_width()-tlcorner[0], tlcorner[1])
blcorner = (tlcorner[0], screen.get_height()-tlcorner[1])
brcorner = (screen.get_width()-tlcorner[0], screen.get_height()-tlcorner[1])

# Initialize radar GUI
radar_radius = int(center[1]-80-tlcorner[1]/2)
radar_center = [int(radar_radius+80+tlcorner[0]), int(center[1]+tlcorner[1]/2)]
angle = 0
# dist of the mooving object on the radar
dist_ratio = 0.6


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

# Initialize Morse GUI
x_speed = 0
y_speed = 0
color = GREEN
xborder_offset = 70
yborder_offset = 100
morse_window = (center[0]+xborder_offset, tlcorner[1]+border_width+yborder_offset, brcorner[0]-border_width-xborder_offset, brcorner[1]-border_width-yborder_offset)
# Current position
x_coord = morse_window[0]
y_coord = morse_window[1]

def draw_cursor(screen, x, y, color):
    pygame.draw.rect(screen, color, [x, y, 1, 5], 0)
    if x != 0:
        x -= 1
    pygame.draw.rect(screen, BLACK, [x, y+7, 5, 2], 0)
    pygame.draw.rect(screen, GREEN, [x+1, y+7, 5, 2], 0)

def draw_white_noise(screen):
  screen.fill(BLACK)
  drawed = 0
  while drawed<10000:
    x = int(random.gauss(screen.get_width()/2, screen.get_width()/3))
    y = int(random.gauss(screen.get_height()/2, screen.get_height()/3))
    if (x<0) or (x>screen.get_width()) or (y<0) or (y>screen.get_height()):
      pass
    else:
      pygame.draw.rect(screen, WHITE, [x, y, 4, 6], 0)
      drawed = drawed+1
    
installation = True
# game set mode
automatic_start = 5
while installation:
    screen.fill(BLACK)
    
    title_font = pygame.font.SysFont("freeserif", 60)
    regular_font = pygame.font.SysFont("freeserif", 30)
    
    title = title_font.render("Mise en place de l'énigme", True,WHITE)
    text1 = regular_font.render("Démarrer l'énigme : rester appuyé 3 secondes sur le bouton --> !!! Attention: son horrible dans le casque !!!", True, WHITE)
    text2 = regular_font.render("L'énigme démarre brouillée et se déverrouille X min après le lancement de celle-ci", True, WHITE)
    textconseil2 = regular_font.render("Idéalement, le jeu doit se déverrouiller entre 5 et 10 min après l'entrée des participants.", True, WHITE)
    textconseil1 = regular_font.render("Nous laissons au soins du préparateur de définir ce temps :", True, WHITE)
    textpreX = regular_font.render("Appui court pour changer (de 5 à 30 min) -> ", True, WHITE)
    textX = regular_font.render("X = " + str(automatic_start+5) + " min", True, WHITE)
    text3 = regular_font.render("Débrancher et rebrancher la carte relancera automatiquement le programme du début", True, WHITE)
    text4 = regular_font.render("Pendant la phase brouillée, si un clavier est branché sur la raspberry pi, un appui sur la touche \"s\" (pour start) déverrouille aussi l'énigme", True, WHITE)

    screen.blit(title, (80, 50))
    screen.blit(text1, (80, 150))
    screen.blit(text2, (80, 250))
    screen.blit(textconseil1, (80, 300))
    screen.blit(textpreX, (80, 350))    
    screen.blit(textX, (650, 350))
    screen.blit(textconseil2, (80, 400))
    screen.blit(text3, (80, 500))
    screen.blit(text4, (80, 550))

    pygame.display.flip()
    if GPIO_event == 1:
      GPIO_event = 0
      if state == 1:
        pressed = True
        last_morse = time.time()
      elif time.time()-last_morse > 3:
        installation = False
      else:
        last_morse = 1000000000000000
        automatic_start = (automatic_start+1)%26
    if time.time()-last_morse > 3.1:
        installation = False
automatic_start = automatic_start+5

# ------------ Bugged mode ---------------------
pygame.mixer.music.set_volume(0.2)
boot_time = time.time()
while not unlocked:
  if time.time()-boot_time > 60 * automatic_start:
    unlocked = True
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        unlocked = True
  # pygame.draw.rect(screen, GREEN, [0, 0, 50, 50], 0)
  draw_white_noise(screen)
  pygame.display.flip()

# ------------- Rebooting ------------------------
pygame.mixer.music.set_volume(0)
screen.fill(BLACK)
font = pygame.font.SysFont("freeserif", 30)
for i in range(0,5):
  screen.fill(BLACK)
  text = font.render("Rebooting .", True, GREEN)
  screen.blit(text, (20, 20))
  pygame.display.flip()
  time.sleep(1)
  
  screen.fill(BLACK)
  text = font.render("Rebooting ..", True, GREEN)
  screen.blit(text, (20, 20))
  pygame.display.flip()
  time.sleep(1)
  
  screen.fill(BLACK)
  text = font.render("Rebooting ...", True, GREEN)
  screen.blit(text, (20, 20))
  pygame.display.flip()
  time.sleep(1)
  
  screen.fill(BLACK)
  text = font.render("Rebooting ....", True, GREEN)
  screen.blit(text, (20, 20))
  pygame.display.flip()
  time.sleep(1)
  
  screen.fill(BLACK)
  text = font.render("Rebooting .....", True, GREEN)
  screen.blit(text, (20, 20))
  pygame.display.flip()
  time.sleep(1)
  
# ------------- Starting animation ------------------
rect_offset = 10

screen.fill(BLACK)
pygame.display.flip()

pygame.draw.rect(screen, GREEN, [tlcorner[0]-border_width, tlcorner[1]-border_width, brcorner[0]-(tlcorner[0]-2*border_width), brcorner[1]-(tlcorner[1]-2*border_width)], 2)
pygame.display.flip()
time.sleep(0.5)

pygame.draw.rect(screen, GREEN, [tlcorner[0]+to_tuch_the_circle, tlcorner[1]+to_tuch_the_circle, brcorner[0]-(tlcorner[0]+2*to_tuch_the_circle), brcorner[1]-(tlcorner[1]+2*to_tuch_the_circle)], 2)
pygame.display.flip()
time.sleep(0.1)

pygame.draw.circle(screen, GREEN, tlcorner, border_width, 2)
pygame.display.flip()
time.sleep(0.5)

pygame.draw.circle(screen, GREEN, trcorner, border_width, 2)
pygame.display.flip()
time.sleep(1)

pygame.draw.circle(screen, GREEN, blcorner, border_width, 2)
pygame.display.flip()
time.sleep(0.2)

pygame.draw.circle(screen, GREEN, brcorner, border_width, 2)
pygame.display.flip()
time.sleep(1)

pygame.draw.rect(screen, GREEN, [morse_window[0]-rect_offset, morse_window[1]-rect_offset, morse_window[2] - morse_window[0] + 2*rect_offset, morse_window[3] - morse_window[1] + 2*rect_offset], 2)
pygame.display.flip()
time.sleep(0.1)

pygame.draw.circle(screen, GREEN, radar_center, radar_radius, 2)
pygame.display.flip()
time.sleep(0.1)

pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.7), 2)
pygame.display.flip()
time.sleep(0.1)

pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.4), 2)
pygame.display.flip()
time.sleep(3)
  

# ------------- Regular mode ---------------------
# start playing the background music
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'ambiance_underwater+code.wav'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)  # loop forever
# --- GUI init ---
screen.fill(BLACK)
pygame.draw.rect(screen, GREEN, [tlcorner[0]-border_width, tlcorner[1]-border_width, brcorner[0]-(tlcorner[0]-2*border_width), brcorner[1]-(tlcorner[1]-2*border_width)], 2)
pygame.draw.rect(screen, GREEN, [tlcorner[0]+to_tuch_the_circle, tlcorner[1]+to_tuch_the_circle, brcorner[0]-(tlcorner[0]+2*to_tuch_the_circle), brcorner[1]-(tlcorner[1]+2*to_tuch_the_circle)], 2)
pygame.draw.circle(screen, GREEN, tlcorner, border_width, 2)
pygame.draw.circle(screen, GREEN, trcorner, border_width, 2)
pygame.draw.circle(screen, GREEN, blcorner, border_width, 2)
pygame.draw.circle(screen, GREEN, brcorner, border_width, 2)


done = False
jump = 2
count = 0
while not done:
  if GPIO_event == 1:
    GPIO_event = 0
    if state == 1:
      last_morse = 100000000000
      jump = 0
      x_speed = 1
      color = GREEN
    else:
      last_morse = time.time()
      x_speed = 0
      color = BLACK
      pygame.draw.rect(screen, BLACK, [x_coord, y_coord+7, 5, 2], 0)
      x_coord = x_coord + 10
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        print("ESC key pressed --> game stopped")
        done = True
      if event.key == pygame.K_a:
          last_morse = time.time()
          jump = 0
          x_speed = 1
          color = GREEN    
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
          x_speed = 0
          color = BLACK
          pygame.draw.rect(screen, BLACK, [x_coord, y_coord+7, 5, 2], 0)
          x_coord = x_coord + 10
        

  # ------------- MORSE code ---------------
  pygame.draw.rect(screen, GREEN, [morse_window[0]-rect_offset, morse_window[1]-rect_offset, morse_window[2] - morse_window[0] + 2*rect_offset, morse_window[3] - morse_window[1] + 2*rect_offset], 2)
  # Move the object according to the speed vector.
  x_coord = x_coord + x_speed
  y_coord = y_coord + y_speed
  
  if jump == 0 and (time.time()-last_morse) > 1.8:
    jump = jump + 1
    last_morse = time.time()
    pygame.draw.rect(screen, BLACK, [x_coord-1, y_coord+7, 6, 2], 0) 
    x_coord = morse_window[0] 
    y_coord += 20
  elif jump == 1 and (time.time()-last_morse) > 4:
    jump = jump + 1
    last_morse = time.time()
    pygame.draw.rect(screen, BLACK, [x_coord-1, y_coord+7, 6, 2], 0) 
    x_coord = morse_window[0] 
    y_coord += 20
  elif x_coord > morse_window[2]:
    pygame.draw.rect(screen, BLACK, [x_coord-1, y_coord+7, 6, 2], 0) 
    y_coord += 20
    if y_coord > morse_window[3]:
      y_coord = morse_window[1]
    pygame.draw.rect(screen, BLACK, [morse_window[0], y_coord, morse_window[2] - morse_window[0], 14], 0)
    x_coord = morse_window[0]
  draw_cursor(screen, x_coord, y_coord, color)

  #----------------- RADAR -----------------
  pygame.draw.circle(screen, BLACK, radar_center, radar_radius, 0)
  # Sweep
  x = radar_center[0] + radar_radius * math.sin(angle)
  y = radar_center[1] + radar_radius * math.cos(angle)
  pygame.draw.line(screen, GREEN, radar_center, [x, y], 2)
  shadow_angle = angle
  amount = 100
  for i in range(0,amount):
    shadow_angle = shadow_angle - 0.0025
    shadow_GREEN = (0, 255-i*(255/amount), 0)
    xx = radar_center[0] + radar_radius * math.sin(shadow_angle)
    yy = radar_center[1] + radar_radius * math.cos(shadow_angle)
    pygame.draw.line(screen, shadow_GREEN, radar_center, [xx, yy], 2)
  angle = angle + .01

  # If we have done a full sweep, reset the angle to 0
  if angle > 2 * PI:
      angle = angle - 2 * PI
  # Circles
  pygame.draw.circle(screen, GREEN, radar_center, radar_radius, 2)
  pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.7), 2)
  pygame.draw.circle(screen, GREEN, radar_center, int(radar_radius*0.4), 2)
  
  # Radar Points
  count = count + 1
  if count % 40 == 0:
    dist_ratio = dist_ratio + 0.00001
    if dist_ratio > 0.99:
      dist_ratio = 0.99
  draw_radar_point(screen, radar_center, radar_radius*dist_ratio, angle, 1, GREEN)
  pygame.display.flip()

GPIO.cleanup() # Clean up
pygame.quit()
