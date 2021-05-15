import

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

def run(indices, boxes, ui):
    count=0
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
                # thong bao la ngoai pham vi len ui (bao loi)
                continue
            while True:
                # print("T {:.2f} {:.2f} {:.2f}".format(theta1, theta2, theta3))
                # with serial.Serial ("/dev/ttyS0", 9600, timeout=5) as ser:
                #     ser.write("DSTT\n")
                #     time.sleep(1)
                #     status = ser.readLine()
                #     if status.find("0") > 0:
                #         ser.write("T {:.2f} {:.2f} {:.2f}".format(theta1, theta2, theta3))
                #         break

                # for test
                count = count + 1
                time.sleep(1)
                ui.num_done.setText(str(count))

        # print(theta1, theta2, theta3)
        # time.sleep(1)
