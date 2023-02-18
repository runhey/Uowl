# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import sys
import importlib.util
from pathlib import Path

# def loadStateModule(moduleName :str):
#     """
#     加载模块
#     :param moduleName:
#     :return:
#     """
#     tasksFile = str(Path(__file__).resolve().parent / moduleName / f"{moduleName}.py")
#     # print(tasksFile)
#     spec = importlib.util.spec_from_file_location(moduleName, tasksFile)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     sys.modules[moduleName] = module
#     return module
#
# def getAllStateModule() -> list:
#     taskName = str(Path(__file__).parent.name)
#     taskPath = Path(__file__).resolve().parent
#     stateModuleList = []
#     for file in taskPath.iterdir():
#         if file.is_dir() and file.parts[-1] != "__pycache__":
#             stateModuleList.append(file.parts[-1])
#     # print(stateModuleList)
#     return stateModuleList
#
# for stateModule in getAllStateModule():
#     loadStateModule(stateModule)

# from GeneralEnter import GeneralEnter
from Src.Device import Device

class UTask:
    def __init__(self):
        pass

    def run(self):
        print("这里执行突破任务")
        # GeneralEnter()
