import pythoncom
import time
from pyWinhook import HookManager

windowName = "TheRender"  # TheRender是雷电模拟器的一个子窗口
mousePress = False


def onMouseEvent(event):
    # 监听鼠标事件
    global mousePress
    if event.WindowName == windowName:
        # print(f"MessageName: {event.MessageName}  Time: {event.Time}  Position: {event.Position}")
        if event.MessageName == "mouse left down":
            mousePress = True
        if event.MessageName == "mouse left up":
            mousePress = False
        if mousePress:
            print(event.Position)


    # print("MessageName:", event.MessageName)
    # print("Message:", event.Message)
    # print("Time:", event.Time)
    # print("Window:", event.Window)
    # print("WindowName:", event.WindowName)
    # print("Position:", event.Position)
    # print("Wheel:", event.Wheel)
    # print("Injected:", event.Injected)
    # print("------------------------------------------------")

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True

def onKeyboardEvent(event):
    # 监听键盘事件
    print("MessageName:", event.MessageName)
    print("Message:", event.Message)
    print("Time:", event.Time)
    print("Window:", event.Window)
    print("WindowName:", event.WindowName)
    print("Ascii:", event.Ascii, chr(event.Ascii))
    print("Key:", event.Key)
    print("KeyID:", event.KeyID)
    print("ScanCode:", event.ScanCode)
    print("Extended:", event.Extended)
    print("Injected:", event.Injected)
    print("Alt", event.Alt)
    print("Transition", event.Transition)
    print("---")
    # 同鼠标事件监听函数的返回值
    return True

def main() -> None:
    # 创建一个“钩子”管理对象
    hm = HookManager()
    # 监听所有键盘事件
    # hm.KeyDown = onKeyboardEvent
    # # 设置键盘“钩子”
    # hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()

if __name__ == '__main__':
    main()


