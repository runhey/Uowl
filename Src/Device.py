# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey

# import cv2
import re
import random
import time

import cv2

from PySide6.QtCore import QThread, QObject
from numpy import frombuffer, uint8, array, random
from pathlib import Path
from subprocess import Popen, PIPE
from win32print import GetDeviceCaps
from win32con import SRCCOPY, DESKTOPHORZRES, DESKTOPVERTRES, WM_LBUTTONUP, WM_LBUTTONDOWN, WM_ACTIVATE, WA_ACTIVE, MK_LBUTTON, WM_NCHITTEST, WM_SETCURSOR, HTCLIENT, WM_MOUSEMOVE
from win32com.client import Dispatch
from win32gui import GetWindowText, FindWindow, FindWindowEx, IsWindow, GetWindowRect, GetWindowDC, DeleteObject, SetForegroundWindow, IsWindowVisible, GetDC, GetParent
from win32process import GetWindowThreadProcessId
from win32ui import CreateDCFromHandle, CreateBitmap
from win32api import GetSystemMetrics, SendMessage, MAKELONG, PostMessage
from PIL import ImageGrab
from pyautogui import position, click, moveTo, dragTo
from math import dist

from robot_mouse_track.mouse_track import MouseTrack
from Src.ConfigFile import ConfigFile
from Src.Log4 import singleton,Log4
from Src.Component.cBezier import BezierTrajectory







class Adb():
    """
    用来执行根abd操作有关的类，不实例化，内部类
    """
    def __init__(self) -> None:
        pass
    @classmethod
    def dealCmd(cls, cmd :str, deviceId :str =None):
        """
        向设备输入一条指令, 返回管道内的东西
        :param cmd:
        :param deviceId:
        :return: 动态返回
        """
        path = Path(__file__).resolve().parent / 'adb.exe'
        if deviceId is None:
            command: str = str(path) + ' ' + cmd
        else:
            command: str = f'{str(path)} -s {deviceId} {cmd}'
        return Popen(command, shell=True, stdout=PIPE).stdout.read()

    @classmethod
    def checkStatus(cls) -> str:
        """
        返回第一个设备的id
        # 检测设备是否在线,如果可以返回一个有设备id，offline and unknown的列表
        如果没有则不返回 为None
        :return:
        """
        result = Adb.dealCmd('devices').decode("utf-8")
        deviceList: list = []
        if result.startswith('List of devices attached'):
            result = result.strip().splitlines()  # 查看连接设备
            deviceSize = len(result)  # 查看连接数量
            if deviceSize > 1:
                for i in range(1, deviceSize):
                    deviceDetail = result[1].split('\t')
                    if deviceDetail[1] == 'device':
                        deviceList.append(deviceDetail[0])
                    elif deviceDetail[1] == 'offline':
                        deviceList.append('offline')
                    elif deviceDetail[1] == 'unknown':
                        deviceList.append('unknown')
            # return deviceList
            if deviceList == []:   #如果都没有设备尝试连接mumu模拟器
                print("mumu 连接中")
                result = Adb.dealCmd('connect 127.0.0.1:7555').decode("utf-8")
                if result.find('connect to 127.0.0.1:7555') == -1:
                    return '127.0.0.1:7555'
            for device in deviceList:
                if device != 'offline' and device != 'unknown':
                    return device

    @classmethod
    def getScreenSize(cls, deviceId :str) -> list:
        """
        获取设备的屏幕尺寸是第一个参数是比较大width的第二个参数是小的
        因为手机和平板的宽高定义不一样
        :param deviceId:
        :return:
        """
        result = str(Adb.dealCmd(' shell wm size', deviceId))
        size = re.findall(r'\d+x\d+', result)
        if size[0].split("x")[0] > size[0].split("x")[1]:
            return size[0].split("x")
        else :
            return [size[0].split("x")[1], size[0].split("x")[0]]

    @classmethod
    def click(cls, deviceId :str, pos :list)-> None:
        """
        点击 Pos第一个是x 第二个是y
        :param deviceId:
        :param pos:
        :return:
        """
        command = rf' shell input tap {pos[0]} {pos[1]}'
        Adb.dealCmd(command, deviceId)

    @classmethod
    def getScreen(cls, deviceId :str):
        """
        返回一个灰色的 图片对象
        :param deviceId:
        :return:
        """
        command = rf' shell screencap -p'
        commend = Adb.dealCmd(command, deviceId)
        if deviceId.startswith('127.0.0.1:7555'):
            scrBytes = commend.replace(b'\r\r\n', b'\n')  # 这个mumu模拟器和其他的不一样
        else:
            scrBytes = commend.replace(b'\r\n', b'\n')  # 传输
        scrImg = cv2.imdecode(frombuffer(scrBytes, uint8), cv2.IMREAD_COLOR)
        scrImg = cv2.cvtColor(scrImg, cv2.COLOR_BGRA2GRAY)
        return scrImg

    @classmethod
    def swipe(cls, deviceId :str, startPos :list, endPos :list) -> None:
        """

        :param deviceId:
        :param startPos:
        :param endPos:
        :return:
        """
        command = rf' shell input swipe {startPos[0]} {startPos[1]} {endPos[0]} {endPos[1]}'
        Adb.dealCmd(command, deviceId)

class Handle():
    """
    用于操作模拟器 窗口的类 依旧不实例化
    """
    def __init__(self):
        pass

    @classmethod
    def getHandleNum(cls, handleTitle :str) -> int:
        """
        返回句柄号 如果没有找到就是返回零
        :param handleTitle:
        :return:
        """
        handleNumParent = FindWindow(None, handleTitle)
        handleNum :int = 0
        handleNum = FindWindowEx(handleNumParent, None, None, "TheRender")  # 先找雷电的
        if handleNum == 0:
            handleNum = FindWindowEx(handleNumParent, None, None, "NemuPlayer")  # 后面找mumu
        return handleNum

    @classmethod
    def getParentHandleNum(cls, handleNum :int) -> int:
        """
        从子窗口获取父窗口的句柄
        :param handleNum:
        :return:
        """
        return GetParent(handleNum)

    @classmethod
    def getHandTitle(cls, handleNum :int) -> str:
        """
        通过句柄号返回窗口的标题，如果传入句柄号不合法则返回None
        :param handleNum:
        :return:
        """
        return None if handleNum is None or handleNum == 0 or handleNum == '' else GetWindowText(handleNum)

    @classmethod
    def getHandPid(cls, handleNum :int) -> int:
        """
        通过句柄号获取句柄进程id，如果句柄号非法则返回0
        :param handleNum:
        :return:
        """
        return 0 if handleNum is None or handleNum == 0 or handleNum == '' else GetWindowThreadProcessId(handleNum)[1]

    @classmethod
    def checkStatus(cls, handleNum :int) -> bool:
        """
        如果窗口还存在返回True否则False
        :param handleNum:
        :return:
        """
        return True if IsWindow(handleNum)==1 else False

    @classmethod
    def getSize(cls, handleNum :int) -> list:
        """
        返回一个由宽带高度组成的列表 第一项是宽带
        :param handleNum:
        :return:
        """
        winRect = GetWindowRect(handleNum)
        width :int = winRect[2] - winRect[0]  # 右x-左x
        height :int = winRect[3] - winRect[1]  # 下y - 上y 计算高度
        return [width, height]

    @classmethod
    def getWindowScaleRate(cls) -> float:
        """
        获取window系统的分辨率
        这个函数在我的电脑上输出结果和我系统设定的不一致，但是使用这个值对
        模拟器截屏缩放是没有问题的，估计是新版本window改了接口吧
        :return:
        """
        hDC = GetDC(0)
        # 物理上（真实的）的 横纵向分辨率
        wReal = GetDeviceCaps(hDC, DESKTOPHORZRES)
        hReal = GetDeviceCaps(hDC, DESKTOPVERTRES)
        # 缩放后的 分辨率
        wAfter = GetSystemMetrics(0)
        hAfter = GetSystemMetrics(1)
        # print(wReal, wAfter)
        return round(wReal / wAfter, 2)

    @classmethod
    def getScreen(cls, handleNum :int, winSize :list, scaleRate :float =1.0):
        """
        windows api 截图
        可以后台，可被遮挡，但是不能点击最小化  图片不包括标题栏边框等1280x720
        :param handleNum:
        :param winSize: 第一个参数是宽度width
        :param scaleRate:
        :return:
        """
        widthScreen = int(winSize[0] / scaleRate)
        heightScreen = int(winSize[1] / scaleRate)
        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDc = GetWindowDC(handleNum)
        # 创建设备描述表
        mfcDc = CreateDCFromHandle(hwndDc)
        # 创建内存设备描述表
        saveDc = mfcDc.CreateCompatibleDC()
        # 创建位图对象准备保存图片
        saveBitMap = CreateBitmap()
        # 为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(mfcDc, widthScreen, heightScreen)
        # 将截图保存到saveBitMap中
        saveDc.SelectObject(saveBitMap)
        # 保存bitmap到内存设备描述表
        saveDc.BitBlt((0, 0), (widthScreen, heightScreen), mfcDc, (0, 0), SRCCOPY)

        # 保存图像
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        imgSrceen = frombuffer(signedIntsArray, dtype='uint8')
        imgSrceen.shape = (heightScreen, widthScreen, 4)
        imgSrceen = cv2.cvtColor(imgSrceen, cv2.COLOR_BGRA2GRAY)
        imgSrceen = cv2.resize(imgSrceen, (winSize[0], winSize[1]))

        # 测试显示截图图片
        # cv2.namedWindow('imgSrceen')  # 命名窗口
        # cv2.imshow("imgSrceen", imgSrceen)  # 显示
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 内存释放
        DeleteObject(saveBitMap.GetHandle())
        saveDc.DeleteDC()
        mfcDc.DeleteDC()
        return imgSrceen

    @classmethod
    def getScreenPIL(cls, handleNum :int):
        """
        PIL截图方法，不能被遮挡，不包括边框标题栏1280x720
        :param handleNum:
        :return:
        """
        shell = Dispatch("WScript.Shell")
        shell.SendKeys('%')
        SetForegroundWindow(handleNum)  # 窗口置顶
        QThread.sleep(0.1)  # 置顶后等0.2秒再截图
        x1, y1, x2, y2 = GetWindowRect(handleNum)  # 获取窗口坐标
        grabImage = ImageGrab.grab((x1, y1, x2, y2))  # 用PIL方法截图
        imgScreen = array(grabImage)  # 转换为cv2的矩阵格式
        imgScreen = cv2.cvtColor(imgScreen, cv2.COLOR_BGRA2GRAY)

        # cv2.namedWindow('imgSrceen')  # 命名窗口
        # cv2.imshow("imgSrceen", imgScreen)  # 显示
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return imgScreen

    @classmethod
    def click(cls, handleNum :int, pos :list) -> list:
        """

        :param handleNum:
        :param pos: 图片上！！！是图片上！！！的相对坐标
        :return: 以用户桌面为坐标系的点击坐标
        """
        x1, y1, x2, y2 = GetWindowRect(handleNum)
        clickPos = MAKELONG(pos[0], pos[1])
        # SendMessage(handleNum, WM_ACTIVATE, WA_ACTIVE, 0)  # 激活窗口
        SendMessage(handleNum, WM_LBUTTONDOWN, 0, clickPos)  # 模拟鼠标按下
        QThread.sleep((random.randint(100, 200)) / 1000.0)  # 点击弹起改为随机,时间100ms-200ms
        SendMessage(handleNum, WM_LBUTTONUP, 0, clickPos)  # 模拟鼠标弹起
        return [x1+pos[0], y1+pos[1]]

    @classmethod
    def clickPIL(cls, handleNum :int, pos :list) -> list:
        """

        :param handleNum:
        :param pos:
        :return:
        """
        x1, y1, x2, y2 = GetWindowRect(handleNum)
        xClick = x1 +pos[0]
        yClick = y1 +pos[1]
        # 把窗口置顶，并进行点击
        shell = Dispatch("WScript.Shell")
        shell.SendKeys('%')
        SetForegroundWindow(handleNum)
        QThread.sleep(0.2)  # 置顶后等0.2秒再点击
        presentPos = position()  # 记录当前的坐标
        moveTo(xClick, yClick)
        click(xClick, yClick)
        moveTo(presentPos[0], presentPos[1])
        return [x1 + pos[0], y1 + pos[1]]

    @classmethod
    def clickMumu(cls, pHandleNum :int, cHandleNum :int, pos :list) -> list:
        """
        对猪场风控的反制，小小猪场难不倒我
        mumu模拟器界面也是qt写的底层同样也是wind API
        :param pHandleNum: 父窗口的句柄 一般是 阴阳师 - MuMu模拟器
        :param cHandleNum:  NemuPlayer
        :param pos:
        :return:
        """
        x1, y1, x2, y2 = GetWindowRect(cHandleNum)
        SendMessage(pHandleNum, WM_LBUTTONDOWN, 0, MAKELONG(pos[0], pos[1]+57))  # 模拟鼠标按下 先是父窗口 上面的框高度是57
        QThread.sleep((random.randint(100, 200)) / 1000.0)  # 点击弹起改为随机,时间100ms-200ms
        SendMessage(cHandleNum, WM_LBUTTONUP, 0, MAKELONG(pos[0], pos[1]))  # 模拟鼠标弹起 后是子窗口
        return [x1 + pos[0], y1 + pos[1]]

    @classmethod
    def swipe(cls, handleNum :int, startPos :list, endPos :list) -> None:
        """
        后台滑动
        :param handleNum:
        :param startPos:
        :param endPos:
        :return:
        """
        interval: int = 8  # 每次移动的间隔时间
        numberList :int = int(dist(startPos, endPos)/(1.5*interval))  # 表示每秒移动1.5个像素点， 总的时间除以每个点10ms就得到总的点的个数
        trace :list = BezierTrajectory.trackArray(start=startPos, end=endPos, numberList=numberList, le=3,
                     deviation=30, bias=0.5, type=3, cbb=0, yhh=10)

        PostMessage(handleNum, WM_ACTIVATE, WA_ACTIVE, 0)  # 激活窗口
        # 先移动到第一个点
        tmpPos = MAKELONG(trace[0][0], trace[0][1])
        SendMessage(handleNum, WM_NCHITTEST, 0, tmpPos)
        SendMessage(handleNum, WM_SETCURSOR, handleNum, MAKELONG(HTCLIENT, WM_LBUTTONDOWN))
        PostMessage(handleNum, WM_LBUTTONDOWN, MK_LBUTTON, tmpPos)
        # 一点一点移动鼠标
        for pos in trace:
            tmpPos = MAKELONG(pos[0], pos[1])
            PostMessage(handleNum, WM_MOUSEMOVE, MK_LBUTTON, tmpPos)
            Log4().csv(pos[0], pos[1], time.time())
            time.sleep((interval+random.randint(-2, 2))/1000.0)
        # 最后释放鼠标
        tmpPos = MAKELONG(trace[-1][0], trace[-1][1])
        PostMessage(handleNum, WM_LBUTTONUP, 0, tmpPos)


    @classmethod
    def swipePIL(cls, handleNum :int, startPos :list, endPos :list) -> None:
        """
        鼠标拖动 前台滑动
        :param handleNum:
        :param startPos:
        :param endPos:
        :param time: 执行时间  好了现在没有用了
        :return:
        """
        x1, y1, x2, y2 = GetWindowRect(handleNum)
        # 把窗口置顶，并进行点击
        shell = Dispatch("WScript.Shell")
        shell.SendKeys('%')
        SetForegroundWindow(handleNum)
        QThread.sleep(0.2)  # 置顶后等0.2秒再滑动
        moveTo(x1+startPos[0], y1+startPos[1])
        dragTo(x1+endPos[0], y1+endPos[1], button='left')

class Device(QObject):
    """
    虽然很大程度上可以把Device当成android mumu leidian 的基类，但是这个三种之间有很大不一样
    考虑到设计需求这个东西是全局唯一的所以设计成单个依赖关系
    非常利于后面调用
    """
    def __init__(self, baseSetting :dict , android :dict , munu :dict, leidian :dict) -> None:
        super(Device, self).__init__()
        self.baseSetting :dict = baseSetting
        self.android :dict = android
        self.mumu :dict = munu
        self.leidian :dict = leidian

    def connect(self) -> None:
        """
        检查 对设备的连接状态,如果OK返回对应的deviceId或者handleNum
        :return:
        """
        match self.baseSetting["deviceType"]:
            case "安卓设备" :
                if self.android["connectType"] == "adb":
                    self.android["deviceId"] = Adb.checkStatus()
                    Log4().log("info",f'连接安卓设备, deviceId:{self.android["deviceId"]}')
                    if not self.android["deviceId"]:
                        Log4().log("info", "无法通过adb连接安卓设备, 请确保安卓设备打开开发者选项并正常运行")
                    return self.android["deviceId"]
            case "mumu模拟器" :
                if self.mumu["connectType"] == "adb":
                    self.mumu["deviceId"] = Adb.checkStatus()
                    Log4().log("info", f'连接mumu模拟器, deviceId:{self.mumu["deviceId"]}')
                    if not self.mumu["deviceId"]:
                        Log4().log("info", "无法通过adb连接mumu模拟器, 请确保模拟器正常运行")
                    return self.android["deviceId"]
                elif self.mumu["connectType"] == "window前台":
                    self.mumu["handleNum"] = Handle.getHandleNum(self.mumu["handleTitle"])
                    Log4().log("info", f'连接mumu模拟器, handleTitle:{self.mumu["handleTitle"]}, handleNum:{self.mumu["handleNum"]}')
                    if self.mumu["handleNum"] == 0:
                        Log4().log("info", "无法连接mumu, 请确保模拟器正常运行")
                    return self.mumu["handleNum"] if Handle.checkStatus(self.mumu["handleNum"]) else None
                elif self.mumu["connectType"] == "window后台":
                    self.mumu["handleNum"] = Handle.getHandleNum(self.mumu["handleTitle"])
                    self.mumu["pHandleNum"] = Handle.getParentHandleNum(self.mumu["handleNum"])
                    Log4().log("info", f'连接mumu模拟器, handleTitle:{self.mumu["handleTitle"]}, handleNum:{self.mumu["handleNum"]}')
                    if self.mumu["handleNum"] == 0:
                        Log4().log("info", "无法连接mumu模拟器, 请确保模拟器正常运行")
                    return self.mumu["handleNum"] if Handle.checkStatus(self.mumu["handleNum"]) else None
            case "雷电模拟器" :
                if self.leidian["connectType"] == "adb":
                    self.leidian["deviceId"] = Adb.checkStatus()
                    Log4().log("info", f'连接雷电模拟器, deviceId:{self.leidian["deviceId"]}')
                    if not self.leidian["deviceId"]:
                        Log4().log("info", "无法通过adb连接雷电模拟器, 请确保模拟器正常运行")
                    return self.android["deviceId"]
                elif self.leidian["connectType"] == "window前台":
                    self.leidian["handleNum"] = Handle.getHandleNum(self.leidian["handleTitle"])
                    Log4().log("info", f'连接雷电模拟器, handleTitle:{self.leidian["handleTitle"]}, handleNum:{self.leidian["handleNum"]}')
                    if self.leidian["handleNum"] == 0:
                        Log4().log("info", "无法连接雷电模拟器, 请确保模拟器正常运行")
                    return self.leidian["handleNum"] if Handle.checkStatus(self.leidian["handleNum"]) else None
                elif self.leidian["connectType"] == "window后台":
                    self.leidian["handleNum"] = Handle.getHandleNum(self.leidian["handleTitle"])
                    Log4().log("info", f'连接雷电模拟器, handleTitle:{self.leidian["handleTitle"]}, handleNum:{self.leidian["handleNum"]}')
                    if self.leidian["handleNum"] == 0:
                        Log4().log("info", "无法连接雷电模拟器, 请确保模拟器正常运行")
                    return self.leidian["handleNum"] if Handle.checkStatus(self.leidian["handleNum"]) else None

    def connectDevice(self) -> None:
        """
        现在没啥用的
        :return:
        """
        pass

    def updateSettingToFile(self) -> None:
        """
        需要使用这个函数之前调用connect函数得到正确的deviceId或者handleNum
        然后更新设置数据写入json
        :return:
        """
        self.baseSetting["defaultWidth"] = 1280
        self.baseSetting["defaultHeight"] = 720
        self.baseSetting["windowScaleRate"] = Handle.getWindowScaleRate()
        match self.baseSetting["deviceType"]:
            case "安卓设备" :
                self.android["androidWidth"] = Adb.getScreenSize(self.android["deviceId"])[0]
                self.android["androidHeight"] = Adb.getScreenSize(self.android["deviceId"])[1]
                Log4().log("info", f'设备尺寸是:{self.android["androidWidth"]}x{self.android["androidHeight"]}')
            case "mumu模拟器":
                if self.mumu["connectType"] == "adb":
                    self.mumu["mumuWidth"] = Adb.getScreenSize(self.mumu["deviceId"])[1]
                    self.mumu["mumuHeight"] = Adb.getScreenSize(self.mumu["deviceId"])[0]
                    Log4().log("info", f'设备尺寸是:{self.mumu["mumuWidth"]}x{self.mumu["mumuHeight"]}')
                else:
                    self.mumu["mumuWidth"] = Handle.getSize(self.mumu["handleNum"])[0]
                    self.mumu["mumuHeight"] = Handle.getSize(self.mumu["handleNum"])[1]
                    Log4().log("info", f'设备尺寸是:{self.mumu["mumuWidth"]}x{self.mumu["mumuHeight"]}')
            case "雷电模拟器":
                if self.leidian["connectType"] == "adb":
                    self.leidian["leidianWidth"] = Adb.getScreenSize(self.leidian["deviceId"])[1]
                    self.leidian["leidianHeight"] = Adb.getScreenSize(self.leidian["deviceId"])[0]
                    Log4().log("info", f'设备尺寸是:{self.leidian["leidianWidth"]}x{self.leidian["leidianHeight"]}')
                else:
                    self.leidian["leidianWidth"] = Handle.getSize(self.leidian["handleNum"])[0]
                    self.leidian["leidianHeight"] = Handle.getSize(self.leidian["handleNum"])[1]
                    Log4().log("info", f'设备尺寸是:{self.leidian["leidianWidth"]}x{self.leidian["leidianHeight"]}')
        ConfigFile().writeSettingFromDevice(self.baseSetting, self.android, self.mumu, self.leidian)

    def getScreen(self):
        """
        这个操作必须保证连接无误
        :return:
        """
        match self.baseSetting["deviceType"]:
            case "安卓设备" :
                if self.android["getScreenWay"] == "adb":
                    return Adb.getScreen(self.android["deviceId"])
                else:
                    pass
            case "mumu模拟器":
                if self.mumu["getScreenWay"] == "adb":
                    return Adb.getScreen(self.mumu["deviceId"])
                elif self.mumu["getScreenWay"] == "window前台":
                    return Handle.getScreenPIL(self.mumu["handleNum"])
                elif self.mumu["getScreenWay"] == "window后台":
                    return Handle.getScreen(self.mumu["handleNum"], [self.mumu["mumuWidth"],self.mumu["mumuHeight"]])
            case "雷电模拟器":
                if self.leidian["getScreenWay"] == "adb":
                    return Adb.getScreen(self.leidian["deviceId"])
                elif self.leidian["getScreenWay"] == "window前台":
                    return Handle.getScreenPIL(self.leidian["handleNum"])
                elif self.leidian["getScreenWay"] == "window后台":
                    return Handle.getScreen(self.leidian["handleNum"], [self.leidian["leidianWidth"],self.leidian["leidianHeight"]])
            case default:
                return None

    def click(self, pos :list ) -> None:
        """

        :param pos:
        :return:
        """
        Log4().csv(pos[0], pos[1], time.time())
        match self.baseSetting["deviceType"]:
            case "安卓设备":
                if self.android["controlWay"] == "adb":
                    Adb.click(self.android["deviceId"], pos)
                else:
                    pass
            case "mumu模拟器":
                if self.mumu["controlWay"] == "adb":
                    Adb.click(self.mumu["deviceId"], pos)
                elif self.mumu["controlWay"] == "window前台":
                    Handle.clickPIL(self.mumu["handleNum"], pos)
                elif self.mumu["controlWay"] == "window后台":
                    Handle.clickMumu(self.mumu["pHandleNum"], self.mumu["handleNum"], pos)
            case "雷电模拟器":
                if self.leidian["controlWay"] == "adb":
                    Adb.click(self.leidian["deviceId"], pos)
                elif self.leidian["controlWay"] == "window前台":
                    Handle.clickPIL(self.leidian["handleNum"], pos)
                elif self.leidian["controlWay"] == "window后台":
                    Handle.click(self.leidian["handleNum"], pos)
            case default:
                return None

    def saveScreen(self, img, name: str, path = None) -> None:
        if path is not None:
            cv2.imwrite( path / name + '.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # 保存截图 质量（0-100）
        else:
            path = str(Path.cwd().resolve() / name) + '.jpg' # 绝对路径
            cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # 保存截图 质量（0-100）

    def swipe(self, startPos :list, endPos :list) -> None:
        """

        :param startPos:
        :param endPos:
        :return:
        """
        match self.baseSetting["deviceType"]:
            case "安卓设备":
                if self.android["controlWay"] == "adb":
                    Adb.swipe(self.android["deviceId"], startPos, endPos)
                else:
                    pass
            case "mumu模拟器":
                if self.mumu["controlWay"] == "adb":
                    Adb.swipe(self.mumu["deviceId"], startPos, endPos)
                elif self.mumu["controlWay"] == "window前台":
                    Handle.swipePIL(self.mumu["handleNum"], startPos, endPos)
                elif self.mumu["controlWay"] == "window后台":
                    Handle.swipe(self.mumu["handleNum"], startPos, endPos)
            case "雷电模拟器":
                if self.leidian["controlWay"] == "adb":
                    Adb.swipe(self.leidian["deviceId"], startPos, endPos)
                elif self.leidian["controlWay"] == "window前台":
                    Handle.swipePIL(self.leidian["handleNum"], startPos, endPos)
                elif self.leidian["controlWay"] == "window后台":
                    Handle.swipe(self.leidian["handleNum"], startPos, endPos)
            case default:
                return None


# h = Handle()
# print(h.getHandleNum("浏览器 - MuMu模拟器"))

# trace = [[500,0], [500,50], [500,100], [500,150], [500,200], [500,250], [500,300], [500,350], [500,400], [500, 450]]
# h = Handle()
# handleNum = h.getHandleNum("MuMu模拟器")
# mouseTrack = MouseTrack(h.swipe(handleNum, [201,440], [800, 440]))
mouseTrack.show_track(x_min=0, y_min=0, x_max=1280, y_max=720)


# adb = Adb()
# deviceId = adb.checkStatus()
# adb.swipe(deviceId, [400, 1], [500, 450])

# h = Handle()
# handleNumParent = FindWindow(None, "MuMu模拟器")
# handleNum = FindWindowEx(handleNumParent, None, None, "NemuPlayer")  # 后面找mumu
# print(f"父窗口大小:{h.getSize(handleNumParent)},  子窗口大小:{h.getSize(handleNum)}")
# SendMessage(handleNumParent, WM_LBUTTONDOWN, 0, MAKELONG(1076, 207))  # 模拟鼠标按下
# QThread.sleep((random.randint(100, 200)) / 1000.0)  # 点击弹起改为随机,时间100ms-200ms
# SendMessage(handleNum, WM_LBUTTONUP, 0, MAKELONG(1076, 150))  # 模拟鼠标弹起
