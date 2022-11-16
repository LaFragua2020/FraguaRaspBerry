#! /usr/bin/python

# import the necessary packages

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2


class Detector():
    def __init__(self,ancho,flip):
        #Initialize 'currentname' to trigger only when a new person is identified.
        self.currentname = "unknown"
        #Determine faces from encodings.pickle file model created from train_model.py
        self.encodingsP = "encodings.pickle"

        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        print("[INFO] loading encodings + face detector...")
        self.data = pickle.loads(open(self.encodingsP, "rb").read())

        # initialize the video stream and allow the camera sensor to warm up
        # Set the ser to the followng
        # src = 0 : for the build in single web cam, could be your laptop webcam
        # src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
        #vs = VideoStream(src=2,framerate=10).start()
        self.vs = VideoStream(usePiCamera=True, vflip = flip).start()
        time.sleep(2.0)

        # start the FPS counter
        self.fps = FPS().start()

        self.ANCHO=ancho#250#125
        
    def key_pressed(self):
        key = cv2.waitKey(1) #& 0xFF
        return(key)

    def guardafoto(self,nombre):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=self.ANCHO)
        cv2.imwrite(nombre+".png", frame)
        
    # loop over frames from the video file stream
    def foto(self,mostrar):
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = self.vs.read()
        frame = imutils.resize(frame, width=self.ANCHO)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        
        listacaras=[]
        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"],encoding)
            name = "Unknown" #if face is not recognized, then print Unknown
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
                #If someone in your dataset is identified, print their name on the screen
                if self.currentname != name:
                    self.currentname = name
                    #print(self.currentname)
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        if boxes:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image - color is in BGR
                centro=( left+(right-left)/2 , top+(bottom-top)/2 )
                cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, str(centro), (left, y), cv2.FONT_HERSHEY_SIMPLEX,.4, (0, 255, 255), 1)
                cv2.putText(frame, name, (left, y-15), cv2.FONT_HERSHEY_SIMPLEX,.4, (0, 255, 255), 1)
                diff=centro[0]-self.ANCHO/2
                
                area=(top-bottom)*(left-right)
                
                '''
                if abs(diff)>1:
                    stepper.izq(-diff)
                    led.dim((100-diff)*5)
                print("diff: {}".format(centro[0]-ANCHO/2))
                '''
                
                listacaras.append({"nombre":name,"centro":centro,"area":area})
        else:
            #print("no boxes")
            #led.apaga()
            #stepper.fin()
            pass
            
            
        # display the image to our screen
        if mostrar:
            cv2.imshow("Facial Recognition is Running", frame)
        
       
        key = cv2.pollKey()& 0xFF# cv2.waitKey(1)& 0xFF#cv2.pollKey()#cv2.waitKey(1) #& 0xFF
        
        # update the FPS counter
        self.fps.update()
        #devuelve lista con datos de cada cara encontrada
        
        
        return({"key":key,"listacaras":listacaras})
        
    def stop(self):
        # stop the timer and display FPS information
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        cv2.destroyAllWindows()
        self.vs.stop()
            

if __name__ == '__main__':
    
    detect=Detector(ancho=250, flip=0)
   
    while True:
        captura=detect.foto(mostrar=1)
        #print(captura["listacaras"])
        listacaras=captura["listacaras"]
        key=captura["key"]
        if len(listacaras)>0:
            for cara in listacaras:
                print(cara)
                print("nombre: ", cara["nombre"])
                print("coordenada x: ", cara["centro"][0])
                print("coordenada y: ", cara["centro"][1])
                print("área: ", cara["area"])
            detect.guardafoto("testCV")
            
        #key = cv2.waitKey(1) & 0xFF
        #cv2.pollKey(1)
        #if key == ord("q"):
         #   break
    detect.stop()

