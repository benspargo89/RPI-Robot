from gpiozero import Motor
from params import params
from time import sleep


right_motor = Motor(forward=params['M2'], backward=params['M3'])
left_motor = Motor(forward=params['M4'], backward=params['M3'])

def move(direction="F", timed=False, delay=1):
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
    right_motor.stop()
    left_motor.stop()
