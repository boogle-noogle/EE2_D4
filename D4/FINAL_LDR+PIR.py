import RPi.GPIO as GPIO
import time
# from gpiozero import LED
import urllib.request
import urllib, json
import re
import requests

PIR1, PIR2, LDR, LED1, LED2 = 26, 19, 13, 17, 12

# led = LED(26)



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIR1, GPIO.IN)  # PIR1
GPIO.setup(PIR2, GPIO.IN)  # PIR2
GPIO.setup(LDR, GPIO.IN)  # 0 if covered, 1 if not
GPIO.setup(LED1, GPIO.OUT)  # LED1
GPIO.setup(LED2, GPIO.OUT)  # LED2
# GPIO.setup(PIR1, GPIO.IN, GPIO.PUD_DOWN)


# GPIO.output(LED1, GPIO.HIGH)

counter1 = 0
counter2 = 0
room1Full = False
room2Full = False

room1Full = False
room2Full = False


GPIO.setup(LED2, GPIO.OUT)
pwm = GPIO.PWM(LED2, 100)
pwm.start(0)

while True:
    url = "https://studev.groept.be/api/a21ib2d04/getLightStatus"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    numberList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(numberList)

    url = "https://studev.groept.be/api/a21ib2d04/getLightControl"
    # response = urllib.urlopen(url)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

# requests.url
    onList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(onList)
    print(str(GPIO.input(PIR1))+"                 " + str(GPIO.input(PIR2)))

    if onList[0] == 1:
        if GPIO.input(PIR1):
            time.sleep(5)
            counter1 += 1
        if (GPIO.input(PIR2) and counter1 %2!=0):
            time.sleep(5)
            counter2 += 1

        if counter1 % 2 != 0 and counter1 != 0 and counter2 % 2 ==0 and GPIO.input(LDR) !=0:
            room1Full = True
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.LOW)
        else:
            room1Full = False
            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.HIGH)

        if counter2 % 2 != 0 and counter2 != 0 and counter1 % 2 != 0 and GPIO.input(LDR) !=0:
            room2Full = True
            GPIO.output(LED2, GPIO.HIGH)
            pwm.ChangeDutyCycle(numberList[0])

        else:
            room2Full = False
            room1Full = True
            GPIO.output(LED2, GPIO.LOW)
            pwm.ChangeDutyCycle(0.0000000001)

        print("counter 1:" + str(counter1) + "       " + "counter 2:" + str(counter2) + "     room1full? :     " + str(
            room1Full))
        print("__________________________")
    if onList[0] == 0:
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED1, GPIO.LOW)
        pwm.ChangeDutyCycle(0.00000000001)
        print('OFF')
