# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import sys
import importlib.util
from pathlib import Path

def loadStateModule(moduleName :str, moduleFile :str):
    """
    加载模块
    :param moduleName:
    :param moduleFile: 文件路径带py
    :return:
    """
    spec = importlib.util.spec_from_file_location(moduleName, moduleFile)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[moduleName] = module
    return module

def getAllStateModule(taskGroup :str, taskName :str):
    """

    :param taskGroup:
    :param taskName:
    :return: 返回
    """
    # taskName = str(Path(__file__).parent.name)
    taskPath = Path(__file__).resolve().parent.parent.parent / "Tasks" / taskGroup / taskName
    # moduleNameList = []
    # moduleFileList = []
    result = []
    for file in taskPath.iterdir():
        if file.is_dir() and file.parts[-1] != "__pycache__":
            temp = []
            temp.append(file.parts[-1])
            temp.append(str(file / f'{file.name}.py'))
            result.append(temp)
    return result

# for moduleName, moduleFile in getAllStateModule('DailyGroup', "地域鬼王"):
#     loadStateModule(moduleName, moduleFile)
# print(sys.modules)



