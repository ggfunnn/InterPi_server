from flask import request
import time
import requests
import RPi.GPIO as GPIO
import os
import configparser


class Interpi_server(object):
    def __init__(self):

        path = os.path.dirname(os.path.realpath(__file__))
        config = configparser.ConfigParser()
        config.read(path + '/config.ini')

        self.PINS = {
            'lock_relay': int(config['interpi_server']['lock_relay_pin'])
            }

        self.STATES = {
            'ON': 0,
            'OFF': 1

        }

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.PINS['lock_relay'], GPIO.OUT)
        GPIO.output(self.PINS['lock_relay'], GPIO.HIGH)

    def __del__(self):
        GPIO.cleanup()
        os.system('pkill python3')

    def unlock(self):
        if request.method == 'POST':
            if GPIO.input(self.PINS['lock_relay']) == self.STATES['OFF']:
    #       TODO: log jaki requester
                GPIO.output(self.PINS['lock_relay'], GPIO.LOW)

                return {'result': 'OK'}

            else:
                return {'result': 'Error: Already unlocked'}

        else:
            return {'result': 'Error 400: Bad request method'}

    def lock(self):
        if request.method == 'POST':
            if GPIO.input(self.PINS['lock_relay']) == self.STATES['ON']:
    #       TODO: log jaki requester
                GPIO.output(self.PINS['lock_relay'], GPIO.HIGH)

                return {'result': 'OK'}

            else:
                return {'result': 'Error: Already locked'}

        else:
            return {'result': 'Error 400: Bad request method'}


class Button_daemon(object):
    """Class of deamon which waits for the gpio button input"""
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        config = configparser.ConfigParser()
        config.read(path + '/config.ini')

        self.groundflr_ipaddress = config['button_daemon']['groundflr_ipaddress']
        self.firstflr_ipaddress = config['button_daemon']['firstflr_ipaddress']
        self.groundflr_port = config['button_daemon']['groundflr_port']
        self.firstflr_port = config['button_daemon']['firstflr_port']
        self.hostname = config['button_daemon']['hostname']

        self.PINS = {
            'ground_floor_button': int(config['button_daemon']['groundflr_button_pin']),
            'first_floor_button': int(config['button_daemon']['firstflr_button_pin'])
            }

    def __del__(self):
        GPIO.cleanup()

    def initialize(self):
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.PINS['ground_floor_button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.PINS['first_floor_button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait(self):
        while True:
            if GPIO.input(self.PINS['ground_floor_button']) == 1:
                try:
                    self.__ring_ground_floor()

                except Exception as e:
                    print(e)

            elif GPIO.input(self.PINS['first_floor_button']) == 1:
                try:
                    self.__ring_first_floor()

                except Exception as e:
                    print(e)

            time.sleep(0.1)

    def __ring_ground_floor(self):
        request_url = 'http://' + self.groundflr_ipaddress + ':' + self.groundflr_port + '/ring/'

        r = requests.post(url=request_url, params={'name': self.hostname})

        if r.json() == {'result': 'OK'}:
#           TODO: log
            pass

        else:
            pass

    def __ring_first_floor(self):
        request_url = 'http://' + self.firstflr_ipaddress + ':' + self.firstflr_port + '/ring/'

        r = requests.post(url=request_url, params={'name': self.hostname})

        if r.json() == {'result': 'OK'}:
#           TODO: log
            pass

        else:
            pass
