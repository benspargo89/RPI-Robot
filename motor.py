from gpiozero import Motor, Robot
from params import params
from time import sleep

robot = Robot(right=(params['M2'], params['M1']), left=(params['M4'], params['M3']))

right_motor = Motor(forward=params['M2'], backward=params['M1'], pwm=True)
left_motor = Motor(forward=params['M4'], backward=params['M3'], pwm=True)

def approach2(angles):
    if angles[0] > 5:
        move(direction='L', autostop=False)
    if angles[0] < -5:
        move(direction='R', autostop=False)
    else:
        move(direction='F', autostop=False)


def approach(point):
    theta = point / 640
    right_speed = (1 - theta) * .6 + .4 
    left_speed  = theta * .6 + .4
    left_motor.forward(speed=left_speed)
    right_motor.forward(speed=right_speed)

def move(direction="F", timed=False, delay=1, autostop=True):
    """
    Primary function to move the robot. Function takes a direction 
    - F, B, R, L - and optionaly a time to move.
    """
    direction = direction.upper()
    if direction == "F":
        right_motor.forward()
        left_motor.forward() 
    elif direction == "B":
        right_motor.backward()
        left_motor.backward()               
    elif direction == "L":
        right_motor.forward()
        left_motor.backward()
    elif direction == "R":
        right_motor.backward()
        left_motor.forward()
    else:
        print(f'ERROR: {direction} is not a valid command.')
    if timed:
        sleep(delay)
    if autostop:    
        right_motor.stop()
        left_motor.stop()
