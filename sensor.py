from time import sleep
import RPi.GPIO as GPIO
import spidev
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_Hz = 250000

GPIO.setmode(GPIO.BCM)
#GPIO.setup(14, GPIO.OUT)
#GPIO.setup(15, GPIO.OUT)

def poll_sensor(channel):
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1.'
    # First bit of cbyte is single=1 or diff=0.
    # Second bit is channel 0 or 1
    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000
          
      # Send (Start bit=1, cbyte=sgl/diff & odd/sign & MSBF = 0)
    r = spi.xfer2([1, cbyte, 0])
                                                                                                                                          # 10 bit value from returned bytes (bits 13-22):
      # XXXXXXXX, XXXX####, ######XX
    return ((r[1] & 31) << 6) + (r[2] >> 2)

try:
    while True:
        channel = 0
        channeldata = poll_sensor(channel)
        voltage = round(((channeldata * 3300)/1048),0)
        print('Voltage (mv): {}'.format(voltage))
        print('Data       :{}\n'.format(channelid))
finally:
    spi.close()
    GPIO.cleanup()
    print "\n All cleaned up."
