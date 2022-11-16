import sys
from picamera import PiCamera
from time import sleep
from pynput.keyboard import Key, Listener

def salir():
    print("adiós")
    camera.stop_preview()
    camera.close()
    listener.stop()
    sys.exit()

def grabar():
    print("grabando imagen")
    camera.capture('foto.png')

def tecla(key):
    print(key)
    if key==Key.esc:
        salir()
    elif key==Key.space:
        grabar()


camera = PiCamera()
listener = Listener(on_press=tecla)
listener.start()
camera.start_preview(fullscreen=False, window=(100,200,480,640))
while True:
    pass


 
