
![logo](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/202302171623299.png)

## ❤为什么选择我们

项目最新状态：[全新规划 · Issue #3 · runhey/Uowl (github.com)](https://github.com/runhey/Uowl/issues/3)

- **自动托管**：设定好时间任务一整天可以去干其他的事情
- **安全防封**
- **高度扩展**
- **开源免费**
- **长期维护**


## 🎈安装方法

<details>
<summary></summary>

+ **以源码安装**(推荐)

  + 环境要求: python >= 3.10.8, 推荐使用pycharm+anaconda

  + 克隆或者下载 本项目

  + 安装库具体看**requirements.txt**

    ~~~powershell
    pip install -r requirements.txt
    ~~~

  + 接下来安装cnocr，这个比较特殊

    ~~~
    pip install cnocr
    ~~~

    如果不出意外的话会报错不能安装**Polygon3**

    ~~~python
    Microsoft Visual C++ 14.0 or greater is required. Get it with “Microsoft C++ Build Tools”: https://visualstudio.microsoft.com/visual-cpp-build-tools/   
    # 因为pip安装的时候 会重新编译一下，而这个包里面有c++文件但是你的电脑没有这个对应的构建工具，无法编译、无法安装，所以要安装我已经编译好的whl文件，运行下面的指令
    ~~~

    + ~~~python
      pip install wheel
      pip install pip install ./Src/Task/Polygon3-3.0.9.1-cp310-cp310-win_amd64.whl
      # 我电脑是amd64的
      ~~~

  + 安装库之后，运行 main.py

  + 打包项目可看[Uowl/Docs/打包项目](https://github.com/runhey/Uowl/blob/master/Docs/打包项目.md)

+ **以打包程序**

  + **star**支持一下不过分吧
  
  点击这里[Releases · runhey/Uowl (github.com)](https://github.com/runhey/Uowl/releases)
  
  解压大概需要四百多兆空间

</details>

## 🎁使用方法

<details>
<summary></summary>

+ 下载客户端，支持：雷电模拟器[官网](https://www.ldmnq.com)、MuMu模拟器[官网](https://yys.163.com/zmb)(**需要以管理员身份打开脚本**)    安卓手机(不保证能正常运行)


  作者强烈推荐使用雷电模拟器或者mumu模拟器

+ 软件启动默认加载所有配置，所以安全起见修改保存后重启

#### 软件设置

###### 基础设置

+ deviceType:  **mumu模拟器** 准没错
+ defaultWidth: 默认1280，不要改
+ defaultHeight: 默认720,  不要改
+ windowScaleRate:  改了也没用每次启动重新加载

###### 安卓设备

+ connectType
+ getScreenWay
+ controlWay  这三者默认adb
+ adbConnectChannel：选usb连接，手机记得开 **开发者选项** 去百度一下每个手机都不同
+ deviceId
+ androidWidth
+ androidHeight 这三者改了也没用每次启动重新加载

###### mumu模拟器

**！！！首先说明一下：例如mumu模拟器等新晋大厂模拟器与老牌模拟器如雷电模拟器底层架构不同**

！！！老牌模拟器是真的虚拟出一个手机，而大厂模拟器是把arm的指令集翻译为window的API

+ connectType ：选adb，window前台需要以管理员身份运行而且桌面鼠标都不能用
+ getScreenWay:  必须跟connectType保持一致
+ controlWay:  必须跟connectType保持一致
+ deviceId: 127.0.0.1:7555别改
+ mumuWidth: 1280
+ mumuHeight: 720
+ handleTitle:  阴阳师 - MuMu模拟器
+ handleNum: 每次启动mumu模拟器都不同

###### 雷电模拟器(推荐推荐再推荐)

+ connectType ：选window后台，但是游戏是不能最小化的可以被其他软件覆盖，推荐新开一个window虚拟桌面
+ getScreenWay:  必须跟connectType保持一致
+ controlWay:  必须跟connectType保持一致
+ mumuWidth: 1280
+ mumuHeight: 720
+ handleTitle:  雷电模拟器
+ handleNum: 每次启动雷电模拟器都不同

#### 客户端设置

###### mumu模拟器

+ 设置分辨率为 1280x720

###### 雷电模拟器

+ ->性能设置 -> 设置分辨率为 1280x720 平板型
+ ->其他设置 -> 设置ADB调试：开启本地链接

#### 游戏设置

+ 庭院选择默认皮肤

  ![image-20230118234546031](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230118234546031.png)

+ 关闭

  ![image-20230118234807124](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230118234807124.png)

+ 旧版

  ![image-20230127012326570](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230127012326570.png)

+ 结界默认

  ![image-20230214162201668](https://raw.githubusercontent.com/runhey/imgStg1/master/img2/202302141622137.png)

#### 详细使用

！！！**作者在写的时候为了提进度没有考虑各种异常情况**，请一定按照说明来操作**mumu模拟器必须用管理员运行脚本**

如有一些不正常的情况请先保存，再重启

+ 第一次打开脚本进入设置设备， 保证句柄一致   

  ![image-20230214171118711](https://raw.githubusercontent.com/runhey/imgStg1/master/img2/202302141711775.png)

  ![image-20230214171432693](https://raw.githubusercontent.com/runhey/imgStg1/master/img2/202302141714046.png)

  ![image-20230214171704829](https://raw.githubusercontent.com/runhey/imgStg1/master/img2/202302141717319.png)

+ 启动游戏再打开Uowl，若接入成功则显示正确的handleNum或者deviceId, 以及设备尺寸

  ![image-20230207164021157](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230207164021157.png)

  ![image-20230207164723281](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230207164723281.png)

+ 点击左边菜单第二个任务调度中心，三个页面分别是每周，每日，立即执行三类，最下边自行添加删除设置。

  ![image-20230207164923000](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230207164923000.png)

+ 值得一提的是的forthwith 下面的default queue是一个下拉框，可以选择设置多个以便不同情况切换

+ 点击左边菜单第一个，点击启动即可运行刚刚添加到forthwith上的任务

+ 游戏多开：目前仅支持雷电模拟器，每多开一个游戏需要复制一份游戏文件，并对于不同的游戏窗口设置不同的handleTitle（在任务管理器可以看到）

![image-20230214171838833](https://raw.githubusercontent.com/runhey/imgStg1/master/img2/202302141718703.png)

![image-20230207165839799](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230207165839799.png)

#### 注意事项

+ 使用window后台时游戏窗口不能点击最小化（但是可以被覆盖），否则脚本无法获取游戏截图而无法正常运行

+ 想保持window桌面干净正确的做法是新建一个虚拟桌面(自行百度一下)，把游戏和脚本放到单独一个桌面

  ![image-20230207165252156](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/image-20230207165252156.png)

  

**如有疑惑请往 搭建任务 [章节](https://github.com/runhey/Uowl/blob/master/Docs/搭建任务.md)**

</details>

## 🔎功能浏览

<details>
<summary></summary>

![屏幕截图 2023-01-27 012140](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202023-01-27%20012140.jpg)

![屏幕截图 2023-01-27 011817](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202023-01-27%20011817.jpg)

#### 工程结构（截至2023.2.15）

~~~
Uowl
├─GuiQML								前端UI文件
├─GuiImage                                                              前端UI切图
│  ├─background
│  ├─configelement
│  ├─logo
│  ├─pullmenu
│  ├─window
├─Log									日志文件及鼠标坐标文件
├─Docs									文档
├─Tools									辅助工具，具体请读对应readme
├─Src									python文件以及一些dll
│  ├─Component		                      	                        一些自定义的组件
│  ├─Task								每个任务的运行
├─Tasks									每个任务具体的配置
│  ├─DefaultGroup						        一些特殊的任务
│  	 ├─Before							每个任务循环的前置判断
│  	 ├─Slice 							切图，统一
│  	 ├─Template							任务模板
│  ├─DailyGroup							        每日任务
│  ├─WeeklyGroup						        每周任务
│  ├─御魂Group						                针对御魂而抽离出来的一个组
│  ├─活动Group						                活动任务
├─Tasks								        配置文件
│  ├─setting.json						        软件设置文件
│  ├─taskScheduler.json					                任务时间安排文件
~~~



</details>

## 🚨防封说明

[Docs/防封说明](https://github.com/runhey/Uowl/blob/master/Docs/防封说明.md)

## ✏搭建任务

[Docs/搭建任务](https://github.com/runhey/Uowl/blob/master/Docs/搭建任务.md)

## 📝更新计划

<details>
<summary></summary>

+ [ ] 开机自启
+ [ ] task时间触发上线游戏

#### Event

| 实现 | Name        | 名字         | 描述                         |
| ---- | ----------- | ------------ | ---------------------------- |
| ✅    | imgEvent    | 图像事件     | 非常重要的一个事件输入       |
| ❌    | intVarEvent | 整形变量事件 | 变量的触发对计数等等很有帮助 |
| ❌    | randomEvent | 随机触发事件 | 应对风控处理                 |
| ❌    | timeEvent   | 时间事件     | 任务内获取实际时间来进行处理 |
| ❌    | ocrEvent    | 文字识别事件 |                              |

#### Action

| 实现 | Name              | 名字         | 描述                   |
| ---- | ----------------- | ------------ | ---------------------- |
| ✅    | transitionsAction | 状态迁移动作 | 状态机根本action       |
| ✅    | clickAction       | 点击动作     | 非常重要的一个事件输入 |
| ❌    | intChangeAction   | 整形变量动作 |                        |
| ✅    | swipeAction       | 滑动动作     |                        |
| ❌    |                   |              |                        |

#### Tasks

###### 每日任务

| name                | description                            |
| ------------------- | -------------------------------------- |
| ✅地狱鬼王           | 打三个鬼王                             |
| ✅封魔之时           | 点四次灯笼和打boss                     |
| ✅结界卡寄养收卡挂卡 | 包括每日收取资金，以高星太鼓斗鱼为主   |
| ✅寮领体力20         | 寮补给体力不到20也可领                 |
| ✅商店每天免费一次   |                                        |
| ✅上线领东西         | 包括签到、领勾玉、收小纸人、领邮箱等待 |
| ✅结界突破           | 打输了自动刷新                         |
| ✅喂养猫咪           |                                        |
| ✅悬赏封印           | 自动邀请                               |
| ✅花合战收取         |                                        |
| 每日一抽            |                                        |
| ✅收友情点           |                                        |
| 寮30                |                                        |
| 狩猎战              |                                        |
| 经验副本            |                                        |
| 金币副本            |                                        |

###### 每周任务

| name                  | description |
| --------------------- | ----------- |
| ✅杂货铺(蓝屏黑蛋体力) |             |
| 图鉴分享              |             |
| 秘闻十层              |             |
| 秘闻分享              |             |
| 寮功勋兑换            |             |
| 寄售屋一百勾玉        |             |
| 秘卷屋紫蛇皮          |             |
| 杂货铺御灵40张        |             |
| 唤妖借处千屋宝库兑换  |             |
| 地狱鬼王分享20勾      |             |

###### 肝帝任务

| name            | description                                                  |
| --------------- | ------------------------------------------------------------ |
| ✅单人挖土       |                                                              |
| ✅双人挖土(队长) | 稳定队友：需要最近一起打过，并且在界面上截取好友头像保存到任务路径friend1.jpg 或者 friend2.jpg （覆盖） |
| ✅多人挖土(队员) | 稳定队友：需要以前打过，勾选邀请时“不再提示”                 |
| ✅业原火         |                                                              |
| 魂水            |                                                              |
| 日轮            |                                                              |
| 六道            |                                                              |
| 觉醒            |                                                              |
| 突破            |                                                              |
| 御灵            |                                                              |
| 困28            |                                                              |

###### 活动任务

| 历次任务列表       | 描述 |
| ------------------ | ---- |
| ✅<2023春节> 伴星歌 |      |

</details>

## 📆更新日志

<details>
<summary></summary>

+ 2023.2.15:  新增坐标记录分析，spyxx工具，鼠标监听脚本，机器行为判断例子， 滑动仿真
+ 2023.2.14:  新增滑动动作，mumu模拟器后台，本地日志和点击滑动位置统计 
+ 2023.2.07:  新增游戏多开，优化启动连接游戏异常显示，修复由于qt兼容性导致渲染混乱而覆盖原有的UI
+ 2023.1.26:  优化UI动画，接受勾协
+ 2023.1.18:  伟大的里程碑！！！完成<地域鬼王>
+ 2023.1.15:  task list done! and complete a part of the scheduler UI
+ 2023.1.14:  "Task Build"   finished!!!
+ 2023.1.13：还有一些Task
+ 2023.1.11：完成一半Task的Build界面
+ 2023.1.8:  rename ThreadRun to TaskScheduler and the forthwith Task function is realized。 添加clickAction, transitionsAction和imgEvent。然后初步实现了task的内容
+ 2023.1.7:   忘记了实现了什么了
+ 2023.1.4：解决雷电模拟器后台模式bug，实现Device类
+ 2023.1.3：实现Bridge,Log4,ThreadRun：建立qml与python通信。实现Adb即Handle设备接口
+ 2023.1.2：打包测试，实现启动页UI，设置页UI，编写基本设置JSON文件
+ 2022.12.29：搭建部分UI框架
+ 2022.12.28：实现部分设计稿
+ 2022.12.27：每一个优秀的项目都是从新建文件夹开始


</details>

## 	⭐Q&A

<details>
<summary></summary>

​    

</details>

## 🙋‍♀️后记

<details>
<summary></summary>

+ 感谢aicezam的项目[SmartOnmyoji](https://github.com/aicezam/SmartOnmyoji)
+ 感谢itmorn的项目[robot-mouse-track](https://github.com/itmorn/robot-mouse-track)
+ 感谢2833844911的项目[gurs](https://github.com/2833844911/gurs)
+ QQ群：743726482 **欢迎加入我们**
+ 如有不足之处还请多多指教

</details>

![QQ图片20230123005204](https://runhey-img-stg1.oss-cn-chengdu.aliyuncs.com/img2/QQ%E5%9B%BE%E7%89%8720230123005204.jpg)
