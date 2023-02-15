# This Python file uses the following encoding: utf-8
import os
import time
from pathlib import Path
import sys

startTime = time.time()
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt, QThread

from Src.ConfigFile import ConfigFile
from Src.TaskScheduler import TaskScheduler
from Src.Bridge import Bridge
from Src.Log4 import Log4
print("启动时间: " + str(time.time() - startTime))

if __name__ == "__main__":
    # 适配高分辨率
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round)
    # 声明
    app = QGuiApplication(sys.argv)
    # 设置Logo
    QGuiApplication.setWindowIcon(QIcon(os.fspath(Path(__file__).resolve().parent / "GuiImage/logo/logo-64.ico")))
    # 设置软件名字
    QGuiApplication.setApplicationName("Uowl")
    #
    QGuiApplication.setOrganizationName("Uowl")

    # Logx系统
    log4 = Log4()
    # 初始化配置文件
    configFile = ConfigFile()
    # 连接python和qml的信号桥，两个语言通信就这两种机制一个是以json文件另一个就是这个信号槽机制
    bridge = Bridge()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("log4", log4)
    engine.rootContext().setContextProperty("configFile", configFile)
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.load(os.fspath(Path(__file__).resolve().parent / "GuiQML/main.qml"))

    # 后端线程
    taskSch = TaskScheduler()
    taskSch.start()

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
