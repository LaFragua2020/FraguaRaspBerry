from datetime import datetime, timedelta
#from func_timeout import func_timeout, FunctionTimedOut
from time import sleep
import smtplib, ssl
import mimetypes
from email.message import EmailMessage


class AutoGmail():
    def __init__(self):
        print("AutoGmail iniciado")
        self.cooldown=datetime.now()

    def enviaMail(self, destino, titulo, parrafo1, adjunto = None):
        try:
            if self.cooldown < datetime.now():
                print("Enviando mail..")
                message = EmailMessage()
                if adjunto:
                    body = parrafo1
                    body+="""
                    
                    .
                    """   
                else:
                    body = parrafo1
                    body+="""
                    .
                    .
                    """                    
                sender = "lafraguabot@gmail.com"
                recipient = destino
                message['From'] = sender
                message['To'] = recipient
                message['Subject'] = titulo
                message.set_content(body)
                if adjunto:
                    mime_type, _ = mimetypes.guess_type(adjunto)
                    mime_type, mime_subtype = mime_type.split('/')
                    with open(adjunto, 'rb') as file:
                        message.add_attachment(file.read(),
                        maintype=mime_type,
                        subtype=mime_subtype,
                        filename=adjunto)
                    #print(message)
                port = 465
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login("lafraguabot@gmail.com", "biujlqcynnpagclm")
                    server.send_message(message)
                    server.quit()
                self.cooldown=datetime.now()+timedelta(seconds=15)
                print("mail enviado.")
            else:
                print("No se pueden mandar correos tan seguido!")     
        except Exception as e:
            print(e)
            print("error, posiblemente no se pudo conectar a GMail.")
            sleep(2)



if __name__ == '__main__':
    AG=AutoGmail()
    sleep(10)
    mensaje="Hola, esta es una prueba de autoGmail."
    correoDestino="g.gutierrez.gagliardi@gmail.com"
    archivoAdjunto="icon.png"
    AG.enviaMail(destino=correoDestino,titulo="Hola",parrafo1=mensaje, adjunto=archivoAdjunto)
    
