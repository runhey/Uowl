# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import sys
import json
import time
import importlib.util

from numpy import random
from PySide6.QtCore import QThread, QObject, Signal, Slot
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path

from Src.Log4 import Log4, singleton
from Src.ConfigFile import ConfigFile
from Src.Bridge import Bridge
from Src.Device import Device
from Src.Task.Task import Task
from Src.Task.TaskLoad import loadStateModule, getAllStateModule



def queueExecute() -> None:
    """
    BlockingScheduler是在一个进程下面的所以说是非阻塞的可能会有同时有多个个任务执行,而我们的需求是唯一的任务执行并且FIFO
    所以说要定义一个队列，需要一个轮询来执行任务
    我们是这么设计的：apscheduler单纯作为一个定时器作用来触发weekly和daily任务，触发之后把任务添加到queue;
                  当然forthwidth任务也在点击按钮的时候添加到queue,好了现在得到了任务队列
                  然后我们要设计在apscheduler中5s轮询一次判断队列是否有任务，如果有则执行（噢对了加上一个互斥锁）
    :return:
    """
    taskSche = TaskScheduler()  # 单例模式只是拿到一个引用
    if len(taskSche.queue) != 0 and taskSche.lock is True:
        taskSche.lock = False  # 记得后面释放
        taskInfo = taskSche.queue[0]
        del taskSche.queue[0]
        Bridge().sigUIUpdatePresentTask.emit(taskInfo["taskName"])  # 向ui发送当前的任务
        Log4().slotStartLog(taskInfo["taskName"])
        taskSche.task = Task(taskInfo["taskGroup"], taskInfo["taskName"], taskSche.device)
        taskSche.task.run()
        Log4().slotFinishLog()
        taskSche.lock = True  # 释放锁

def queueAdd(taskGroup :str, taskName :str) -> None:
    """
    这个用于 给week和day设置定时向queue添加task的函数
    :return:
    """
    taskInfo: dict = {"taskGroup": taskGroup, "taskName": taskName}
    TaskScheduler().queue.append(taskInfo)

@singleton
class TaskScheduler(QThread):
    def __init__(self) -> None:
        super().__init__()
        self.device = Device(ConfigFile.getSettingDict("baseSetting"),
                             ConfigFile.getSettingDict("android"),
                             ConfigFile.getSettingDict("mumu"),
                             ConfigFile.getSettingDict("leidian"))

        self.task : Task= None
        self.queue :list = []  # 队列每一项都是任务的信息 包括指向具体的任务，以及当前设备的信息
        self.lock :bool = True   #任务互斥锁， true表示还没有上锁可以执行任务，false表示正在执行任务不能拿走
        self.scheduler = BlockingScheduler()
        self.scheduler.coalescing= True  # 哑弹任务关闭
        self.scheduler.add_job(queueExecute, id="queneExecute",
                               trigger="interval", seconds=5, max_instances=5, coalesce=False, jitter=0)
        Bridge().sigPresentTasks.connect(self.slotPresentTasks)
        Bridge().sigThreadExit.connect(self.slotThreadExit)
        Bridge().sigUIUpdateProgressBar.emit(0.4)

    def run(self) -> None:
        """
        第二个线程后端线程
        """
        QThread.sleep(1)  # 等个三秒钟设备qml初始化
        self.device.connect()
        self.device.updateSettingToFile()

        self.addWeeklyTask()
        self.addDailyTask()
        self.scheduler.start()

    @Slot(str)
    def slotPresentTasks(self, cmd: str) -> None:
        """
        由ui端控制的 任务按钮 有
        :param cmd:
        :return:
        """
        print(cmd)
        if cmd == "start":  # 开始
            self.addForthwithTask()
        elif cmd == "pause":  # 暂停
            self.task.taskChangeState("onPause")
            self.scheduler.pause()
            self.scheduler.pause_job("queneExecute")
        elif cmd == "resume": # 继续
            self.task.taskChangeState("running")
            self.scheduler.resume()
            self.scheduler.resume_job("queneExecute")
        elif cmd == "stop":  # 停止
            self.queue.clear()
            self.task.taskChangeState("quit")

    @Slot()
    def slotThreadExit(self) -> None:
        self.scheduler.remove_all_jobs()
        if self.task:
            self.task.taskChangeState("quit")
        self.scheduler.shutdown(wait=False)
        self.terminate()  # 不安全退出

    def addWeeklyTask(self) -> None:
        schedulerInfo: str = ConfigFile().readTaskScheduler()
        infoRoot = json.loads(schedulerInfo)
        for item in infoRoot["weekly"]:
            w :str = "mon"
            match item["week"]:
                case "周一":
                    w = "mon"
                case "周二":
                    w = "tue"
                case "周三":
                    w = "wed"
                case "周四":
                    w = "thu"
                case "周五":
                    w = "fri"
                case "周六":
                    w = "sat"
                case "周日":
                    w = "sun"
            jitter = 600 if (item["random"] == "true") else None
            taskInfo: dict = {"taskGroup": item["groupName"], "taskName": item["taskName"]}
            self.scheduler.add_job(queueAdd, trigger='cron', day_of_week=w, hour=4, minute =4,
                                   jitter=jitter, timezone='Asia/Shanghai', kwargs=taskInfo)

    def addDailyTask(self) -> None:
        schedulerInfo: str = ConfigFile().readTaskScheduler()
        infoRoot = json.loads(schedulerInfo)
        for item in infoRoot["daily"]:
            jitter = 600 if (item["random"] == "true") else None
            taskInfo: dict = {"taskGroup": item["groupName"], "taskName": item["taskName"]}
            self.scheduler.add_job(queueAdd, trigger='cron', hour=item["hour"], minute =item["minute"],
                                   jitter=jitter, timezone='Asia/Shanghai', kwargs=taskInfo)


    def addForthwithTask(self) -> None:
        """
        向队列添加任务
        :return:
        """
        schedulerInfo :str = ConfigFile().readTaskScheduler()
        infoRoot = json.loads(schedulerInfo)
        for queue in infoRoot["forthwith"]:
            if queue["queue"] == infoRoot["forthwithCurrentQueue"]:  # 找到这个队列
                if queue["runModel"] == "单次执行":  # 单次执行就是 顺序执行一次
                    for info in queue["list"]:
                        taskInfo :dict ={"taskGroup":info["group"], "taskName":info["task"]}
                        self.queue.append(taskInfo)
                elif queue["runModel"] == "顺序循环":  # 要读列表的任务文件获取运行时间好计算
                    totalTime :float = 0.0
                    configFile = ConfigFile()
                    while totalTime <= float(queue["runTime"]):
                        for info in queue["list"]:
                            taskRoot = json.loads(configFile.readTaskConfig(info["group"], info["task"]))
                            if totalTime + float(taskRoot["runTime"]) <= float(queue["runTime"]):
                                totalTime += float(taskRoot["runTime"])
                                taskInfo: dict = {"taskGroup": info["group"], "taskName": info["task"]}
                                self.queue.append(taskInfo)
                            else:  # 保证计算的永远是小于预定的时间
                                return  # 直接退出两个循环
                elif queue["runModel"] == "随机循环":
                    totalTime :float = 0.0
                    configFile = ConfigFile()
                    while totalTime <= float(queue["runTime"]):
                        random.shuffle(queue["list"])  # 每次都打乱就可以了
                        for info in queue["list"]:
                            taskRoot = json.loads(configFile.readTaskConfig(info["group"], info["task"]))
                            if totalTime + float(taskRoot["runTime"]) <= float(queue["runTime"]):
                                totalTime += float(taskRoot["runTime"])
                                taskInfo: dict = {"taskGroup": info["group"], "taskName": info["task"]}
                                self.queue.append(taskInfo)
                            else:  # 保证计算的永远是小于预定的时间
                                return  # 直接退出两个循环



def loadTask(taskGroup :str, taskName :str) -> None:
    tasksFile = str(Path(__file__).resolve().parent.parent / "Tasks" / taskGroup / taskName / "UTask.py")
    print(tasksFile)
    loadStateModule('UTask', tasksFile).UTask().run()

# loadTask("DailyGroup", "地域鬼王")
