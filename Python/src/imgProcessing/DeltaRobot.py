import math

cos120 = math.cos(2 * math.pi / 3)
sin120 = math.sin(2 * math.pi / 3)
cos240 = math.cos(4 * math.pi / 3)
sin240 = math.sin(4 * math.pi / 3)

f = 100
La = 165
Lb = 340
e = 50

# Ham chuyen tu toa do ve goc
def reverse(x, y, z):
    try:
        theta1 = calcAngle(x, y, z)
        theta2 = calcAngle(x * cos120 - y * sin120, x * sin120 + y * cos120, z)
        theta3 = calcAngle(x * cos240 - y * sin240, x * sin240 + y * cos240, z)
        theta1 += 58.5
        theta2 += 65.76
        theta3 += 65.76
        return theta1, theta2, theta3
    except:
        return -1, -1, -1

def calcAngle(x, y, z):
    T = f + x - e
    K = Lb * Lb - y * y - T * T - z * z - La * La
    
    e1 = 2 * T * La + K
    e2 = -4 * z * La
    e3 = -2 * T * La + K

    theta = 2 * math.atan((-e2 + math.sqrt(e2 * e2 - 4 * e1 * e3)) / (2 * e1))
    theta = theta * 180 / math.pi
    thetamax = theta + 180
    thetamin = theta - 180
    if thetamax > -58.5 and thetamax < 77.71:
        return thetamax
    elif thetamin > -58.5 and thetamin < 77.71:
        return thetamin
    elif theta > -58.5 and theta < 77.71:
        return theta
    else:
        raise ArgumentException("Position failed")

