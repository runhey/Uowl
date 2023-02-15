# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
# 图像事件，变量事件，时间时间，随机事件,
import time

import cv2

from PySide6.QtCore import QObject, Signal
from numpy import float32, int32, uint8, fromfile
from pathlib import Path
# from cnocr import CnOcr
# 这个ocr使得脚本启动时间从1.9变成了6.9足足多了5秒

from Src.Log4 import Log4
from Src.Device import Handle

class ImgEvent(QObject):
    sigEvent = Signal(dict)   # 匹配到后发送事件
    # def __init__(self, scrImg, compressRate: float, matchWay, matchThreshold :float, eventInfo :dict) -> None:
    def __init__(self, taskGroup :str, taskName : str,
                 matchWay :str, compressRate :str ,matchThreshold :str,
                 eventInfo :dict) -> None:
        """
        进行一次图片匹配，是可以写成纯函数的写成类为了符合信号槽机制 。
        前面四个参数都是设备提供的，而后面是任务需要提供的
        """
        super().__init__()
        # 任务扔过来的
        self.taskGroup = taskGroup
        self.taskName = taskName
        self.matchWay = matchWay
        self.compressRate = compressRate
        self.matchThreshold = matchThreshold
        # 下面是从扔过来的信息中提取的
        self.eventInfo = eventInfo
        if eventInfo["eventName"]:
            self.eventName = eventInfo["eventName"]
        if eventInfo["imgName"]:
            self.imgName = eventInfo["imgName"]
            fileName = str(Path(__file__).parent.parent.parent / 'Tasks' / self.taskGroup / self.taskName / self.imgName)
            img = cv2.imdecode( fromfile(fileName, dtype=uint8), -1)
            self.matchImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # self.matchImg = cv2.imread(fileName, cv2.COLOR_BGRA2GRAY)
        # 获取这个imgevent在屏幕中的范围
        Log4().log("info", f'event载入->eventName:{self.eventName},  匹配图片名称:{self.imgName},  '
                           f'截图裁剪width:[{float(self.eventInfo["x0"])} : {float(self.eventInfo["width"])+float(self.eventInfo["x0"])}],  '
                           f'height:[{float(self.eventInfo["y0"])} : {float(self.eventInfo["height"])+float(self.eventInfo["y0"])}]')


    def __compress(self, img, rate :float =0.5) :
        """
        压缩图片默认 0.5
        :param img:
        :param rate:
        :return:
        """
        height, width = img.shape[:2]  # 获取宽高
        # 压缩图片,压缩率compress_val
        size = (int(width * rate), int(height * rate))
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        return img

    def __matchTemplete(self, img, mat, threshold :float =0.9):
        """
        模板匹配，速度快，但唯一的缺点是，改变目标窗体后，必须重新截取模板图片才能正确匹配
        :return: 返回坐标(x,y) 与opencv坐标系对应，以及与坐标相对应的图片在模板图片中的位置 (注意这个图片一般是裁剪后的图片的)
        """
        res = cv2.matchTemplate(img, mat, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)  # 最小匹配度，最大匹配度，最小匹配度的坐标，最大匹配度的坐标
        if maxVal > threshold:
            return [maxLoc[0]+int(mat.shape[1]/2), maxLoc[1]+int(mat.shape[0]/2)]
        else:
            return None
    def __matchSift(self, img, mat):
        sift = cv2.SIFT_create()
        kpImg, desImg = sift.detectAndCompute(img, None)
        kpMat, desMat = sift.detectAndCompute(mat, None)
        minMatchCount = 5  # 匹配到的角点数量大于这个数值即匹配成功
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=100)
        # 根据设置的参数创建特征匹配器 指定匹配的算法和kd树的层数,指定返回的个数
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        # 利用创建好的特征匹配器利用k近邻算法来用模板的特征描述符去匹配图像的特征描述符，k指的是返回前k个最匹配的特征区域
        # 返回的是最匹配的两个特征点的信息，返回的类型是一个列表，列表元素的类型是Dmatch数据类型，具体是什么我也不知道
        matches = flann.knnMatch(desMat, desImg, k=2)
        # 设置好初始匹配值，用来存放特征点
        good = []
        for i, (m, n) in enumerate(matches):
            # 设定阈值, 距离小于对方的距离的0.7倍我们认为是好的匹配点.
            if m.distance < 0.7*n.distance:
                good.append(m)
        # print(len(good))
        if len(good) >= minMatchCount:
            # ret = cv2.drawMatchesKnn(img, kpImg, mat, kpMat, matches, None)
            # cv2.imshow('result', ret)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            srcPts = float32([kpMat[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dstPts = float32([kpImg[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            m, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)
            # 计算中心坐标
            w, h = mat.shape[1], mat.shape[0]
            pts = float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            if m is not None:
                dst = cv2.perspectiveTransform(pts, m)
                arr = int32(dst)
                posArr = arr[0] + (arr[2] - arr[0]) // 2
                pos = (int(posArr[0][0]), int(posArr[0][1]))
                return pos
            else:
                return None
        else:
            return None

    def deal(self, scrImg) -> None:
        """
        按照自身参数进行图片的匹配,找到了发送信号，信号内容为返回的坐标点
        :return: 如果找到图片返回，以原图为坐标系的坐标点，该点以匹配图片为中心；没有找到为None
        """
        img = self.__compress(scrImg, self.compressRate)
        mat = self.__compress(self.matchImg, self.compressRate)
        width, height = img.shape[1], img.shape[0]  #这个是图片压缩后的大小
        cropImg = None
        posTemp = None
        # if float(self.eventInfo["x0"])+float(self.eventInfo["width"])<=1 and float(self.eventInfo["y0"])+float(self.eventInfo["height"])<=1 :
        #     # 裁剪
        #     xStart, xEnd = int(width*float(self.eventInfo["x0"])), int(width*float(self.eventInfo["x0"])+width*float(self.eventInfo["width"]))
        #     yStart, yEnd = int(height*float(self.eventInfo["y0"])), int(height*float(self.eventInfo["y0"])+height*float(self.eventInfo["height"]))
        #     cropImg = img[yStart:yEnd, xStart:xEnd]  # 矩阵的第一项就是图片的y
        # else:
        #     pass
        if float(self.eventInfo["x0"])+float(self.eventInfo["width"]) > 1:
            xStart = int(width*float(self.eventInfo["x0"]))
            xEnd = int(width)
        else:
            xStart = int(width * float(self.eventInfo["x0"]))
            xEnd = int(width*float(self.eventInfo["x0"])+width*float(self.eventInfo["width"]))

        if float(self.eventInfo["y0"])+float(self.eventInfo["height"]) > 1:
            yStart = int(height*float(self.eventInfo["y0"]))
            yEnd = int(height)
        else:
            yStart = int(height * float(self.eventInfo["y0"]))
            yEnd = int(height*float(self.eventInfo["y0"])+height*float(self.eventInfo["height"]))
        cropImg = img[yStart:yEnd, xStart:xEnd]  # 矩阵的第一项就是图片的y

        # 匹配图片
        # cv2.imshow('result', cropImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        match self.matchWay :
            case "matchTemplate":
                posTemp = self.__matchTemplete(cropImg, mat, self.matchThreshold)
            case "matchSift":
                posTemp = self.__matchSift(cropImg, mat)

        # 把在裁剪的图片中的坐标点变为原图中的坐标点
        if posTemp is not None:
            xTemp ,yTemp= float(self.eventInfo["x0"])*width + posTemp[0], float(self.eventInfo["y0"])*height + posTemp[1]
            position = [int(xTemp/self.compressRate),
                        int(yTemp/self.compressRate)]
            info :dict ={}
            info["position"] = position
            Log4().log("info", f'imgEvent:找到图片{self.imgName},  坐标{position[0]} {position[1]}')
            self.sigEvent.emit(info)
            return position
        else:
            return None


# matchInfo = {
#     "x0": "0.5",
#     "y0": "0.1",
#     "width": "0.3",
#     "height": "0.4",
#     "name": "tingzhong.jpg",
#     "path": "D:/runhey/Uowl/Tasks/DailyGroup/DiGui"
# }
# srcImg = cv2.imread(str(Path.cwd().parent.parent/'Tasks'/'home.jpg'), cv2.COLOR_BGRA2GRAY)
# imgEvent = ImgEvent(srcImg, compressRate=1, matchWay="matchSift", matchThreshold=0.9, eventInfo=matchInfo)
# print(imgEvent.deal())

class IntVarEvent(QObject):
    """
    现在是int型变量
    """
    sigVarEvent = Signal(dict)
    def __init__(self, eventInfo :dict) -> None:
        super(IntVarEvent, self).__init__()
        self.name = eventInfo["name"]
        self.value = int(eventInfo["initVal"])
        self.compareType = eventInfo["compareType"]
        self.compareValue = int(eventInfo["compareValue"])
    def deal(self):
        """
        处理一次，如果达到预期发出信号
        :return:
        """
        match self.compareType:
            case "=":
                if self.value == self.compareValue:
                    self.sigVarEvent.emit("=")
                    return "="
                else:
                    return None
            case ">":
                if self.value > self.compareValue:
                    self.sigVarEvent.emit(">")
                    return ">"
                else:
                    return None
            case "<":
                if self.value < self.compareValue:
                    self.sigVarEvent.emit("<")
                    return "<"
                else:
                    return None
            case ">=":
                if self.value >= self.compareValue:
                    self.sigVarEvent.emit(">=")
                    return ">="
                else:
                    return None
            case "<=":
                if self.value <= self.compareValue:
                    self.sigVarEvent.emit("<=")
                    return "<="
                else :
                    return None
            case default: return None




# varInfo ={
#     "name":"var1",
#     "initVal":"0",
#     "compareType":"=", #字符串
#     "compareValue":"5"
# }
# vint = IntVarEvent(varInfo)
# print(vint.deal())
# vint.value=5
# print(vint.deal())

class OcrEvent(QObject):
    sigEvent = Signal(dict)  # 匹配到后发送事件
    def __init__(self, string :str, threshold :float, type : int,
                 x0 :float, width :float, y0 :float, height :float,
                 eventInfo :dict) -> None:
        """

        :param string:  要匹配的文字，
        :param threshold: 阈值
        :param type: 水平还是横的 1表示单行水平， 2表示竖直的文字
        :param x0:
        :param width:
        :param y0:
        :param height:
        :param eventInfo: 信息，待定
        """
        super(OcrEvent, self).__init__()
        self.string = string
        self.threshold = threshold
        self.type = type
        self.x0 = x0
        self.y0 =y0
        self.width = width
        self.height = height
        self.eventInfo = eventInfo
        # 开始配置
        match self.type:
            case 1:
                self.ocr = CnOcr()
            case 2:
                self.ocr = CnOcr(rec_model_name='ch_PP-OCRv3')

    def deal(self, scrImg) -> None:
        """

        :param scrImg: 截取的整个图片
        :return: 如果识别得到则返回对应中心坐标，否则NONE
        """
        # 裁剪图片
        width, height = scrImg.shape[1], scrImg.shape[0]  # 这个是图片压缩后的大小
        if self.x0 + self.width > 1:
            xStart = int(width * self.x0)
            xEnd = int(width)
        else:
            xStart = int(width * self.x0)
            xEnd = int(width * self.x0 + width * self.width)

        if self.y0 + self.height > 1:
            yStart = int(height * self.y0)
            yEnd = int(height)
        else:
            yStart = int(height * self.y0)
            yEnd = int(height * self.y0 + height * self.height)
        cropImg = scrImg[yStart:yEnd, xStart:xEnd]  # 矩阵的第一项就是图片的y

        # cv2.namedWindow('scrImg')  # 命名窗口
        # cv2.imshow("scrImg", cropImg)  # 显示
        # cv2.waitKey(0)
        # print("开始识别")
        # cv2.destroyAllWindows()

        # 开始识别
        match self.type:
            case 1:
                out = self.ocr.ocr(cropImg)
            case 2:
                out = self.ocr.ocr(cropImg)
        for one in out:
            if -1 != one["text"].find(self.string):
                centerX = (one["position"][0][0] + one["position"][2][0])/2 + (self.x0 * width)
                centerY = (one["position"][0][1] + one["position"][2][1]) / 2 + (self.y0 * height)
                return [centerX, centerY]
        return None

    def test(self) -> None:
        h = Handle()
        handleNum = h.getHandleNum("雷电模拟器")
        scrImg = h.getScreen(handleNum, [1280, 720], scaleRate=1.0)
        print(self.deal(scrImg))

# OcrEvent("游戏", 0.80, 1, 0.4, 0.26, 0.75, 0.12, {"eventName":"test"}).test()

