from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	tokenT (string): the token type (silver or golden) (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
	    tokenT=token.info.marker_type
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, tokenT

def Sector_min(dist, rot_y_min, rot_y_max):
    """this method return the distance of the nearest golden token in the circular sector around the robot specified by rot_y_min, rot_y_max angles and the radius dist"""
    S=[]  
    for token in R.see():
        if token.dist < dist and rot_y_min <= token.rot_y <= rot_y_max and token.info.marker_type == MARKER_TOKEN_GOLD:
            S.append([token.dist , token.rot_y])  
    try: 
        """the try - except function is used to handle the case when there is no golden token in the circular sector"""     
        S_min = min(S , key=lambda x: x[0])
    except:
        S_min=[1000, 1000, 1000]
    return S_min[0]

def Grab_token():
    """ this method uses the robot methods drive(),turn(),grab() and release() with the find_token() methods specified above to find a silver token near the robot, grab it, turn, release the token and
    return to the position when the robot has grabbed the token"""
    while 1:
        dist, rot_y , tokenT = find_token()
        if dist < d_th and tokenT == MARKER_TOKEN_SILVER and -a_th <= rot_y <= a_th :
            """in this case i'm near a silver token and i want to move it behind me and return to the initial position""" 
            print("Found it")
            R.grab() 
            print("Grabbed") 
            turn(12 , 5)
            drive(10 , 2)
            R.release()
            print("released")
            drive(-10 , 2)
            turn(-12 , 5)
            break
        elif -a_th <= rot_y <= a_th and tokenT == MARKER_TOKEN_SILVER:  
            """ in this case we're alligned with the token and we've just to reach it"""
            print("i've found a silver token")
            drive(10, 0.5)
        elif -90 < rot_y < -a_th and tokenT == MARKER_TOKEN_SILVER:
            """ in this case to allign with the token we've to turn left a bit"""
            print("left a bit...")
            turn(-3, 0.5)
        elif 90 > rot_y > a_th and tokenT == MARKER_TOKEN_SILVER:
            """ in this case to allign with the token we've to turn right a bit"""
            print("right a bit...")
            turn(3, 0.5)
        else:
            break

def Avoid_guardrail():
    """this method is used to avoid the arena's boundaries composed by golden token"""
    Ss=[Sector_min(10, -15, 15), Sector_min(10, -70, -15), Sector_min(10, 15, 70)]
    if min(Ss) == Ss[0] and Sector_min(10, -100, -80)-Sector_min(10, 80, 100) < -0.5 and Ss[0]<1.8:
        """in this case the robot has a near part of the boundaries in front of him and at his left, so to avoid it it has to turn right"""
        print("guardrail at my left and in front of me")
        turn(5, 1)
    elif min(Ss) == Ss[0] and Sector_min(10, -100, -80)-Sector_min(10, 80, 100) > 0.5 and Ss[0]<1.8:
        """in this case the robot has a near part of the boundaries in front of him and at his right, so to avoid it it has to turn left"""
        print("guardrail at my right and in fron of me")
        turn(-5, 1)   
    elif min(Ss) == Ss[0] and -0.5 < Sector_min(10, -100, -80)-Sector_min(10, 80, 100) < 0.5 and Ss[0]<1.8:
        """in this case the robot has a near part of the boundaries in front of him and the distance between the robot and the boundarie at his left and right is almost the same,
        so to avoid the beginning of a infinity loop where the robot turn right and then left i've decided to consider a different circular sector for the boundaries at the left and the right more
        closer to the driving direction"""
        if Sector_min(10, -80, -60)-Sector_min(10, 60, 80) > 0.5:
            print("guardrail at my right and in fron of me")
            turn(-5, 1)
        elif Sector_min(10, -80, -60)-Sector_min(10, 60, 80) < -0.5:
            print("guardrail at my left and in fron of me")
            turn(5, 1)             
    elif min(Ss) == Ss[1] and Ss[1]<0.8 :
        """ in this case the boundarie is near the robot at his left so it has to turn right a bit"""
        print("guardrail at my left")
        turn(10, 0.5)
    elif min(Ss) == Ss[2] and Ss[2]<0.8:
        """ in this case the boundarie is near the robot at his left so it has to turn right a bit"""
        print("guardrail at my right")
        turn(-10, 0.5)
    else:
        """ in this case the robot is far enough from the boundarie and it can drive straight"""
        drive(20, 0.5)
        print("driving")

def main():
    """ to accomplish the required task the robot has to find and grab the tokens while it avoid the boundaries"""
    while 1:
        Grab_token()        
        Avoid_guardrail()
      
main()
