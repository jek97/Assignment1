Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## assignment
-----------------------------

the assignment1.py file is composed by 6 main methods used to accomplish the requested task, which is to move the robot around the arena, rappresented by golden token, without touching it and each time the robot is near to a silver token grabs it and releases it behind the robot.
let we see these methods in detail:
* drive(speed, seconds): this method is used to move the robot straight ahead, it's arguments are the speed of the motors (expressed in meters/seconds) and the duration of the motion in seconds
  rappresented by the argument seconds.
  This function set the power of the two motors to the value specified by speed for a time interval specified by seconds, after that it set the speed to zero again.

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

* turn(speed, seconds): this method is used to turn the robot in place, it's arguments are the speed of the motors (expressed in meters/seconds) and the duration of the motion in seconds rappresented
  by the argument seconds.
  This function set the power of the two motors to the value specified by speed fot the right motor and to -speed for the left motor, for a time interval specified by seconds, after that it set the
  speed to zero again.

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

* find_token(): this method is used to identify the tokens near the robot and will return the polar coordinates of the token (dist, rot_y) and the token type (tokenT) (silver or gold), if there is no
  token it will return a distance equal to -1, an angle equal to -1 and a token type euqal to -1. 

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

* Sector_min(dist, rot_y_min, rot_y_max): this method return the distance of the nearest golden token respect the robot in the circular sector specified by the angles rot_y_min, rot_y_max and the
  radius equal to dist, more over the try-except function is used to handle the case when there is no token in the circular sector.

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

* Grab_token(): this method is used to grab the silver token any time the robot aproach one and move it behind him.
  Infact to grab a token the distance between the token and the robot must be less then d_th=0.4 and the angle between the robot front direction and the token must be less then a_th=2.

  def Grab_token():
      """ this method uses the robot methods drive(),turn(),grab() and release() with the find_token() methods specified above to find a silver token near the robot, grab it, turn, release the token
      and return to the position when the robot has grabbed the token"""
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
            
  To see how this method works we can see the pseudocode of it:
  
  grab_token(): method to grab the nearest silver token, leave it behind the robot, and return to the position when the token was grabbed.
  
      while ever: ( in this way the following command will be repeated untill the task accomplish)
      
          define the polar position and token type of the nearest token
          
          if the token is nearer then d_th, it's a silver token and it's in the angular grabbing range defined by a_th:
              
              grab the token
              
              turn of 180 degree
              
              move forward a bit
              
              release the token
              
              drive backward a bit
              
              turn again of 180 degree
              
              exit from the while loop
          
          else if the robot is alligned with the silver token but it's too far from it:
          
              drive forward to reach it
          
          else if the robot is not alligned with the silver token which is at his left:
          
              turn left a bit to allign with it
          
          else if the robot is not alligned with the silver token which is at his right:
          
              turn right a bit to allign with it
          
          else:
          
              exit from the while loop ( this is the case where there is no token near the robot )
              
* Avoid_guardrail(): this method is used to move the robot around the arena without inpact on his boundaries, which are composed by golden token.

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

  To see how this method works we can see the pseudocode of it:

  Avoid_guardrail(): this method moves the robot along the arena without inpact on his boundaries.
  
      define the list Ss of the distances of the nearest golden token rispectively in front of the robot (sector between the angles -15, 15 and a distance of 10), at his left ( sector between the
      angles -70, -15 and a distance of 10), at his right ( sector between the angles 15, 70 and a distance of 10).
      
      if the minimum golden token distance is in front of the robot (as defined in Ss[0]), it's less then 1.8 and the second minimum golden token distance is in the left sector (between the angles
      -100, -80 and a distance of 10) and at least less of 0.5 then the minimum golden token distance in the right sector (between the angles 80, 100 and a distance of 10):
         
          turn right a bit
          
      else if the minimum golden token distance is in front of the robot (as defined in Ss[0]), it's less then 1.8 and the second minimum golden token distance is in the right sector (between the 
      angles 80, 100 and a distance of 10) and at least less of 0.5 then the minimum golden token distance in the left sector (between the angles -100, -80 and a distance of 10):
         
          turn left a bit
          
      else if the minimum golden token distance is in front of the robot (as defined in Ss[0]), it's less then 1.8 and the difference between the minimum golden token distance in the left sector
      (between the angles -100, -80 and a distance of 10) and the minimum golden token distance in the right sector (between the angles 80, 100 and a distance of 10) is between -0.5 and 0.5: 
      (in this case the robot has a near part of the boundaries in front of him and the distance between the robot and the boundarie at his left and right is almost the same, so to avoid the beginning
      of a infinity loop where the robot turn right and then left i've decided to consider a different circular sector for the boundaries at the left and the right more closer to the driving direction)
          
          if the minimum golden token distance in the right sector (between the angles -80, -60 and a distance of 10) is greater of 0.5 then the minimum golden token distance in the left sector
          (between the angles 60, 80 and a distance of 10):
              
              turn left a bit   
               
          else if the minimum golden token distance in the left sector (between the angles 60, 80 and a distance of 10) is greater of 0.5 then the minimum golden token distance in the right sector
          (between the angles -80, -60 and a distance of 10):
              
              turn right a bit  
              
      else if the minimum golden token distance is in the left sector (as defined in Ss[1]) and it's less then 0.8:
          
          turn right a bit
          
      else if the minimum golden token distance is in the right sector (as defined in Ss[2]) and it's less then 0.8:
          
          turn left a bit
          
      else:
      
          drive forward
 
* main(): this method is basically composed rispectively by the two methods Grab_token() and Avoid_guardrail() used in a while loop with no end, in this way the method Grab_token() has the priority on
  the Avoid_guardrail() method when the robot find a silver token near him.
 
To run the assignment script in the simulator, use `run.py`, passing it the file names assignment1.py. 

```bash
$ python run.py assignment1.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
