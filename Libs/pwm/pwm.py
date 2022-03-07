import RPi.GPIO as GPIO   # Import the GPIO library.
from time import sleep             # Import time library


def finTodo():
    GPIO.cleanup()            # resets GPIO ports used back to input mode
     

class PWM():
    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
                                  # Can use GPIO.setmode(GPIO.BCM) instead to use 
                                  # Broadcom SOC channel names.
        
        self.pwm_pin=pin
        GPIO.setup(self.pwm_pin, GPIO.OUT)  # Set GPIO pin to output mode.
        self.pwm = GPIO.PWM(self.pwm_pin, 60)    # Initialize PWM on pwmPin 100Hz frequency
        self.dc=0
        self.pwm.start(self.dc)             # Start PWM with 0% duty cycle
    def frec(self,val):
        if val==0:
            val=1
        self.pwm.ChangeFrequency(abs(val))
    def duty(self,val):
        self.pwm.ChangeDutyCycle(min(100, abs(val) ))
    def fin(self):
        self.pwm.stop()                         # stop PWM
   

if __name__ == '__main__' :
    # main loop of program
    print("\nPresiona ctr+c para salir \n")  # Print blank line before and after message.
    dc=0                           
    led=PWM(29)
    buzzer=PWM(21)
    try:
        while True:# Loop until Ctl C is pressed to stop.
            for dc in range(0, 101, 5):    # Loop 0 to 100 stepping dc by 5 each loop
                led.duty(dc)
                led.frec(100+dc*10)
                sleep(0.05)             # wait .05 seconds at current LED brightness
                print(dc)
            for dc in range(95, 0, -5):    # Loop 95 to 5 stepping dc down by 5 each loop
                led.duty(dc)
                led.frec(100+dc*10)
                buzzer.duty(dc)
                buzzer.frec(100+dc*10)
                sleep(0.05)             # wait .05 seconds at current LED brightness
                print(dc)
            buzzer.duty(0)
            led.duty(0)
    except KeyboardInterrupt:
        print("Salida")
        buzzer.fin()
        led.fin()
        finTodo()