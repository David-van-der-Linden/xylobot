
import math
class PID_pf(object):
    """
    PID in (pure) parallel form
    """
    

    def __init__(self, t_step, p_gain, i_gain, d_gain):
        """
        =INPUT=
            t_step - float
                Controller time step
            p_gain, i_gain, d_gain - float
                Proportional, integrative, differential controller gains
        """
        self.t_step = t_step
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain

        self.past_error = 0
        self.integrated_error = 0

        return

    def angles_motor_1(self,x,y):
        self.x=x
        self.y=y
   # physical constants
        L_1 = 120       #linkage 1 (short)
        L_2 = 240       #linkage 2 (long)
        m = 18.8        #distance between motor and the frame origin


    # input(new positions)

    #relations for angle 1
        a = -2*y*L_1
        b = 2*L_1*(x - m)
        A = 1/(a**2 + b**2)**0.5
        B = L_2**2 - L_1**2 - y**2 - m**2 - x**2 + 2*m*x
        C = b/a
        a_times_b = A*B
        if a_times_b <=-1:
            asin_ab = -1.5
        elif a_times_b >= 1:
            asin_ab = 1.5
        else:
            asin_ab =math.asin(A*B)
        theta = math.degrees(asin_ab) - math.degrees(math.atan(C))


        # motor angle 1
        theta_1 = -1*theta 
   

        return theta_1
    
   
    # def angles_motor_2(self,x,y):
    #  # physical constants
    #     L_1 = 120       #linkage 1 (short)
    #     L_2 = 240       #linkage 2 (long)
    #     m = 18.8        #distance between motor and the frame origin

    #     ## relations for motor 2
    #     a = -2*y*L_1
    #     b2 = 2*L_1*(-m - x)
    #     A = 1/(a**2 + b2**2)**0.5
    #     B = L_2**2 - L_1**2 - y**2 - m**2 - x**2 - 2*m*x
    #     C = b2/a
    #     theta2 = math.degrees(math.asin(A*B)) - math.degrees(math.atan(C))
    #     theta_b = -1*theta2 
        

    # # motor angle 2
    #     theta_2 = 180 - theta_b

    #     return theta_2

    #angles_motor_1(100,300)
    #angles_motor_2(100,300)

    def step(self, reference, measured, filtfun=None):
        """
        =INPUT=
            reference - float
            measured - float
            filtfun - callable
                Callable which takes a sample as input and filters it.
                Used only on the differential signal.
        """
        
        # Compute error, integrated error, and differential error
        error = reference - measured
        self.integrated_error += error * self.t_step
        differential_error = (error - self.past_error) / self.t_step

        # Filter if a filter function handle was supplied
        if filtfun is not None:
            differential_error = filtfun(differential_error)
        
        self.past_error = error

        return (self.p_gain * error+self.i_gain * self.integrated_error + self.d_gain * differential_error)