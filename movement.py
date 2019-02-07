from datetime import datetime

import requests

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO
import time
from rpi_rf import RFDevice

# movement detector
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4
last_movement = datetime.now()

# music device
musiccast_endpoint = 'http://Kinderzimmer/YamahaExtendedControl/v1/main/'
room_active = False

# power switch
enable_code = 5506385
disable_code = 5506388

GPIO_RF = 17
rfdevice = RFDevice(GPIO_RF)
rfdevice.enable_tx()


def play_music():
    print('Playing music')
    assert requests.get(musiccast_endpoint + 'setPower?power=on').status_code == 200
    assert requests.get(musiccast_endpoint + 'setInput?input=net_radio').status_code == 200
    assert requests.get(musiccast_endpoint + 'setPlayback?playback=play').status_code == 200


def stop_music():
    print('Stopping music')
    assert requests.get(musiccast_endpoint + 'setPower?power=standby').status_code == 200


def switch_lamp(code):
    print('Sending code ' + str(code))
    rfdevice.tx_code(code, 1, 350, 24)


def movement_callback(_):
    global last_movement, room_active

    print('Movement detected')
    last_movement = datetime.now()
    if not room_active:
        play_music()
        switch_lamp(enable_code)
        room_active = True


if __name__ == '__main__':
    try:
        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(GPIO_PIR, GPIO.RISING, callback=movement_callback)
        print('Started')

        while True:
            # timeout without movement
            if room_active and (datetime.now() - last_movement).seconds > 60:
                stop_music()
                switch_lamp(disable_code)
                room_active = False

            time.sleep(0.2)

    finally:
        print('Cleaning up')
        stop_music()
        GPIO.cleanup()
