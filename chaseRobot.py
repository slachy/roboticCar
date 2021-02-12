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

chaseVoice = ["chase1.mp3", "chase2.mp3"]
policeSiren = "police.mp3"

class ChaseRobot:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        pygame.init()
        pygame.mixer.init()
        self.blinkLeds = -1;
        self.pill2kill = None
        self.voiceId = 0
        self.speed = MAX_SPEED 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.task = None


    def startup(self):
        self.right()
        sleep(0.2)
        self.left()
        sleep(0.4)
        self.right()
        sleep(0.2)
        self.stop()
        pygame.mixer.music.load(chaseVoice[0])
        pygame.mixer.music.play()


    def forward(self):
        motors.motor1.setSpeed(self.speed)
        motors.motor2.setSpeed(-self.speed)


    def reverse(self):
        motors.motor1.setSpeed(-self.speed)
        motors.motor2.setSpeed(self.speed)


    def left(self):
        motors.motor1.setSpeed(self.speed)
        motors.motor2.setSpeed(self.speed)


    def right(self):
        motors.motor1.setSpeed(-self.speed)
        motors.motor2.setSpeed(-self.speed)


    def stop(self):
        motors.motor1.setSpeed(0)
        motors.motor2.setSpeed(0)


    def ioio(self, stop_event, arg):
        blueLed = 20
        redLed = 21
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


    def stopTask(self):
        self.pill2kill.set()
        self.task.join()
        self.pill2kill = None
        pygame.mixer.music.stop()


    def action1(self):
        self.blinkLeds = ~self.blinkLeds
        if self.blinkLeds == -1:
            self.stopTask()


    def action2(self):
        if self.blinkLeds == 0:
            self.blinkLeds = ~self.blinkLeds
            self.stopTask()
        pygame.mixer.music.load(chaseVoice[self.voiceId])
        self.voiceId = (self.voiceId + 1) % NUMBER_OF_VOICES
        pygame.mixer.music.play()


    def run(self):
        try:
          while True:
              data, addr = self.sock.recvfrom(1024)
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

              if self.blinkLeds == 0 and self.pill2kill == None:
                  self.pill2kill = threading.Event()
                  self.task = threading.Thread(target=self.ioio, args=(self.pill2kill, "task"))
                  pygame.mixer.music.load(policeSiren)
                  pygame.mixer.music.play()
                  self.task.start()
              
        finally:
            motors.setSpeeds(0, 0)
            GPIO.cleanup()

def main():
    GPIO.cleanup()
    chase = ChaseRobot()
    chase.startup()
    chase.run()

main()
