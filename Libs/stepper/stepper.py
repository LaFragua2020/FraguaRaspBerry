#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# libraries
import time
import RPi.GPIO as GPIO



class Stepper():
    def __init__(self, pin1,pin2,pin3,pin4):   
        #ini
        # Use BCM GPIO references
        # Instead of physical pin numbers
        GPIO.setmode(GPIO.BOARD)#(GPIO.BCM)
        self.pin1=pin1
        self.pin2=pin2
        self.pin3=pin3
        self.pin4=pin4

        # Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
        self.StepPins = [self.pin1,self.pin2,self.pin3,self.pin4]#[18,22,24,26]
        # Set all pins as output
        for pin in self.StepPins:
            #print("Setup pins")
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        # Define some settings
        self.WaitTime = 0.005

        # Define simple sequence
        self.StepCount1 = 4
        self.Seq1 = []
        self.Seq1 = [i for i in range(0, self.StepCount1)]
        self.Seq1[0] = [1,0,0,0]
        self.Seq1[1] = [0,1,0,0]
        self.Seq1[2] = [0,0,1,0]
        self.Seq1[3] = [0,0,0,1]
        # Define advanced half-step sequence
        self.StepCount2 = 8
        self.Seq2 = []
        self.Seq2 = [i for i in range(0, self.StepCount2)]
        self.Seq2[0] = [1,0,0,0]
        self.Seq2[1] = [1,1,0,0]
        self.Seq2[2] = [0,1,0,0]
        self.Seq2[3] = [0,1,1,0]
        self.Seq2[4] = [0,0,1,0]
        self.Seq2[5] = [0,0,1,1]
        self.Seq2[6] = [0,0,0,1]
        self.Seq2[7] = [1,0,0,1]
        # Choose a sequence to use
        self.Seq = self.Seq2
        self.StepCount = self.StepCount2

    def steps(self,nb):
            StepCounter = 0
            if nb<0: sign=-1
            else: sign=1
            nb=int(sign*nb*2) #times 2 because half-step
            #print("nbsteps {} and sign {}".format(nb,sign))
            for i in range(nb):
                    for pin in range(4):
                            xpin = self.StepPins[pin]
                            if self.Seq[StepCounter][pin]!=0:
                                    GPIO.output(xpin, True)
                            else:
                                    GPIO.output(xpin, False)
                    StepCounter += sign
                    # If we reach the end of the sequence
                    # start again
                    if (StepCounter==self.StepCount):
                            StepCounter = 0
                    if (StepCounter<0):
                            StepCounter = self.StepCount-1
                    # Wait before moving on
                    time.sleep(self.WaitTime)
    def izq(self,pasos):
        self.steps(2*pasos)
        self.stop()
    def der(self,pasos):
        self.steps(-2*pasos)
        self.stop()
    
    def stop(self):
        #print("Stop motor")
        for pin in self.StepPins:
                GPIO.output(pin, False)
# Start main loop
nbStepsPerRev= 8#32#128#2048
if __name__ == '__main__' :
    hasRun=False
    stepper=Stepper(18,22,24,26)
    while not hasRun:
            stepper.izq(200)# parcourt un tour dans le sens horaire
            #time.sleep(1)
            stepper.der(200)# parcourt un tour dans le sens anti-horaire
            #time.sleep(1)
            hasRun=True

    print("Stop motor")
    stepper.stop()
