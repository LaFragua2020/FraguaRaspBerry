import sys
from Libs.facialReq import facial_req



detect=facial_req.Detector(ancho=250, flip=0)


#pygame.init()
#pygame.display.set_mode([640,480])
def salir():
    print("adiós")  
    detect.stop()
    sys.exit(0)

while True:
    captura=detect.foto(mostrar=1)
    key=captura["key"]
    lista=captura["listacaras"]
    
    if len(lista)>0:
        print("Encotramos a :")
        for cara in lista:
            print(" "+ cara["nombre"])

    if key==ord('q'):
        salir()

    

