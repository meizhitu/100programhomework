__author__ = 'rui'
#coding=utf-8

import time
import os
import threading
import sys
import traceback
import pygame

codeDir = os.path.dirname(__file__)


class Alarm(threading.Thread):
    def __init__(self, hours, minutes):
        super(Alarm, self).__init__()
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.keep_running = True

    def run(self):
        try:
            while self.keep_running:
                now = time.localtime()
                if (now.tm_hour == self.hours and now.tm_min >= self.minutes):
                    print("时间到")
                    playMusic()
                    return
            time.sleep(60)
        except:
            printTraceback()
            return

    def just_die(self):
        self.keep_running = False


def getAbsolutePath(relatePath):
    return os.path.join(codeDir, relatePath)


def playMusic():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode([640, 480])
    pygame.time.delay(1000)
    pygame.mixer.music.load(r"res/bk.ogg")
    pygame.mixer.music.play()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return

def printTraceback():
    try:
        print traceback.format_exc()
    except:
        return


def doAlarm():
    hh = input("小时：")
    mm = input("分钟：")
    print("闹钟将在{0:02}:{1:02}响".format(hh, mm))
    alarm = Alarm(hh, mm)
    alarm.start()
    try:
        while True:
            text = str(raw_input())
            if text == "stop":
                alarm.just_die()
                break
    except:
        print("出了点问题")
        alarm.just_die()


if __name__ == "__main__":
    doAlarm()