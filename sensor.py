#Import Items needed to read TempSensor and connect via SSH
import csv
import datetime
import paramiko
import time
import board
import busio
import adafruit_mcp9808
from datetime import timedelta

#Define the abaility to edit/put a file on a remote device
def put_file(machinename, username,  dirname, passwd, filename, data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machinename,username=username,password=passwd)
    sftp = ssh.open_sftp()
    #try:
    #    sftp.mkdir(dirname)
    #except IOError:
    #    pass
    f = sftp.open(dirname + '/' + filename, 'a+')
    f.write(data)
    f.close()
    ssh.close()

i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)
tempC = mcp.temperature
tempF = tempC * 9/5+32
if float(tempF) >= 86:
    print('Danger, current temp is {} F, over the trehsold'.format(tempF))
    else:
    print('Temp {} F'.format(tempF))
time.sleep(2)
