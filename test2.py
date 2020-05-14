from gpiozero import DigitalInputDevice, Robot, InputDevice, Motor
from time import sleep, time

class Encoded_Motor(object):
    def __init__(self, name, encoder_pin_1, encoder_pin_2, motor_pin_1, motor_pin_2):
        self.name                       = name
        self.time                       = time()
        self.motor_active               = False
        self.rotation_made              = False
        self.debug                      = False
        self.motor_direction            = 'S'
        self._value                     = 0
        self.total_value                = 0
        self.speed                      = .75
        self.last_reading               = 70
        self.target_speed               = 70
        self.p_gain                     = .25
        self.last_error                 = 0
        self.d_gain                     = .05
        self.motor                      = Motor(forward=motor_pin_1, backward=motor_pin_2)
        self.encoder_1                  = DigitalInputDevice(encoder_pin_1, pull_up=True)
        self.encoder_2                  = DigitalInputDevice(encoder_pin_2, pull_up=True)
        self.encoder_1.when_activated   = self._increment
        self.encoder_1.when_deactivated = self._increment
        self.encoder_2.when_activated   = self._increment
        self.encoder_2.when_deactivated = self._increment

    def reset(self):
        self._value = 0

    def _increment(self):
        self._value += 1
        if time() - self.time > .1:
            if time() - self.time < .125:
                if self.debug:
                    print(self.name, 'Encoder Value:', self._value, 'Speed:', self.speed, 'Total Value', self.total_value)
                if not self.rotation_made:
                    self.rotation_made = True
                    self.total_value += self._value
                    self.reset()
                else:
                    self.total_value += self._value
                    self.update_speed()
            else:
                self.time = time()
                self.total_value += self._value
                self.reset()
            if self.motor_active:
                self.move(direction=self.motor_direction)

    def update_speed(self):
            self.last_reading = self._value
            self.reset()
            p = min(((self.target_speed - self.last_reading) / self.target_speed) * self.p_gain * self.speed, .125)
            d = self.last_error * self.d_gain
            self.last_error = p
            self.speed = min(self.speed + p + d, 1)
            self.time = time()

    @property
    def value(self):
        return self._value

    def move(self, direction='S'):
        if direction == 'F':
            self.motor.forward(speed=self.speed)
            self.motor_active = True
            self.motor_direction = direction
        elif direction == 'B':
            self.motor.backward(speed=self.speed)
            self.motor_active = True
            self.motor_direction = direction
        elif direction == 'S':
            self.motor.stop()
            self.motor_active = False
            self.motor_direction = direction
            self.rotation_made = False
            self.total_value = 0
        else:
            print('Invalid Motor Command')

FL = Encoded_Motor('Front Left', 4, 17, 2, 3)
FR = Encoded_Motor('Front Right', 19, 26, 20, 21)
BR = Encoded_Motor('Back Right', 8, 25, 16, 12)
BL = Encoded_Motor('Back Left', 23, 24, 1, 7)
FL.debug = True
FR.debug = True
FL.move(direction='F')
FR.move(direction='F')
sleep(10)
