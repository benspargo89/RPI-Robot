import RPi.GPIO as GPIO
from params import params
import time
GPIO.setmode(GPIO.BCM)

def check_distance(n_readings=3, print_distance=False):
    try:
        GPIO.setmode(GPIO.BCM)
        PIN_TRIGGER = params['Trigger']
        PIN_ECHO = params['Echo']
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        readings = []
        for reading in range(n_readings):
            GPIO.output(PIN_TRIGGER, GPIO.LOW)
            time.sleep(.001)
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)
            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            readings.append(distance)
        median_distance = readings[int(len(readings)/2)]
        if print_distance:
            print("Distance:",median_distance,"cm")
        return median_distance
    except:
        return None
