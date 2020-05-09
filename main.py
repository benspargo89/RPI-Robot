from gpiozero import DistanceSensor
from motor import move
from params import params


distance_sensor = DistanceSensor(params['Echo'], params['Trigger'], max_distance=3)