import time
import urllib
import requests
from gpiozero import Servo
from time import sleep
import spidev
import json

from gpiozero.pins import pigpio
from scipy import stats
import re

servo = Servo(21)
val = 0
spi = spidev.SpiDev()
spi.open(0, 0)
# spi.max_speed_hz=1000000
spi.max_speed_hz = 1000000
datalist1 = []
datalist2 = []
datalist3 = []
filterRatio = 0.3
sampleSize = 10
limit = 28


def readChannel(channel):
    value = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((value[1] & 3) << 8) + value[2]
    return data


while True:
    zone = 'no zone'

    if __name__ == "__main__":
        v1 = (readChannel(0) / 1023.0) * 3.3
        v2 = (readChannel(1) / 1023.0) * 3.3
        v3 = (readChannel(2) / 1023.0) * 3.3

        if (8.53 * v1 ** 4 - 54.90 * v1 ** 3 + 131.26 * v1 ** 2 - 144.85 * v1 + 72.28 - 0.3) < 30:
            dist1 = (8.53 * v1 ** 4 - 54.90 * v1 ** 3 + 131.26 * v1 ** 2 - 144.85 * v1 + 72.28 - 0.3)
        else:
            dist1 = 30

        if (8.53 * v2 ** 4 - 54.90 * v2 ** 3 + 131.26 * v2 ** 2 - 144.85 * v2 + 72.28 - 0.3) < 30:
            dist2 = (8.53 * v2 ** 4 - 54.90 * v2 ** 3 + 131.26 * v2 ** 2 - 144.85 * v2 + 72.28 - 0.3)
        else:
            dist2 = 30

        if (8.53 * v3 ** 4 - 54.90 * v3 ** 3 + 131.26 * v3 ** 2 - 144.85 * v3 + 72.28 - 0.3) < 30:
            dist3 = (8.53 * v3 ** 4 - 54.90 * v3 ** 3 + 131.26 * v3 ** 2 - 144.85 * v3 + 72.28 - 0.3)
        else:
            dist3 = 30

    while len(datalist1) < sampleSize:
        datalist1.append(dist1)

    if len(datalist1) == sampleSize:
        finalDist1 = stats.trim_mean(datalist1, filterRatio)
        datalist1.pop(0)
        # print(finalDist1)

    while len(datalist2) < sampleSize:
        datalist2.append(dist2)

    if len(datalist2) == sampleSize:
        finalDist2 = stats.trim_mean(datalist2, filterRatio)
        datalist2.pop(0)
        # print(finalDist2)

    while len(datalist3) < sampleSize:
        datalist3.append(dist3)

    if len(datalist3) == sampleSize:
        finalDist3 = stats.trim_mean(datalist3, filterRatio)
        datalist3.pop(0)
        # print(finalDist3)

    servo.value = val
    # print("Dist 1 is " + str(dist1))
    # print("Dist 2 is " + str(dist2))
    # print("Dist 3 is " + str(dist3))
    # print("________________________")
    # time.sleep(1)

    url = "https://studev.groept.be/api/a21ib2d04/getSoundControl"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    onList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(onList)

    url = "https://studev.groept.be/api/a21ib2d04/getNrofpeople"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    peopleList = [int(num) for num in re.findall(r"\d+", str(data))]
    # peopleList[0] = 1 activate else dont

    if dist1>limit and dist2>limit and dist3>limit:# default
        zone = "zone5"
        val = 0.5

    if finalDist1 < limit and finalDist2 > limit and finalDist3 > limit and peopleList[0] == 1 and onList[0]==1:
        # print ("Distan 1: %.2f cm" % dist1)
        if finalDist1 < 10:
            zone = "1"
            val = 0.5
        else:
            if finalDist1 < 20:
                zone = "2"
                val = 0.2
            else:
                zone = "3"
                val = 0

    elif finalDist1 > limit and finalDist2 < limit and finalDist3 > limit and peopleList[0] == 1  and onList[0]==1:
        # print ("Distan 2: %.2f cm" % dist2)
        if dist2 < 10:
            zone = "4"
            val = 0.9
        else:
            if finalDist2 < 20:
                zone = "5"
                val = 0.5
            else:
                zone = "6"
                val = 0.3

    elif finalDist1 > limit and finalDist2 > limit and finalDist3 < limit and peopleList[0] == 1  and onList[0]==1:
        # print ("Distan 3: %.2f cm" % dist3)
        if dist3 < 10:
            zone = "7"
            val = 1
        else:
            if finalDist3 < 22.6:
                zone = "8"
                val = 0.8
            else:
                zone = "9"
                val = 0.5

    else:
        val = 0.5

    print(str(finalDist1) + "  " + str(finalDist2) + "  " + str(finalDist3))
    print(zone)
    url= "https://studev.groept.be/api/a21ib2d04/inputZone/"+zone
    requests.get(url)
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read())

    # print("__________________________________")
    # time.sleep(0.05)
