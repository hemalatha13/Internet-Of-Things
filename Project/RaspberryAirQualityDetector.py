#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import httplib, urllib
import time
import os
import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
DHTpin = 26
import smtplib

sleep = 5 # how many seconds to sleep between posts to the channel

fromaddr = 'your email2@gmail.com'
toaddrs  = 'destination email@.com'
# Credentials
username = 'your email@gmail.com'
password = 'your password'





GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout








# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# sensor connected to adc #0
sensor_adc = 0;

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'




#Report Raspberry Pi readings to Thingspeak Channel
def calculate():
    while True:
        temp = trim_pot

        #calculate DHT
        RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
        #Convert from Celius to Farenheit
        TWF = 9/5*TW+32

        print "temperature is"
        print TWF
        print "humidity is"
        print RHW
        print "sending value to thingspeak"
        params = urllib.urlencode({'field8': temp,'key':'6KYI9OPAE7WRCZL2'})
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print "response time is"
            print response.status, response.reason
            print " "
            data = response.read()
        except:
            print "connection failed"
            
        params = urllib.urlencode({'field4': RHW,'key':'6KYI9OPAE7WRCZL2'})        
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        params = urllib.urlencode({'field2': TWF,'key':'6KYI9OPAE7WRCZL2'})        
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params, headers)
        conn.close()            


        if (TWF>75):
            subject = 'Room2 alert'
            text = 'Temperature high!!!'
            msg = 'Subject: %s\n\n%s' % (subject, text)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
        if (temp>566):
            print " sending mail"
            subject = 'Room2 alert'
            text = 'Air Quality badd!!!'
            msg = 'Subject: %s\n\n%s' % (subject, text)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
        break


  

        




while True:
        # we'll assume that the pot didn't move
        trim_pot_changed = False

        # read the analog pin
        trim_pot = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - last_read)

        if DEBUG:
                print "quality:", trim_pot
                print "last_read", last_read

        if ( pot_adjust > tolerance ):
               trim_pot_changed = True


        if ( trim_pot_changed ):
                set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                set_volume = round(set_volume)          # round out decimal value
                set_volume = int(set_volume)            # cast volume as integer

                set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
                os.system(set_vol_cmd)  # set volume

                # save the potentiometer reading for the next loop
                last_read = trim_pot

        # hang out and do nothing for a half second
        calculate()
        time.sleep(sleep)




        
