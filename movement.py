try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4


def movement_callback(_):
    print('moved')


if __name__ == '__main__':
    try:
        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(GPIO_PIR, GPIO.RISING, callback=movement_callback)
        print('Started')

        while True:
            time.sleep(1)

    finally:
        print('Cleaning up')
        GPIO.cleanup()
