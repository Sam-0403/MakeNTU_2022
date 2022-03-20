# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(18, GPIO.OUT)
# GPIO.setup(22, GPIO.OUT)
# GPIO.setup(23, GPIO.OUT)

# while True:
#     ch = input("車子如何移動 f往前  b往後 l往左  r往右 q結束？")
#     if ch == 'q':
#        GPIO.output(17, False)
#        GPIO.output(18, False)
#        GPIO.output(22, False)
#        GPIO.output(23, False)
#        break
#     if ch == 'f':
#        GPIO.output(17, False)
#        GPIO.output(18, True)
#        GPIO.output(22, False)
#        GPIO.output(23, True)
#     if ch == 'b':
#        GPIO.output(17, True)
#        GPIO.output(18, False)
#        GPIO.output(22, True)
#        GPIO.output(23, False)
#     if ch == 'r':
#        GPIO.output(17, False)
#        GPIO.output(18, True)
#        GPIO.output(22, False)
#        GPIO.output(23, False)
#     if ch == 'l':
#        GPIO.output(17, False)
#        GPIO.output(18, False)
#        GPIO.output(22, False)
#        GPIO.output(23, True)

import time
import RPi.GPIO as GPIO

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def switch2deg(deg):
    dc = angle_to_duty_cycle(deg)
    pwm.ChangeDutyCycle(dc)

degrees = [45, 90, 135, 90]

for i in range(5):
    for deg in degrees:
        switch2deg(deg)
        time.sleep(0.5)

pwm.stop()
GPIO.cleanup()