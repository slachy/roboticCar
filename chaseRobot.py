import socket
import threading
import pygame
from pololu_drv8835_rpi import motors, MAX_SPEED
from time import sleep
from random import randrange
import RPi.GPIO as GPIO

UDP_IP = "0.0.0.0"
UDP_PORT= 5050

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

chaseVoice = ["chase1.mp3", "chase2.mp3"]

s = 70#MAX_SPEED / 2

def forward():
    motors.motor1.setSpeed(s)
    motors.motor2.setSpeed(-s)

def reverse():
    motors.motor1.setSpeed(-s)
    motors.motor2.setSpeed(s)

def left():
    motors.motor1.setSpeed(s)
    motors.motor2.setSpeed(s)

def right():
    motors.motor1.setSpeed(-s)
    motors.motor2.setSpeed(-s)

def stop():
    motors.motor1.setSpeed(0)
    motors.motor2.setSpeed(0)

def ioio(stop_event, arg):
    blueLed = 20
    redLed = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(redLed, GPIO.OUT)
    GPIO.setup(blueLed, GPIO.OUT)
    while not stop_event.wait(1):
        GPIO.output(blueLed, GPIO.HIGH)
        GPIO.output(redLed, GPIO.LOW)
        sleep(0.5)
        GPIO.output(blueLed, GPIO.LOW)
        GPIO.output(redLed, GPIO.HIGH)
        sleep(0.5)
    GPIO.output(blueLed, GPIO.LOW)
    GPIO.output(redLed, GPIO.LOW)

def startup():
    right()
    sleep(0.2)
    left()
    sleep(0.4)
    right()
    sleep(0.2)
    stop()
    pygame.mixer.music.load(chaseVoice[0])
    pygame.mixer.music.play()


def main():
  pygame.init()
  pygame.mixer.init()
  blinkLeds = -1;
  pill2kill = None
  voiceId = 0
  try:
      startup()
      while True:
          data, addr = sock.recvfrom(1024)
          raw = data
      
          if raw == "forward":
              forward()
      
          elif raw == "backward":
              reverse()
      
          elif raw == "left":
              left()
      
          elif raw == "right":
              right()
      
          elif raw == "stop":
              stop()
          
          elif raw == "action 1":
              blinkLeds = ~blinkLeds
              if blinkLeds == -1:
                  pill2kill.set()
                  t.join()
                  pill2kill = None
                  pygame.mixer.music.stop()

          elif raw == "action2":
              pygame.mixer.music.load(chaseVoice[voiceId])
              voiceId = (voiceId + 1) % 2
              pygame.mixer.music.play()

          else:
              stop()

          if blinkLeds == 0 and pill2kill == None:
              pill2kill = threading.Event()
              t = threading.Thread(target=ioio, args=(pill2kill, "task"))
              pygame.mixer.music.load("../police.mp3")
              pygame.mixer.music.play()
              t.start()
          
  finally:
      motors.setSpeeds(0, 0)
      GPIO.cleanup()

main()
