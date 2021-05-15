import DeltaRobot
import serial
import time
import cv2
import argparse
import numpy as np
from imutils.video import VideoStream
import imutils
import math

import os
dirname = os.path.dirname(__file__)

var1 = 0
var2 = 0
# Cai dat tham so doc weight, config va class name
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--config', default=os.path.join(dirname, 'weight_yolo/a.cfg'),
                help='path to yolo config file')
ap.add_argument('-w', '--weights', default=os.path.join(dirname, 'weight_yolo/a.weights'),
                help='path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', default=os.path.join(dirname, 'weight_yolo/a.names'),
                help='path to text file containing class names')
args = ap.parse_args()


classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNet(args.weights, args.config)


def get_color():
    return COLORS

# Ham tra ve output layer
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

# Ham ve cac hinh chu nhat va ten class
def draw_prediction(img, class_id, p, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id]) + ": " +str(int( p* 100)) + "%"
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Ham ve cac hinh chu nhat va ten class
def draw_target(img, class_id, p, x, y, x_plus_w, y_plus_h, color):
    label = str(classes[class_id]) + ": " +str(int( p* 100)) + "%"
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# tra ve toa do thuc cua delta
def imageToRealLocal(a, b, H1):
    # khoảng cách từ mặt cơ sở f đến mặt luống rau là H1 
    # P là chân đường phân giác từ camera hạ xuống theo mặt zOy PC=AC*BC/(AB+AC);BP=AB*BC/(AB+AC) coi BPC thằng hàng nhé
    PC = math.sqrt(680*680 + 200*200)*450/(math.sqrt(680*680 + 650*650) + math.sqrt(680*680 + 200*200))
    BP = 450 - PC
    # P1C1,B1P1 tương ứng với độ dài PC,BP ở độ cao H1
    B1P1 = BP * H1/680
    P1C1 = PC * H1/680
    # print(PC,BP,B1P1,P1C1)
    # A1B1,C1D1 là hai đáy lớn bé của hình thang ở chiều cao H1
    A1B1 = 800*H1/680
    C1D1 = 600*H1/680
    # h là chiều cao hình thang ở mặt đất , đất chạm bánh xe ấy
    h = 450
    # h1 là chiều cao hình thang ở độ cao h
    h1 = h * H1 / 680
    # Bắt đầu tính các thông số để ra tọa độ ở độ cao h1
    # y = (-0.000244*b*b + 0.8*b)*H1/680
    if (250 < b < 720/2):
        y = B1P1*b/360 + 15
    elif (b <= 250):
        y = B1P1*b/360 + 20
    else:
        # y = (0.537136*b + 31631/500)*H1/680
        y = B1P1 + P1C1*(b-360)/360
    # y = h1*b/720
    x1 = A1B1 * a / 1280
    print("y",y)
    if (a < 1280/2):
        # x4 = x2 + x3
        x4 = a/1280*(C1D1 -A1B1) + 100
        x2 = x4*b/720
        # x2 = x4*y/h1
        x = x1 + x2
    else:
        x4 = (1 - a/1280)*(C1D1 - A1B1) + 100
        x2 = x4 * b/720
        # x2 = x4 *y/h1
        x = x1 - x2
    # k/c từ tâm A1 đến camera
    yc = 640*H1/680
    xc = 370*H1/680
    # k/c từ camera đến gốc Delta
    xd = 20
    yd = 290
    #  Tọa độ thực với gốc là gốc của Delta
    yT = y - yc + yd
    xT = x - xc -xd
    return xT, yT


def detect_img():
    # Doc tu webcam
    # cap  = VideoStream(src=0).start()
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Doc ten cac class

    # Bat dau doc tu webcam
    # i=1
    # while (True):
        # Doc frame

    # ret,image = cap.read()
    # image = imutils.resize(frame, width=520)
        # i+=1
        # if i%20==0:
    # Resize va dua khung hinh vao mang predict
    image = cv2.imread("a.jpg")

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 1/255.0
    print(image.shape)

    # nomalize input va thay doi kich thuoc anh
    # the scale factor (1/255 to scale the pixel values to [0..1])
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    # Loc cac object trong khung hinh
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if (confidence > 0.5):
                # toa do tam
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                # Kich thuoc
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                # toa do goc tren ben trai 
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h, center_x, center_y])

    # loc cac box co diem so cao nhat
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Ve cac khung chu nhat quanh doi tuong
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        #draw_prediction(image, class_ids[i], confidences[i], int(x), int(y), int(x + w), int(y + h))
    return image, confidence, class_ids, boxes, indices

def Tspeed(speed):
    ser.write("S {speed}")
    var2 = 1

def run(indices, boxes):
    for i in indices:
        i = i[0]
        box = boxes[i]
        center_x = box[4]
        center_y = box[5]
        
        # coi như mặt đất cách mặt cơ sở 500
        H1 = 500
        # H1 là chiều cao đến mặt rau
        xT,yT = imageToRealLocal(center_x, center_y, H1)
        # coi như delta sẽ làm việc ở độ cao 300
        # print(xT, yT, class_ids[i])
        if class_ids[i] == 0:
            theta1, theta2, theta3 = DeltaRobot.reverse(xT, yT, -300)
            if theta1*theta2*theta3 == -1:
                continue
            while True:
                print("T {:.2f} {:.2f} {:.2f}".format(theta1, theta2, theta3))
                with serial.Serial ("/dev/ttyS0", 9600, timeout=5) as ser:
                    ser.write("DSTT\n")
                    time.sleep(1)
                    status = ser.readLine()
                    if status.find("0") > 0:
                        ser.write("T {:.2f} {:.2f} {:.2f}".format(theta1, theta2, theta3))
                        break    

        # print(theta1, theta2, theta3)
        # time.sleep(1)

    # #cv2.imshow("object detection", image)
    #     # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     #     break
    # cv2.waitKey(0)
    #     # cap.stop()
    # cv2.destroyAllWindows()
