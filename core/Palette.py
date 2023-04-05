# -*- coding:utf-8 -*-
# @time:2023/4/415:02
# @author:LX
# @file:Palette.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QWidget,
    QPainter,
    QColor,
    QRect,
    QPen,
    QBrush,
    QPoint,
    QMouseEvent,
    QPixmap,
    qt,
    QRect,
    QPoint,
    QPaintEvent
)
import typing
PathType = typing.TypeVar("PathType",QRect,QPoint)

class GraphManagement:
    def __init__(self):
        # freedomLine 自由线,特殊图形
        self.__graphs = {
            "cu_graph": "freedomLine",  # 当前绘制的图形
            "managements": {"rect": [], "line": [], "ellipse": [],"freedomLine":[]}  # 记录
        }

    def setShape(self,shape:str):
        self.__graphs["cu_graph"] = shape

    def shape(self)->str:
        return self.__graphs["cu_graph"]

    # 获取指定形状的路径信息
    def getPathInformation(self,shape:str)->list:
        return self.__graphs["managements"][shape]

    # 获取当前形状的路径信息
    def cuShapePathInfo(self)->list:
        return self.getPathInformation(self.shape())

    # 给当前形状添加路径信息
    def appendPathInformation(self,path_args:PathType):
        self.__graphs["managements"][self.shape()].append(path_args)

    def getManagements(self)->dict:
        return self.__graphs["managements"]


class Palette(QWidget):
    def __init__(self,*args,**kwargs):
        super(Palette, self).__init__(*args,**kwargs)
        
        self.painter = QPainter()
        self.painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform)

        op = QPen()
        op.setColor(QColor(255,0,0))
        op.setWidth(3)
        # 画板的配置
        self.options={
            "bg":QColor(255,255,255) , # 背景颜色
            "cu_brush":QColor(255,0,0),
            "cu_open":op,
        }

        # 鼠标信息相关的
        self.mouse_info={
            "isClick":False,
            "click_pos":QPoint(0,0),
            "cu_click":QPoint(0,0),
            "isPitch":False, # 是否选中图形
            "pitch_info":None #选中的信息
        }

        # 图形管理器
        self.graphs = GraphManagement()

        # 开启鼠标跟踪
        self.setMouseTracking(False)

        self.painter.setBrush(self.options["bg"])

    # 切换绘制的图形
    def setGraph(self,name):
        self.graphs.setShape(name)

    # 判断一个坐标点是否在矩形上
    def isRectRange(self,pos:QPoint,rect:QRect)->bool:
        if pos.x() >= rect.x() and pos.x() <= rect.x() + rect.width() and \
                pos.y() >= rect.y() and pos.y() <= rect.y() + rect.height():
            return True
        return False

    # 判断图形是否选中,是者返回信息
    def pitch(self,pos:QPoint)->tuple:
        # 如果是点击在同一个图形上,则直接返回
        # if self.mouse_info["isPitch"]:
        #     name = self.mouse_info["pitch_info"][0]
        #     info = self.mouse_info["pitch_info"][1]
        #     if self.isRectRange(pos,QRect(*info)):
        #         return name, info

        for name,graph in self.graphs.getManagements().items():
            for info in graph[::-1]:
                if name in ["rect","ellipse"]:
                    if self.isRectRange(pos,QRect(*info)):
                        return name,info
        return False

    def mousePressEvent(self, e:QMouseEvent):
        if e.button() == 1:
            pch = self.pitch(e.pos())
            if pch:
                self.mouse_info["isPitch"] = True
                self.mouse_info["pitch_info"] = pch
            else:
                self.mouse_info["isPitch"] = False
                self.mouse_info["pitch_info"] = None

                self.mouse_info["isClick"] = True

                self.mouse_info["click_pos"] = e.pos()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e:QMouseEvent):
        if e.button() == 1:
            if self.mouse_info["isPitch"]:
                self.update()
                super().mouseReleaseEvent(e)
                return

            # 加入图形管理器
            if self.graphs.shape() in ["rect","ellipse"]:
                x, y = self.mouse_info["click_pos"].x(),self.mouse_info["click_pos"].y()
                w, h = e.x()-x,e.y()-y
                if w < 0 or h < 0:
                    w,h = abs(w),abs(h)
                    x = x-w
                    y = y-h
                self.graphs.appendPathInformation((x, y, w, h))
            elif self.graphs.shape() == "line":
                x1, y1 = self.mouse_info["click_pos"].x(), self.mouse_info["click_pos"].y()
                x2, y2 = e.x(), e.y()
                self.graphs.appendPathInformation((x1, y1, x2, y2))
            elif self.graphs.shape() == "freedomLine":
                self.graphs.appendPathInformation(None) # 加入一个断点,防止所有画的图都是连续的
                print(self.graphs.getPathInformation("freedomLine"))
            self.mouse_info["isClick"] = False
            self.mouse_info["click_pos"] = QPoint(0,0)

        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e:QMouseEvent):
        self.mouse_info["cu_click"] = e.pos()
        if self.graphs.shape() == "freedomLine":
            self.graphs.appendPathInformation((e.x(),e.y()))
        self.update()
        super().mouseMoveEvent(e)

    def paintEvent(self, e:QPaintEvent):
        self.painter.begin(self)
        self.painter.drawRect(e.rect())

         # 优先渲染图形管理中的图形
        self.painter.setPen(self.options["cu_open"])
        self.painter.setBrush(self.options["cu_brush"])

        start_freedomLine = None
        end_freedomLine = None
        for name,graph in self.graphs.getManagements().items():
            for info in graph:
                # 标记选中
                if self.mouse_info["isPitch"]:
                    if info == self.mouse_info["pitch_info"][1]:
                        op = QPen()
                        op.setColor(QColor(30, 30, 45))
                        op.setWidth(3)
                        self.painter.setPen(op)

                if name == "rect":
                    self.painter.drawRect(*info)
                elif name == "ellipse":
                    self.painter.drawEllipse(*info)
                elif name == "line":
                    self.painter.drawLine(*info)
                elif name == "freedomLine":
                    if len(graph) > 1:
                        if start_freedomLine is None and end_freedomLine is None:
                            start_freedomLine = end_freedomLine = info
                        else:
                            if info is None:
                                start_freedomLine = end_freedomLine = None
                            else:
                                start_freedomLine = info
                                self.painter.drawLine(*start_freedomLine,*end_freedomLine)
                                end_freedomLine = start_freedomLine

                if self.mouse_info["isPitch"]:
                    self.painter.setPen(self.options["cu_open"])

        if self.mouse_info["isClick"]:
            if self.graphs.shape() in ["rect","ellipse"]:
                x, y = self.mouse_info["click_pos"].x(), self.mouse_info["click_pos"].y()
                w, h = self.mouse_info["cu_click"].x() - x, self.mouse_info["cu_click"].y() - y
                if self.graphs.shape() == "rect":
                    self.painter.drawRect(x,y,w,h)
                elif self.graphs.shape() == "ellipse":
                    self.painter.drawEllipse(x, y, w, h)
            elif self.graphs.shape() == "line":
                x1, y1 = self.mouse_info["click_pos"].x(), self.mouse_info["click_pos"].y()
                x2, y2 = self.mouse_info["cu_click"].x(), self.mouse_info["cu_click"].y()
                self.painter.drawLine(x1,y1,x2,y2)
        self.painter.end()