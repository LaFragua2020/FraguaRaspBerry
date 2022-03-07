import RPi.GPIO as GPIO
from time import sleep


def finTodo():
    GPIO.cleanup()  

class Servo():
    def __init__(self, pin):    
        self.servo_pin=pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm=GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(0)

    def setAngle(self, angle):
        if angle>180:
            angle=180
        elif angle<0:
            angle=0
        duty = angle / 18 + 3
        #print(angle)
        self.pwm.ChangeDutyCycle(duty)

    def fin(self):
        self.pwm.stop()



if __name__ == '__main__' :
    #Programa
    servo=Servo(11)
    for i in range(0,181,10):
        servo.setAngle(i)#ángulo entre 0 y 180, de 10 en 10
        print(i)
        sleep(1)
    for i in range(180,-1,-25):
        servo.setAngle(i)#ángulo entre 180 y 0 de 25 en 25
        print(i)
        sleep(1)
        
    servo.setAngle(90)
    print("90")
    sleep(1)
    
    print("fin")
    servo.fin()

