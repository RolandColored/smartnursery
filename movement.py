from datetime import datetime

import requests

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_PIR = 4

musiccast_endpoint = 'http://Kinderzimmer/YamahaExtendedControl/v1/main/'
last_movement = datetime.now()
playing_music = False


def play_music():
    global playing_music

    if not playing_music:
        print('Playing music')
        assert requests.get(musiccast_endpoint + 'setPower?power=on').status_code == 200
        assert requests.get(musiccast_endpoint + 'setInput?input=net_radio').status_code == 200
        assert requests.get(musiccast_endpoint + 'setPlayback?playback=play').status_code == 200
        playing_music = True


def stop_music():
    global playing_music

    if playing_music:
        print('Stopping music')
        assert requests.get(musiccast_endpoint + 'setPower?power=standby').status_code == 200
        playing_music = False


def movement_callback(_):
    global last_movement

    print('moved')
    last_movement = datetime.now()
    play_music()


if __name__ == '__main__':
    try:
        GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(GPIO_PIR, GPIO.RISING, callback=movement_callback)
        print('Started')

        while True:
            if (datetime.now() - last_movement).seconds > 60:
                stop_music()

            time.sleep(0.1)

    finally:
        print('Cleaning up')
        stop_music()
        GPIO.cleanup()
