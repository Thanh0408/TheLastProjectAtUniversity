# start venv
# source /home/thanh/Documents/Study/python-test/myenv/bin/activate


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
from goto import goto, label


class ImgProcessing():
    def __init__(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        # Cai dat tham so doc weight, config va class name
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument('-c', '--config', default=os.path.join(self.dirname, 'weight_yolo/a.cfg'),
                        help='path to yolo config file')
        self.ap.add_argument('-w', '--weights', default=os.path.join(self.dirname, 'weight_yolo/a.weights'),
                        help='path to yolo pre-trained weights')
        self.ap.add_argument('-cl', '--classes', default=os.path.join(self.dirname, 'weight_yolo/a.names'),
                        help='path to text file containing class names')
        self.args = self.ap.parse_args()


        self.classes = None

        with open(self.args.classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.COLORS = np.array([[0.0, 0.0, 255.0], [0.0, 255.0, 0.0]])
        self.net = cv2.dnn.readNet(self.args.weights, self.args.config)


    def get_color(self):
        return self.COLORS

    # Ham tra ve output layer
    def get_output_layers(self, net):
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers

    # Ham ve cac hinh chu nhat va ten class
    def draw_prediction(self, img, class_id, p, x, y, x_plus_w, y_plus_h):
        label = str(self.classes[class_id]) + ": " +str(int( p* 100)) + "%"
        color = self.COLORS[class_id]
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 10)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 10)
        return img

    # Ham ve cac hinh chu nhat va ten class
    def draw_target(self, img, class_id, p, x, y, x_plus_w, y_plus_h, color):
        label = str(self.classes[class_id]) + ": " +str(int( p* 100)) + "%"
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 10)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 10)
        return img


    # tra ve toa do thuc cua delta
    def imageToRealLocal(self, a, b, H1):
        # khoảng cách từ mặt cơ sở f đến mặt luống rau là H1
        # P là chân đường phân giác từ camera hạ xuống theo mặt zOy PC=AC*BC/(AB+AC);BP=AB*BC/(AB+AC) coi BPC thằng hàng nhé
        NP = math.sqrt(680*680 + 200*200)*450/(math.sqrt(680*680 + 650*650) + math.sqrt(680*680 + 200*200))
        MP = 450 - PC
        # P1C1,B1P1 tương ứng với độ dài PC,BP ở độ cao H1
        M1P1 = MP * H1/680
        N1P1 = NP * H1/680
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

        """
        if (b<=360):
            y=N1P1*b/360
            if(a < 640):
                x = H1/680 * 800 *a / 1280 + y/450 *(686-800)(a/1280 - 1/2)
            else:
                x = H1/680 * 800 *a / 1280 - y/450 *(800-686)(a/1280 - 1/2)
        else:
            y=N1P1+M1P1*(b-360)/360
            if(a < 640):
                x = H1/680 * 686 *a / 1280 + y/450 *(600-686)(a/1280 - 1/2)
            else:
                x = H1/680 * 686 *a / 1280 - y/450 *(686-600)(a/1280 - 1/2)

        """

        if (250 < b < 720/2):
            y = M1P1*b/360 + 15
        elif (b <= 250):
            y = M1P1*b/360 + 20
        else:
            # y = (0.537136*b + 31631/500)*H1/680
            y = M1P1 + N1P1*(b-360)/360
        # y = h1*b/720
        x1 = A1B1 * a / 1280
        if (a < 1280/2):
            # x4 = x2 + x3
            x4 = a/1280*(C1D1 -A1B1) + 100
            # 100 = 84 = (C1D1-A1B1)/2
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

    def detect_img(self):
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
        image = cv2.imread(os.path.join(self.dirname, '../../img/c.jpg'))
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 1/255.0
        print(image.shape)

        # nomalize input va thay doi kich thuoc anh
        # the scale factor (1/255 to scale the pixel values to [0..1])
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers(self.net))

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
        num_x = 0
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            image = self.draw_prediction(image, class_ids[i], confidences[i], int(x), int(y), int(x + w), int(y + h))
            if(class_ids[i] == 0):
                num_x = num_x + 1
        return image, confidence, class_ids, boxes, indices, num_x

    def Tspeed(self, speed):
        x = 0
        while(x == 0):
            x = x + 1
            with serial.Serial ("/dev/ttyUSB0", 9600, timeout=5) as ser:
                ser.flushInput()
                ser.flushOutput()
                time.sleep(1)
                ser.write(b"S {:.0f}\n".format(speed))
                time.sleep(1)
                ser.close()

    def run(self, indices, boxes, class_ids, ui, number_stop):
        count = 0
        number_stop = 0
        for i in indices:
            i = i[0]
            box = boxes[i]
            center_x = box[4]
            center_y = box[5]

            # coi như mặt đất cách mặt cơ sở 500
            H1 = 500
            # H1 là chiều cao đến mặt rau
            xT,yT = self.imageToRealLocal(center_x, center_y, H1)
            # coi như delta sẽ làm việc ở độ cao 300
            # print(xT, yT, class_ids[i])
            if class_ids[i] == 0:
                theta1, theta2, theta3 = DeltaRobot.reverse(xT, yT, -300)
                if theta1*theta2*theta3 == -1:
                    continue
                can_send = False
                while True:
                    with serial.Serial ("/dev/ttyUSB0", 9600, timeout=5) as ser:
                        ser.flushInput()
                        ser.flushOutput()
                        print("Check status....")
                        time.sleep(1)
                        ser.write(b"DSTT\n")
                        status = ser.readline().decode(encoding = 'UTF-8')
                        print('get status: ' + status)
                        time.sleep(1)
                        ser.close()
                        if number_stop:
                            goto .end
                        if status.find('0') >= 0:
                            can_send = True

                    if can_send:
                        with serial.Serial ("/dev/ttyUSB0", 9600, timeout=5) as ser:
                            ser.flushInput()
                            ser.flushOutput()
                            cmd = "T {:.2f} {:.2f} {:.2f}\n\r".format(theta1, theta2, theta3)
                            print("Sending cmd: " + cmd)
                            time.sleep(1);
                            ser.flushOutput()
                            ser.write(str.encode(cmd))
                            ser.flush()
                            time.sleep(1);
                            status = ser.readline().decode(encoding = 'UTF-8')
                            print('get cmd: ' + status)
                            count = count + 1
                            ui.num_done.setText(str(count))
                            num_detected = int(ui.num_detected.text())
                            per = "{:.0f}".format(count/num_detected * 100) + "%"
                            ui.performance.setText(str(per))
                            time.sleep(1)
                            ser.close()
                            break
        
        label .end
        with serial.Serial ("/dev/ttyUSB0", 9600, timeout=5) as ser:
            ser.flushInput()
            ser.flushOutput()
            time.sleep(1);
            ser.write(b"H\n")
            time.sleep(1);
            ser.close()
            break
            # print(theta1, theta2, theta3)
            # time.sleep(1)

        # #cv2.imshow("object detection", image)
        #     # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     #     break
        # cv2.waitKey(0)
        #     # cap.stop()
        # cv2.destroyAllWindows()
