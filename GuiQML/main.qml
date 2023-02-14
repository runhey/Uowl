import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12
import QtQml 2.12
import Qt.labs.settings 1.1
import Qt5Compat.GraphicalEffects

import "./Pane"
import "./Body"
import "./Component"
import "./Component/ajax.js" as Ajax


Window {
    id:rootWindow
    width: 700+8
    height: 700+8 // +8是因为外阴影一边用了4
    minimumWidth: 400
    minimumHeight: 400
    visible: true
    color: '#00000000'
    flags:   Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint| Qt.Window

    property int menuPaneFlag
    Settings{
        property alias windowWidth: rootWindow.width
        property alias windowHeight: rootWindow.height
    }
    //外阴影
    DropShadow{
        anchors.fill: windowMain
        horizontalOffset: 1
        verticalOffset: 1
        radius: 8
        samples: 16
        source: windowMain
        color: "#1abc9c"
        Behavior on radius { PropertyAnimation { duration: 100 } }
    }
    //主界面
    Rectangle{
        id:windowMain
        anchors.fill: parent
        radius: 12
        clip: true
        // 当窗口全屏时，设置边距为 0，则不显示阴影，窗口化时设置边距为 6 就可以看到阴影了
        anchors.margins: rootWindow.visibility === Window.Maximized ? 0 : 4
        //color: "#663399"
        //背景
        Image {
            id:windowBackground
            anchors.fill: windowMain
            source: "../GuiImage/background/background1.jpg"
            clip: true
            visible: false
        }

        // 圆形窗口
        OpacityMask {
                id: mask
                anchors.fill: windowBackground
                source: windowBackground
                maskSource: windowMain
         }
        //高斯模糊
        FastBlur{
            anchors.fill: windowMain
            source: windowBackground
            radius: 24
        }



        //菜单
        MenuPane{
            id:menuPane
            anchors{
                left: parent.left
                leftMargin: 12
                top: parent.top
                topMargin: 12
                bottom: parent.bottom
                bottomMargin: 12
            }
            onMenuPaneFlagChanged: {
                rootWindow.menuPaneFlag = menuPane.menuPaneFlag
                bodyPane.changeBodySource(menuPane.menuPaneFlag)
            }
        }

        //标题栏
        Item {
            height: 30
            anchors{
                left: (menuPane.visible === true)?  menuPane.right:parent.left
                right: parent.right
                top: parent.top
            }

            //拖动栏
            Item {
                anchors.fill: parent
                TapHandler {
                    onTapped: if (tapCount === 2) toggleMaximized()
                    gesturePolicy: TapHandler.DragThreshold
                }
                DragHandler {
                    grabPermissions: TapHandler.CanTakeOverFromAnything
                    onActiveChanged: if (active) { rootWindow.startSystemMove(); }
                }
            }
            //四个按钮
            Row{
                anchors{
                    right: parent.right
                    rightMargin: 8
                    verticalCenter: parent.verticalCenter
                }
                spacing: 16
                Button{  //帮助hlep github
                    width: 24
                    height: 24
                    flat:true
                    highlighted: true
                    background: Rectangle{
                        anchors.fill: parent
                        radius: 4
                        color: "transparent"
                    }
                    icon.source: "../GuiImage/window/help.png"
                    icon.color: "transparent"
                    icon.width: parent.width
                    icon.height: parent.height
                    MouseArea{
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { Qt.openUrlExternally("https://github.com/runhey/Uowl") }
                    }
                }
                Button{  //最小到任务栏
                    width: 24
                    height: 24
                    background: Rectangle{
                        anchors.fill: parent
                        color: "transparent"
                    }
                    icon.source: "../GuiImage/window/window-minimize.png"
                    icon.color: "transparent"
                    icon.width: parent.width
                    icon.height: parent.height
                    MouseArea{
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { rootWindow.showMinimized() }
                    }
                }
                Button{  //最大化最小化
                    width: 24
                    height: 24
                    background: Rectangle{
                        anchors.fill: parent
                        color: "transparent"
                    }
                    icon.source: (rootWindow.visibility === Window.Maximized ) ?"../GuiImage/window/window-restore.png" : "../GuiImage/window/window-maximize.png"
                    icon.color: "transparent"
                    icon.width: parent.width
                    icon.height: parent.height
                    MouseArea{
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if(rootWindow.visibility === Window.Maximized ) {
                            rootWindow.showNormal();
                        }
                        else{
                            rootWindow.showMaximized()
                        }
                        }
                    }
                }
                Button{  //关闭软件
                    width: 24
                    height: 24
                    background: Rectangle{
                        anchors.fill: parent
                        color: "transparent"
                    }
                    icon.source: "../GuiImage/window/window-close.png"
                    icon.color: "transparent"
                    icon.width: parent.width
                    icon.height: parent.height
                    MouseArea{
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        bridge.sigThreadExit()
                        rootWindow.close() }
                    }
                }

            }
        }
        //图标
        Item {
            id: logo
            height: 36
            width: 140
            anchors{
                left: (menuPane.visible === true)?  menuPane.right:parent.left
                leftMargin: 12
                top: parent.top
                topMargin: 12
            }
            Image {
                id: appLoge
                height: parent.height
                width: parent.height
                anchors.left: parent.left
                source: "../GuiImage/logo/logo-64.ico"
            }
            Label{
                id: appName
                anchors.left: appLoge.right
                anchors.leftMargin: 2
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Uowl")
                color: "#FFCC00"
                font.bold: true
                font.pixelSize: 28
            }
            Label{
                id: appVersion
                anchors.left: appName.right
                anchors.leftMargin: 4
                anchors.bottom: parent.bottom
                text: qsTr("v0.3-beta")
                color: "#FFCC00"
                font.bold: false
                font.pixelSize: 12
            }
            Button{
                anchors.fill: parent
                background: Rectangle{
                    anchors.fill: parent
                    radius: 4
                    color: "transparent"
                }
                MouseArea{
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: { Qt.openUrlExternally("https://github.com/runhey/Uowl") }
                }
            }
        }
        //主体
        BodyPane{
            id:bodyPane
            anchors.top: logo.bottom
            anchors.topMargin: 4
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 12
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.left: (menuPane.visible === true)?  menuPane.right:parent.left
            anchors.leftMargin: 12
        }
        //弹出显示异常信息
        Snackbar{
            id: snackbar
        }
    }
    //更新对话框
    UDialog{
        id:updaeDialog
        TextArea{
            id:infoText
            anchors.fill: parent
        }

        function buttonClicked(label){
            updaeDialog.close()
        }
        Component.onCompleted: {
           updaeDialog.footerButtonClicked.connect(buttonClicked)
           Ajax.get("https://api.github.com/repos/runhey/Uowl/releases/latest",
                    function(result, json){         //成功后的回调函数
                        if(json["tag_name"]!==appVersion.text){
                            updaeDialog.title = "最新版本"+json["tag_name"]
                            infoText.text = json["body"].substring(0, json["body"].indexOf('\r\n### 下载使用',0))
                            updaeDialog.open()
                        }
                    },function (){              //失败后的回调函数
                        console.log("error")
                    })
        }}
    //改变鼠标形状
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: {
            if (rootWindow.visibility !== Window.Maximized){
            const p = Qt.point(mouseX, mouseY);
            const b = 4; // Increase the corner size slightly
            if (p.x < b && p.y < b) return Qt.SizeFDiagCursor;
            if (p.x >= width - b && p.y >= height - b) return Qt.SizeFDiagCursor;
            if (p.x >= width - b && p.y < b) return Qt.SizeBDiagCursor;
            if (p.x < b && p.y >= height - b) return Qt.SizeBDiagCursor;
            if (p.x < b || p.x >= width - b) return Qt.SizeHorCursor;
            if (p.y < b || p.y >= height - b) return Qt.SizeVerCursor;
            }
        }
        acceptedButtons: Qt.NoButton // don't handle actual events
    }
    //边界跟随拖动
    DragHandler {
        id: resizeHandler
        grabPermissions: TapHandler.TakeOverForbidden
        target: null
        onActiveChanged: if (rootWindow.visibility !== Window.Maximized) {
                             if (active) {
                             const p = resizeHandler.centroid.position;
                             const b =  20; // Increase the corner size slightly
                             let e = 0;
                             if (p.x <= b) { e |= Qt.LeftEdge }
                             if (p.x >= width - b) { e |= Qt.RightEdge }
                             if (p.y <= b) { e |= Qt.TopEdge }
                             if (p.y >= height - b) { e |= Qt.BottomEdge }
                             if(e != 0) {rootWindow.startSystemResize(e);}
                             }
                         }
    }
    // 最大最小
    function toggleMaximized() {
        if (rootWindow.visibility === Window.Maximized) {
            rootWindow.showNormal();
        } else {
            rootWindow.showMaximized();
        }
    }
    // 切换菜单项 对外接口
    function changeMenu(index){
        menuPane.menuPaneFlag = index
    }
}
