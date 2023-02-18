# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from Src.Task.TaskLoad import loadStateModule, getAllStateModule
for moduleName, moduleFile in getAllStateModule('DailyGroup', "地域鬼王"):
    loadStateModule(moduleName, moduleFile)

from GeneralEnter import GeneralEnter
from GeneralExit import GeneralExit
from GeneralBattle import GeneralBattle
from Src.Device import Device
from Src.ConfigFile import ConfigFile


class UTask:
    def __init__(self, device :Device):
        """

        :param device:  设备注入
        """
        self.device = device
        # 状态的定义
        self.generalEnter = GeneralEnter()
        self.generalExit = GeneralExit()
        self.generalBattle = GeneralBattle()

    def run(self):
        print("这里执行地域鬼王任务")


    def test(self) -> None:
        self.run()



def test():
    device = Device(ConfigFile.getSettingDict("baseSetting"),
                    ConfigFile.getSettingDict("android"),
                    ConfigFile.getSettingDict("mumu"),
                    ConfigFile.getSettingDict("leidian"))
    device.connect()
    device.updateSettingToFile()
    uTask = UTask(device)
    uTask.test()