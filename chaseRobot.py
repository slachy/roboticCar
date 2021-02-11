import socket
import threading
import pygame
from pololu_drv8835_rpi import motors
from time import sleep
from random import randrange
import RPi.GPIO as GPIO

UDP_IP = "0.0.0.0"
UDP_PORT = 5050
NUMBER_OF_VOICES = 2
MAX_SPEED = 70

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

chaseVoice = ["chase1.mp3", "chase2.mp3"]
policeSiren = "police.mp3"

class ChaseRobot:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.blinkLeds = -1;
        self.pill2kill = None
        self.voiceId = 0
        self.speed = MAX_SPEED 


    def startup():
        self.right()
        sleep(0.2)
        slef.left()
        sleep(0.4)
        self.right()
        sleep(0.2)
        self.stop()
        pygame.mixer.music.load(chaseVoice[0])
        pygame.mixer.music.play()


    def forward():
        motors.motor1.setSpeed(self.speed)
        motors.motor2.setSpeed(-self.speed)


    def reverse():
        motors.motor1.setSpeed(-self.speed)
        motors.motor2.setSpeed(self.speed)


    def left():
        motors.motor1.setSpeed(self.speed)
        motors.motor2.setSpeed(self.speed)


    def right():
        motors.motor1.setSpeed(-self.speed)
        motors.motor2.setSpeed(-self.speed)


    def stop():
        motors.motor1.setSpeed(0)


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


    def action1():
        self.blinkLeds = ~self.blinkLeds
        if self.blinkLeds == -1:
           self.pill2kill.set()
           t.join()
           pill2kill = None
           pygame.mixer.music.stop()


    def action2():
        if self.blinkLeds == 0:
            self.blinkLeds = ~self.blinkLeds
            self.pill2kill.set()
            t.join()
            self.pill2kill = None
            pygame.mixer.music.stop()
            pygame.mixer.music.load(chaseVoice[voiceId])
            self.voiceId = (self.voiceId + 1) % NUMBER_OF_VOICES
            pygame.mixer.music.play()


    def run():
        try:
          while True:
              data, addr = sock.recvfrom(1024)
              raw = data
          
              if raw == "forward":
                  self.forward()
              elif raw == "backward":
                  self.reverse()
              elif raw == "left":
                  self.left()
              elif raw == "right":
                  self.right()
              elif raw == "stop":
                  self.stop()
              elif raw == "action 1":
                  self.action1()
              elif raw == "action2":
                  self.action2()
              else:
                  self.stop()

              if self.blinkLeds == 0 and slef.pill2kill == None:
                  self.pill2kill = threading.Event()
                  t = threading.Thread(target=ioio, args=(pill2kill, "task"))
                  pygame.mixer.music.load(policeSiren)
                  pygame.mixer.music.play()
                  t.start()
              
          finally:
              motors.setSpeeds(0, 0)
              GPIO.cleanup()

def main():
    chase = ChaseRobot()
    chase.startup()
    chase.run()

main()
