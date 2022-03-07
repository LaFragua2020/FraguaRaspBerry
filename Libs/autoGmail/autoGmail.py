from datetime import datetime, timedelta
#from func_timeout import func_timeout, FunctionTimedOut
from time import time, sleep
from datetime import datetime, timedelta


import gspread


class AutoGmail():
    def __init__(self):
       self.sa=None
       self.sh=None
       self.wks=None
       self.cooldown=datetime.now()

    def conecta(self):
        print("Conectando..")
        try:
            self.sa=gspread.service_account(filename="service_account_gmail.json")
            print("Conectado a GS!")
            self.sh = self.sa.open("AutoGmail")#sa.open("ProtoFormulario")
            print("Conectado a SpreadSheet!")
            self.wks= self.sh.worksheet("Correos")#("Respuestas de formulario 1")
            print("Conectado a WorkSheet! ")
            print("Rows: ", self.wks.row_count)
            print("Cols: ", self.wks.col_count)
        except Exception as e:
            print(e)
            print("error, posiblemente no se pudo conectar a GS.")
            sleep(10)

    def enviaMail(self, destino, titulo, parrafo1, parrafo2):
        
        try:
            if self.cooldown+timedelta(seconds=10) < datetime.now():
                print("Enviando mail..")
                filaDisp=int(self.fila_disponible())
                print("Fila disponible: ", filaDisp )
                row=[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), destino, "",titulo,parrafo1, "", parrafo2,"Salduos,","Enviar"]
                #self.wks.update_cell(filaDisp, 0, 'Bingo!')
                self.wks.insert_row(row, 2)
                #self.update_row(row, filaDisp )
                self.cooldown=datetime.now()
                
            else:
                print("No se pueden mandar correos tan seguido!")
                
        except Exception as e:
            print(e)
            print("error, posiblemente no se pudo conectar a GS.")
            sleep(2)

    def update_row(self, row, filaDisp):
        print("registrando correo..")
        try:
            for cell in range(1,len(row)+1):

                print(filaDisp)
                print(cell)
                print(row[cell-1])
                self.wks.update_cell(int(filaDisp), int(cell), str(row[cell-1]))
                #print("Cols: ", self.wks.col_count)
                #self.wks.update_cell(3, 3, "Hola" )
            print("Correo registrado..")

        except Exception as e:
            print(e)
            print("error, posiblemente no se pudo conectar a GS.")
            sleep(10)

    def fila_disponible(self):
        str_list = list(filter(None, self.wks.col_values(1)))
        return str(len(str_list)+1)


def main():
    AG=AutoGmail()
    AG.conecta()
    AG.enviaMail(destino="g.gutierrez.gagliardi@gmail.com",titulo="Hola",parrafo1="asdsad",parrafo2="dadasfa")


if __name__ == '__main__':
    AG=AutoGmail()
    AG.conecta()
    sleep(10)
    AG.enviaMail(destino="g.gutierrez.gagliardi@gmail.com",titulo="Hola",parrafo1="asdsad",parrafo2="dadasfa")
