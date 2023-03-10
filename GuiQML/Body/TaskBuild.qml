import QtQuick 2.12
import QtQuick.Controls 2.12
import Qt5Compat.GraphicalEffects

import "../Component"
import "./TaskBuild.js" as TB

Item {
    Component.onCompleted: {
        //数据一切以这个页面为准
        var taskScheluder = JSON.parse(configFile.readTaskScheduler())
        buildGroup = taskScheluder["groupName"]
        buildName = taskScheluder["taskName"]
        taskBuild.root = JSON.parse(configFile.readTaskConfigUI(buildGroup, buildName))

    }
    property var root: {""}
    property string buildGroup: "DailyGroup"
    property string buildName: "DiGui"
    id: taskBuild
    BuildMenu{
        id: tBuildMenu
        height: parent.height
        width: 200
        anchors.right: parent.right
        stateName: machineGraph.stateIndex
    }
    Item{
        height: parent.height
        anchors.left: parent.left
        anchors.right: tBuildMenu.left
        MachineGraph{
            id: machineGraph
            width: parent.width
            anchors.top: parent.top
            anchors.bottom: splitLine.top
        }
        Rectangle{
            id: splitLine
            width: parent.width-8
            height: 8
            y: 500
            radius: 3
            color: "#FFCC00"
            MouseArea{
                id: splitLineMouseArea
                anchors.fill: parent
                property int lastY: 0
                hoverEnabled: true
                cursorShape: (containsMouse
                              ?Qt.SizeVerCursor
                              :Qt.ArrowCursor);
                onPressedChanged: {
                    //按下鼠标记录坐标
                    if(containsPress){
                        lastY = mouseY
                    }

                }
                onPositionChanged: {
                    if(pressed){
                        if( parent.y<=taskBuild.height-160 &&  parent.y>=160 ){
                        parent.y += mouseY - lastY
                        }
                        if(parent.y<160){
                            parent.y=160
                        }
                        if(parent.y >= taskBuild.height-160){
                            splitLine.y = taskBuild.height-160
                        }
                    }
                }
            }
        }
        BuildContents{
            id: tContexts
            width: parent.width
            anchors.top: splitLine.bottom
            anchors.bottom: parent.bottom
        }

    }
    RoundButton{
        width: 50
        height: width
        radius: 25
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 4
        anchors.right: parent.right
        anchors.rightMargin: 4
        background: Rectangle{
            id:backgroundRectangle1
            anchors.fill: parent
            radius: 25
            color: "#FFB5D83C"
            border.color: "#80ffffff"
            border.width: 1
        }
        DropShadow
        {
            anchors.fill: backgroundRectangle1
            radius: 8
            samples: 16
            color: "#B5D83C"
            source: backgroundRectangle1
         }
        contentItem:Text {
            text: "保存"
            color: "#ffffff"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
        MouseArea{
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            tContexts.saveContents(tBuildMenu.stateName, tContexts.showMainName, tContexts.showSubName) //保存当前显示的页面
            configFile.writeTaskConfigUI(buildGroup, buildName, JSON.stringify(taskBuild.root))
            var taskConfig = JSON.stringify(TB.ui2Config(root))
            configFile.writeTaskConfig(buildGroup, buildName, taskConfig)
            log4.log("info", "已保存")
        }
        }
    }

    function changeContents(mainName, subName){
        tContexts.saveContents(tBuildMenu.stateName, tContexts.showMainName, tContexts.showSubName)
        if(mainName === "0" && subName === "baseConfig"){
            tContexts.showContents("0", "0", "baseConfig")
        }else{
            tContexts.showContents(tBuildMenu.stateName, mainName, subName)
        }
    }

    function getStateList(){
        return TB.getStateList(taskBuild.root)
    }
    function getEventOActionList(type){
        if(type === "eventName"){
            return TB.getEventNameList(taskBuild.root, tBuildMenu.stateName)
        }else if(type === "actionName"){
            return TB.getActionNameList(taskBuild.root, tBuildMenu.stateName)
        }
    }
}
