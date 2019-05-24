#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import pygame
import math
import random

# ---------- Physical button on the rasp ----------
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
state = 0
GPIO_event = 0
def button_callback(channel):
    global GPIO_event
    global state
    if GPIO.input(10) == 0:
      if state == 1:
        print("Button was released!")
        GPIO_event = 1
      state = 0
    else:
      if state == 0:
        print("Button was pushed!")
        GPIO_event = 1  
      state = 1
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.BOTH,callback=button_callback) # Setup event on pin 10 rising edge

# ---------- SOCKET connection with the central table ----------
unlocked = False
#import socket
#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#print("before socket")        
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.bind((HOST, PORT))
#    s.listen()
#    conn, addr = s.accept()
#    with conn:
#        print('Connected by', addr)
#        while True:
#           data = conn.recv(1024)
#            if not data:
#                break
#            conn.sendall('<3 from server')
#print("after socket")





# autre -------------------------------------
#unlocked = False
#import threading
#import socketserver
 
#from datetime import datetime
 
## Python vient avec ses serveurs socket tout prêts.
## Tout ce qu'il y a faire c'est créer une classe 
## de handler, c'est à dire l'objet qui va s'occuper
## des messages quand ils arrivent. On hérite du 
## handler de la lib standard, et on redéfinit juste
## handle() qui est la méthode qui va être appelée
## à chaque message.
#class RequestHandler(socketserver.BaseRequestHandler): 
    #def handle(self):
        #data = self.request.recv(1024)
        #if data == "CMD_DEBLOCK" or data == "CMD_DEBLOCK\n":
          #global unlocked
          #unlocked = True
        ## on récupère des requêtes, et on répond avec
        ## exactement le même message + un timestamp
 
        #self.request.sendall(data)
        
## Pour le serveur, pas grand chose à faire à part le définir
## Ici je fais un serveur threadé pour le Lulz car ça
## ne sert pas à grand chose pour un client avec 3 messages
## synchrones
#class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    #pass
  
## on instancie notre server et on lui passe le gestionnaire de
## requêtes
#server = ThreadedTCPServer(('127.0.0.1', 65432), RequestHandler)
#ip, port = server.server_address

## on start le thread pour le serveur et on le daemonise
#server_thread = threading.Thread(target=server.serve_forever)

#server_thread.daemon = True
#server_thread.start()

import threading
import time
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65441        # The port used by the server
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
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)  # loop forever

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
radar_radius = int(center[1]-50-tlcorner[1]/2)
radar_center = [int(radar_radius+50+tlcorner[0]), int(center[1]+tlcorner[1]/2)]
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
morse_window = (center[0]+20, 10+tlcorner[1]+border_width)
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
    # r = random.randint(0,255)
    # width = random.randint(5,10)
    # height = random.randint(5,10)
    x = int(random.gauss(screen.get_width()/2, screen.get_width()/3))
    y = int(random.gauss(screen.get_height()/2, screen.get_height()/3))
    if (x<0) or (x>screen.get_width()) or (y<0) or (y>screen.get_height()):
      pass
    else:
      pygame.draw.rect(screen, WHITE, [x, y, 4, 6], 0)
      drawed = drawed+1
    

# ------------ Bugged mode ---------------------
while not unlocked:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        unlocked = True
  # pygame.draw.rect(screen, GREEN, [0, 0, 50, 50], 0)
  draw_white_noise(screen)
  pygame.display.flip()
  

# ------------- Regular mode ---------------------
# start playing the background music
pygame.mixer.music.load(os.path.join(os.getcwd(), 'sounds', 'ambiance_underwater+code.wav'))
pygame.mixer.music.set_volume(0.3)
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
while not done:
  if GPIO_event == 1:
    GPIO_event = 0
    if state == 1:
      x_speed = 1
      color = GREEN
    else:
      color = BLACK      
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
# ------------- MORSE event --------------        
    #elif event.type == pygame.KEYUP:
      
        

  # ------------- MORSE code ---------------
  # Move the object according to the speed vector.
  x_coord = x_coord + x_speed
  y_coord = y_coord + y_speed
  if x_coord > screen.get_width()-(20+tlcorner[0]+border_width):
    pygame.draw.rect(screen, BLACK, [x_coord-1, y_coord+7, 5, 2], 0) 
    y_coord += 20
    if y_coord > screen.get_height()-(10+tlcorner[1]+border_width):
      y_coord = morse_window[1]
    pygame.draw.rect(screen, BLACK, [morse_window[0], y_coord, center[0]-(border_width+tlcorner[0]+20), 14], 0)
    x_coord = morse_window[0]
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
  angle = angle + .01
  # If we have done a full sweep, reset the angle to 0
  if angle > 2 * PI:
      angle = angle - 2 * PI
  # Radar Points
  dist_ratio = dist_ratio + 0.00001
  draw_radar_point(screen, radar_center, radar_radius*dist_ratio, angle, 1, GREEN)
  pygame.display.flip()

GPIO.cleanup() # Clean up
pygame.quit()
