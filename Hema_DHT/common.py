# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

import time

import platform_detect


# Define error constants.
DHT_SUCCESS        =  0
DHT_ERROR_TIMEOUT  = -1
DHT_ERROR_CHECKSUM = -2
DHT_ERROR_ARGUMENT = -3
DHT_ERROR_GPIO     = -4
TRANSIENT_ERRORS = [DHT_ERROR_CHECKSUM, DHT_ERROR_TIMEOUT]

# Define sensor type constants.
DHT11  = 11
DHT22  = 22
AM2302 = 22
SENSORS = [DHT11, DHT22, AM2302]


def get_platform():
	"""Return a DHT platform interface for the currently detected platform."""
	plat = platform_detect.platform_detect()
	if plat == platform_detect.RASPBERRY_PI:
		# Check for version 1 or 2 of the pi.
		version = platform_detect.pi_version()
		if version == 1:
			import Raspberry_Pi
			return Raspberry_Pi
		elif version == 2:
			import Raspberry_Pi_2
			return Raspberry_Pi_2
		else:
			raise RuntimeError('No driver for detected Raspberry Pi version available!')
	elif plat == platform_detect.BEAGLEBONE_BLACK:
		import Beaglebone_Black
		return Beaglebone_Black
	else:
		raise RuntimeError('Unknown platform.')

def read(sensor, pin, platform=None):
	
	if sensor not in SENSORS:
		raise ValueError('Expected DHT11, DHT22, or AM2302 sensor value.')
	if platform is None:
		platform = get_platform()
	return platform.read(sensor, pin)

def read_retry(sensor, pin, retries=15, delay_seconds=2, platform=None):
	
	for i in range(retries):
		humidity, temperature = read(sensor, pin, platform)
		if humidity is not None and temperature is not None:
			return (humidity, temperature)
		time.sleep(delay_seconds)
	return (None, None)
