from RPi import GPIO
import re
import urllib.request
import urllib,json
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)

#Setting up notes
tone1 = GPIO.PWM(24, 100)

#Note frequencies, starting with a C
#speaker works good from 32hz to about 500hz, so the first four octaves here
c = [32, 65, 131, 262, 523]
db= [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb= [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb= [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab= [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb= [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

#notes of two scales, feel free to add more
cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]

def playScale(scale, pause):
    for i in range(0, 5):
        for note in scale:
            tone1.ChangeFrequency(note[i] * numberList[0]/100 + 0.0001)
            time.sleep(pause)
    tone1.stop()

def playSong(songnotes, songbeats, tempo):
    tone1.start(50)
    tone1.ChangeDutyCycle(50)
    for i in range(0, len(songnotes)):
        tone1.ChangeFrequency(songnotes[i] * numberList[0]/100 + 0.0001)
        time.sleep(songbeats[i]*tempo)
    tone1.ChangeDutyCycle(0)


while True:
    # getting data from the database
    url = "https://studev.groept.be/api/a21ib2d04/getSoundControl"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    onList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(onList)

    url = "https://studev.groept.be/api/a21ib2d04/getNrofpeople"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    peopleList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(peopleList)

    url = "https://studev.groept.be/api/a21ib2d04/getZone"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    zone = str(data)
    print(zone)

    url = "https://studev.groept.be/api/a21ib2d04/getSoundStatus"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    numberList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(numberList)

    url = "https://studev.groept.be/api/a21ib2d04/getSongSatus"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    songList = [int(num) for num in re.findall(r"\d+", str(data))]
    print(songList)

    #songs depending on ON/OFF
    if onList[0] == 1:
        if peopleList[0] == 1:
            #song depending on zone
            if zone == "[{'zone': '9'}]" or zone == "[{'zone': '6'}]" or zone == "[{'zone': '3'}]":
                if songList[0] == 1:
                    starwars_notes = [c[3], g[3], f[3], e[3], d[3], c[4], g[3], f[3], e[3], d[3], c[4], g[3],
                                      f[3], e[3], f[3], d[3]]
                    starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]
                    playSong(starwars_notes, starwars_beats, 0.2)
                if songList[0] == 2:
                    londonbridges_notes = [g[3], a[3], g[3], f[3], e[3], f[3], g[3], d[3], e[3], f[3],
                                           e[3], f[3], g[3], g[3], a[3], g[3], f[3], e[3], f[3], g[3],
                                           d[3], g[3], e[3], c[3]]
                    londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1,
                                           2, 2, 2, 1,1]
                    playSong(londonbridges_notes, londonbridges_beats, 0.3)
                if songList[0] == 3:
                    twinkletwinkle_notes = [c[4],c[4],g[4],g[4],a[4],a[4],g[4],
                                            f[4],f[4],e[4],e[4],d[4],d[4],c[4],
                                            g[4],g[4],f[4],f[4],e[4],e[4],d[4],
                                            g[4],g[4],f[4],f[4],e[4],e[4],d[4],
                                            c[4],c[4],g[4],g[4],a[4],a[4],g[4],
                                            f[4],f[4],e[4],e[4],d[4],d[4],c[4]]
                    twinkletwinkle_beats = [    4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6]
                    playSong(twinkletwinkle_notes,twinkletwinkle_beats, 0.1)
                if songList[0] == 4:
                    manaderna_notes = [e[4],e[4],f[4],g[4],g[4],f[4],e[4],d[4],c[4],c[4],d[4],e[4],d[4],c[4],c[4],
                                       d[4],d[4],e[4],c[4],d[4],e[4],f[4],e[4],c[4],d[4],e[4],f[4],e[4],d[4],c[4],d[4],g[3]]

                    manaderna_beats = [    2,2,2,2,
                                           2,2,2,2,
                                           2,2,2,2,
                                           2,4,2,
                                           2,2,2,2,
                                           2,4,4,2,2,
                                           2,4,4,2,2,
                                           2,2,1]
                    playSong(manaderna_notes, manaderna_beats, 0.2)


            elif zone == "[{'zone': '2'}]" or zone == "[{'zone': '5'}]" or zone == "[{'zone': '8'}]":
                if songList[0] == 1:
                    starwars_notes = [c[2], g[2], f[2], e[2], d[2], c[3], g[2], f[2], e[2], d[2], c[3], g[2],
                                      f[2], e[2], f[2], d[2]]
                    starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]
                    playSong(starwars_notes, starwars_beats, 0.2)
                if songList[0] == 2:

                    londonbridges_notes = [g[2], a[2], g[2], f[2], e[2], f[2], g[2], d[2], e[2], f[2],
                                           e[2], f[2], g[2], g[2], a[2], g[2], f[2], e[2], f[2], g[2],
                                           d[2], g[2], e[2], c[2]]
                    londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1,
                                           2, 2, 2, 1,1]
                    playSong(londonbridges_notes, londonbridges_beats, 0.3)
                if songList[0] == 3:
                    twinkletwinkle_notes = [c[3],c[3],g[3],g[3],a[3],a[3],g[3],
                                            f[3],f[3],e[3],e[3],d[3],d[3],c[3],
                                            g[3],g[3],f[3],f[3],e[3],e[3],d[3],
                                            g[3],g[3],f[3],f[3],e[3],e[3],d[3],
                                            c[3],c[3],g[3],g[3],a[3],a[3],g[3],
                                            f[3],f[3],e[3],e[3],d[3],d[3],c[3]]
                    twinkletwinkle_beats = [    4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,]
                    playSong(twinkletwinkle_notes,twinkletwinkle_beats, 0.1)
                if songList[0] == 4:
                    manaderna_notes = [e[3],e[3],f[3],g[3],g[3],f[3],e[3],d[3],c[3],c[3],d[3],e[3],d[3],c[3],c[3],
                                       d[3],d[3],e[3],c[3],d[3],e[3],f[3],e[3],c[3],d[3],e[3],f[3],e[3],d[3],c[3],d[3],g[2]]

                    manaderna_beats = [    2,2,2,2,
                                           2,2,2,2,
                                           2,2,2,2,
                                           2,4,2,
                                           2,2,2,2,
                                           2,4,4,2,2,
                                           2,4,4,2,2,
                                           2,2,1]
                    playSong(manaderna_notes, manaderna_beats, 0.2)

            elif zone == "[{'zone': '1'}]" or zone == "[{'zone': '4'}]" or zone == "[{'zone': '7'}]":
                if songList[0] == 1:
                    starwars_notes = [c[1], g[1], f[1], e[1], d[1], c[2], g[1], f[1], e[1], d[1], c[2], g[1],
                                      f[1], e[1], f[1], d[1]]
                    starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]
                    playSong(starwars_notes, starwars_beats, 0.2)
                if songList[0] == 2:
                    londonbridges_notes = [g[1], a[1], g[1], f[1], e[1], f[1], g[1], d[1], e[1], f[1],
                                           e[1], f[1], g[1], g[1], a[1], g[1], f[1], e[1], f[1], g[1],
                                           d[1], g[1], e[1], c[1]]
                    londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1,
                                           2, 2, 2, 1,1]
                    playSong(londonbridges_notes, londonbridges_beats, 0.3)
                if songList[0] == 3:
                    twinkletwinkle_notes = [c[2],c[2],g[2],g[2],a[2],a[2],g[2],
                                            f[2],f[2],e[2],e[2],d[2],d[2],c[2],
                                            g[2],g[2],f[2],f[2],e[2],e[2],d[2],
                                            g[2],g[2],f[2],f[2],e[2],e[2],d[2],
                                            c[2],c[2],g[2],g[2],a[2],a[2],g[2],
                                            f[2],f[2],e[2],e[2],d[2],d[2],c[2]]
                    twinkletwinkle_beats = [    4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,
                                                4,4,4,4,4,4,6,]
                    playSong(twinkletwinkle_notes,twinkletwinkle_beats, 0.1)
                if songList[0] == 4:
                    manaderna_notes = [e[2],e[2],f[2],g[2],g[2],f[2],e[2],d[2],c[2],c[2],d[2],e[2],d[2],c[2],c[2],
                                       d[2],d[2],e[2],c[2],d[2],e[2],f[2],e[2],c[2],d[2],e[2],f[2],e[2],d[2],c[2],d[2],g[1]]

                    manaderna_beats = [    2,2,2,2,
                                           2,2,2,2,
                                           2,2,2,2,
                                           2,4,2,
                                           2,2,2,2,
                                           2,4,4,2,2,
                                           2,4,4,2,2,
                                           2,2,1]
                    playSong(manaderna_notes, manaderna_beats, 0.2)
            else:
                none_notes = [a[0]]
                none_beats = [1]
                print("zone not possible")
                playSong(none_notes, none_beats, 0.2)

    if onList[0] == 1:
        if peopleList[0] > 1:
            if songList[0] == 1:
                starwars_notes = [c[3], g[3], f[3], e[3], d[3], c[4], g[3], f[3], e[3], d[3], c[4], g[3],
                                  f[3], e[3], f[3], d[3]]
                starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]
                playSong(starwars_notes, starwars_beats, 0.2)
            if songList[0] == 2:
                londonbridges_notes = [g[3], a[3], g[3], f[3], e[3], f[3], g[3], d[3], e[3], f[3],
                                       e[3], f[3], g[3], g[3], a[3], g[3], f[3], e[3], f[3], g[3],
                                       d[3], g[3], e[3], c[3]]
                londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1,
                                       2, 2, 2, 1,1]
                playSong(londonbridges_notes, londonbridges_beats, 0.3)
            if songList[0] == 3:
                twinkletwinkle_notes = [c[4],c[4],g[4],g[4],a[4],a[4],g[4],
                                        f[4],f[4],e[4],e[4],d[4],d[4],c[4],
                                        g[4],g[4],f[4],f[4],e[4],e[4],d[4],
                                        g[4],g[4],f[4],f[4],e[4],e[4],d[4],
                                        c[4],c[4],g[4],g[4],a[4],a[4],g[4],
                                        f[4],f[4],e[4],e[4],d[4],d[4],c[4]]
                twinkletwinkle_beats = [    4,4,4,4,4,4,6,
                                            4,4,4,4,4,4,6,
                                            4,4,4,4,4,4,6,
                                            4,4,4,4,4,4,6,
                                            4,4,4,4,4,4,6,
                                            4,4,4,4,4,4,6]
                playSong(twinkletwinkle_notes,twinkletwinkle_beats, 0.1)
            if songList[0] == 4:
                manaderna_notes = [e[4],e[4],f[4],g[4],g[4],f[4],e[4],d[4],c[4],c[4],d[4],e[4],d[4],c[4],c[4],
                                   d[4],d[4],e[4],c[4],d[4],e[4],f[4],e[4],c[4],d[4],e[4],f[4],e[4],d[4],c[4],d[4],g[3]]

                manaderna_beats = [    2,2,2,2,
                                       2,2,2,2,
                                       2,2,2,2,
                                       2,4,2,
                                       2,2,2,2,
                                       2,4,4,2,2,
                                       2,4,4,2,2,
                                       2,2,1]
                playSong(manaderna_notes, manaderna_beats, 0.2)

    elif onList[0]==0:
        print("off")