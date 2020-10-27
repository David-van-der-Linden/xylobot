
import math



def angles_motor_1(x ,y):
    # physical constants
    L_1 = 120  # linkage 1 (short)
    L_2 = 240  # linkage 2 (long)
    m = 18.8  # distance between motor and the frame origin


    # input(new positions)

   # relations for angle 1
    a = - 2 * y *L_1
    b = 2* L_1 * (x - m)
    A = 1 / (a ** 2 + b ** 2) ** 0.5
    B = L_2 ** 2 - L_1 ** 2 - y ** 2 - m ** 2 - x ** 2 + 2 * m * x
    C = b / a
    theta = math.degrees(math.asin(A * B)) - math.degrees(math.atan(C))

    # motor angle 1
    theta_1 = -1*theta 
   

    return theta_1
    
   
def angles_motor_2(x,y):
    # physical constants
    L_1 = 120       #linkage 1 (short)
    L_2 = 240       #linkage 2 (long)
    m = 18.8        #distance between motor and the frame origin

 
    ## relations for motor 2
    a = -2 * y * L_1
    b2 = 2 * L_1 * (-m - x)
    A = 1 / (a ** 2 + b2 ** 2) ** 0.5
    B = L_2 ** 2 - L_1 ** 2 - y ** 2 - m ** 2 - x ** 2 - 2 * m * x
    C = b2 / a
    theta2 = math.degrees(math.asin(A * B)) - math.degrees(math.atan(C))
    theta_b = -1 * theta2

    # motor angle 2
    theta_2 = 180 - theta_b

    return theta_2

#angles_motor_1(100,300)
#angles_motor_2(100,300)
