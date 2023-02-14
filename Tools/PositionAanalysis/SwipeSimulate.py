# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey

import sys
import time
import os

from pathlib import Path
srcPath = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(srcPath))

from Src.Device import Device
from Src.Task.Action import SwipeAction
from Src.ConfigFile import ConfigFile
from Src.Log4 import Log4

def swipeTest() -> None:
    log4 = Log4()
    log4.slotStartLog("swipedtest")
    device = Device(ConfigFile.getSettingDict("baseSetting"),
                                 ConfigFile.getSettingDict("android"),
                                 ConfigFile.getSettingDict("mumu"),
                                 ConfigFile.getSettingDict("leidian"))
    device.connect()
    device.updateSettingToFile()
    swipe = SwipeAction([1280, 720], {"actionName": "test", "angle": 0, "distance": 0.5, "random": 50}, device)
    for i in range(10):
        print(swipe.deal({"centerPos": [640, 360]}))
        time.sleep(0.8)
    log4.slotFinishLog()



if __name__ == '__main__':
    """
    打开模拟器 ，运行会在Log生成csv文件，使用该文件进行数据分析
    """
    swipeTest()