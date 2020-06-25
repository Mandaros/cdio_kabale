# https://docs.opencv.org/4.3.0/index.html

from tkinter import *
import cv2
import numpy
import time
from PIL import Image
from PIL import ImageTk
import threading
import CardClass


class CV:
    def __init__(self, tk, gui, sizeX, sizeY, mode):
        self.tk = tk  # pointer til GUI
        self.gui = gui  # variable til kommando
        self.gpuMode = mode

        self.data = []
        self.lock = threading.Lock()

        # Window størrelse
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.drawBorderFlag = True

        self.intervalY = sizeY / 4

        self.panel = Label(tk)

    def videoStream(self):
        # file paths
        namesPath = "yoloFiles/cards.names"
        weightsPath = "yoloFiles/yolo-obj3_best.weights"
        cfgPath = "yoloFiles/yolo-obj3.cfg"
        
        # webcam 40 cm over kabale
        # (768, 768) er ideel.
        # blobsize skal være dividerbar med 32
        # pga. kaldet til net.forward(outputLayers)
        blobSize = (768, 768)
        
        # procent sikker før der reageres
        conPer = 0.9
        font = cv2.FONT_HERSHEY_PLAIN
        
        # text farve i BGR
        # https://docs.opencv.org/2.4/doc/tutorials/core/basic_geometric_drawing/basic_geometric_drawing.html#scalar
        color = (0, 0, 0)

        # read(): Reads the file
        # strip(): Remove spaces
        # split(): Creates a list
        classes = open(namesPath).read().strip().split('\n')

        # Reads the deep learning network from Darknet framework
        net = cv2.dnn.readNet(weightsPath, cfgPath)
        
        # runs on GPU with CUDA
        if self.gpuMode:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        # runs on CPU only
        else:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        # gets the internal layer names
        # https://towardsdatascience.com/yolo-v3-object-detection-53fb7d3bfe6b
        layerNames = net.getLayerNames()
        
        # Returns indexes of layers with unconnected outputs.
        outputLayers = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        
        # uses camera 0. If there's more than one camera use 1, 2, ...
        # for GPU
        if self.gpuMode:
            cap = cv2.VideoCapture(0)
        # uses camera 0 with added DirectShow. If there's more than one camera use 1, 2, ...
        # for CPU
        else:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Sets the VideoCapture property.
        # First argument is the property to change
        # Second argument is the value to set
        # here it's the frame size
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.sizeX)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.sizeX)

        while True:
            startTime = time.time()

            # Læser billed fra webcam
            success, frame = cap.read()
            height, width, _ = frame.shape

            # Detect objects
            blob = cv2.dnn.blobFromImage(frame,          # image
                                         1.0 / 255.0,    # scaleFactor
                                         blobSize,       # Size
                                         (0, 0, 0),      # Scaler
                                         True,           # swapRB
                                         crop = False    # Crop
            )
            
            # Sets the new input value for the network. 
            net.setInput(blob)
            
            # Runs forward pass to compute output of layer
            outs = net.forward(outputLayers)

            # Show information in frame
            classIDs = []
            confidences = []
            boxes = []
            
            # goes through all the layers and calculates the confidences
            # only acts on it if the confidence with greater than the thresshold.
            for out in outs:
                for detection in out:
                    score = detection[5:]
                    class_id = numpy.argmax(score)
                    con = score[class_id]
                    if con > conPer:
                        # Object detected
                        centerX = int(detection[0] * width)
                        centerY = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordainates
                        x = int(centerX - w / 2)
                        y = int(centerY - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(con))
                        classIDs.append(class_id)

            # Performs Non-Maximum Suppression
            # i.e. edge detection
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            if self.drawBorderFlag:
                self.drawBorders(frame)

            self.lock.acquire()
            self.data.clear()
            
            # draw the rectangles and confidences
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[classIDs[i]])
                    con = confidences[i]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + str(round(con, 2)), (x, y - 5), font, 1, color, 2)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), 4)

                    num, type = self.getInfoFromLabel(label)
                    self.data.append(CardClass.Card(int(num), type, int(x), int(y), con))
            self.lock.release()

            # resizes the frame
            if width != 720 and height != 960:
                frame = cv2.resize(frame, (960, 720), interpolation = cv2.INTER_AREA)

            # Webcam feed i GUI
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img
            
            # Prints the FPS we get
            print("FPS: ", round(1.0 / (time.time() - startTime), 2))
            
            # Waits for a pressed key.
            cv2.waitKey(1)
            # end for loop
        
        # Closes video file or capturing device. 
        cap.release()
        #end while loop
        
    # end videoStream

    def getInfoFromLabel(self, label):
        if len(label) == 2:
            num = label[0]
            type = label[1]
        else:
            num = label[0] + label[1]
            type = label[2]

        if type == "C":
            return num, "Clubs"
        elif type == "D":
            return num, "Diamonds"
        elif type == "S":
            return num, "Spades"
        elif type == "H":
            return num, "Hearts"

        return None, None

    def drawBorders(self, frame):
        color = (0, 165, 255)
        thickness = 6

        width = frame.shape[1]
        height = frame.shape[0]
        wI = width / 7
        hI = int(self.intervalY)

        # Tegner vandret linje
        sPoint = (0, hI)
        ePoint = (width, hI)
        frame = cv2.line(frame, sPoint, ePoint, color, thickness)

        for i in range(6):
            if i != 1:
                sPoint = (int(wI * (i + 1)), 0)
            else:
                sPoint = (int(wI * (i + 1)), hI)
            ePoint = (int(wI * (i + 1)), height)
            frame = cv2.line(frame, sPoint, ePoint, color, thickness)

        return frame

    def getDataList(self):
        return self.data
