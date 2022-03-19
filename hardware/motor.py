import RPi.GPIO as GPIO
import time
 
CONTROL_PIN_1 = 18
CONTROL_PIN_2 = 12
 
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(CONTROL_PIN_1, GPIO.OUT)
GPIO.setup(CONTROL_PIN_2, GPIO.OUT)
 
try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        print('開始正向轉動')
        GPIO.output(CONTROL_PIN_1, GPIO.HIGH)
        GPIO.output(CONTROL_PIN_2, GPIO.LOW)
        time.sleep(3)
        print('停止轉動')
        GPIO.output(CONTROL_PIN_1, GPIO.LOW)
        GPIO.output(CONTROL_PIN_2, GPIO.LOW)
        time.sleep(3)
        print('開始反向轉動')
        GPIO.output(CONTROL_PIN_1, GPIO.LOW)
        GPIO.output(CONTROL_PIN_2, GPIO.HIGH)
        time.sleep(3)
        print('停止轉動')
        GPIO.output(CONTROL_PIN_1, GPIO.HIGH)
        GPIO.output(CONTROL_PIN_2, GPIO.HIGH)
        time.sleep(3)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()