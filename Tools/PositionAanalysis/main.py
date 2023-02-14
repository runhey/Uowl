# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import os
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

# 路径 默认是 ./Uowl/Log
csvPath = Path(__file__).resolve().parent.parent.parent / 'Log'
# 文件列表 请改成路径下的
csvFileList = ['02-14^00@地域鬼王.csv',
               '02-14^00@突破.csv']
# 图的大小 默认1280x720
csvSize = [1280, 720]


def readCsv(path :str, fileList :list) -> None:
    """

    :param path:
    :param fileList:
    :return: 返回 点的列表列表
    """
    reslutX, reslutY = [], []
    for file in fileList:
        with open(os.fspath(path / file), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reslutX.append(int(row["x"]))
                reslutY.append(int(row["y"]))
    return reslutX, reslutY

def showCsv(xList :list, yList :list, size :list) -> None:
    x = np.array(xList)
    y = np.array(yList)


    fig, ax = plt.subplots(1, 1)
    mpl.style.use("seaborn-v0_8-dark")
    mpl.rcParams["figure.dpi"] = 300

    ax.invert_yaxis()
    ax.set_xlim((0, size[0]))
    ax.set_ylim((0, size[1]))
    plt.scatter(x, y, s=np.ones(x.size))
    plt.title("position")
    plt.show()


if __name__ == '__main__':
    xList, yList = readCsv(csvPath, csvFileList)
    showCsv(xList, yList, size=csvSize)
