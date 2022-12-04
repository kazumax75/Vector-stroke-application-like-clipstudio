import itertools
import cv2
import numpy as np
import copy
from typing import List
import CatmullRomSpline as cmr
from typing import Tuple
import dataclasses
from abc import ABCMeta, abstractmethod

class EditableCatmullRomCurve(cmr.CatmullRomSpline):
    def __init__(self, pts) -> None:
        super().__init__(pts)
    
    def movePoint(self, idx, pt):
        self.points[idx] = pt
        return self.points[idx]
        
        
    def 近くの制御点のインデックス取得(self, pt):
        if self.points is None: return -1
        
        for i, points in enumerate(self.points[1:-1]):
            distance = np.linalg.norm( np.array(pt) - points )
            # print(i, distance)
            if distance <= 10:
                return i + 1
        return -1
    
def 曲線を再描画する(img, cmr, div):
    img.fill(255)
    for _p in cmr.plot(200):
        img[int(_p[1]), int(_p[0])] = (0,0,255)
    
class ILayer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, width, height) -> None:
        self.img = None
class ToolOperater(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, canvas) -> None:
        self.canvas = canvas
    @abstractmethod
    def LButtonDown(self): pass
    @abstractmethod
    def LButtonUp(self): pass
    @abstractmethod
    def LButtonMove(self):pass
    @abstractmethod
    def RButtonDown(self):pass
    @abstractmethod
    def RButtonUp(self):pass
    @abstractmethod
    def RButtonMove(self):pass
    @abstractmethod
    def mouseMove(self):pass
    
class Canvas:
    def __init__(self, width, height) -> None:
        self.width  = width
        self.height = height
        self.currentIdx = 0
        
        # self.guide_layer = self.__createLayer()
        self.layer: ILayer = []
        
        for i in range(1):
            self.layer.append( VectorLayer(self.width, self.height) )
        
        pass
    
    def getMat(self):
        # todo
        return self.layer[0].img
        
    def getCurrentLayer(self):
        return self.layer[self.currentIdx]
    
        
    
    

@dataclasses.dataclass
class Stroke:
    # curves: List[EditableCatmullRomCurve]
    curves: EditableCatmullRomCurve
    color: Tuple[int, int, int]
    thickness: int
class VectorLayer(ILayer):
    def __init__(self, width, height) -> None:
        self.img = np.zeros((height, width, 3), dtype=np.uint8)
        self.img.fill(255)
        
        self.temp_img = self.img.copy()
        self.Stroke = []
        

    
    
    def ベクター線の描画開始(self):
        self.temp_img = self.img.copy()
        
        
    def ベクター線の描画(self, pts, color, thickness):
        
        # 描画途中の線を消去した上で、改めてスプライン曲線を描画する。
        self.img = self.temp_img.copy()
        
        # _cmr = EditableCatmullRomCurve(pts)
        # self.Stroke.append( Stroke(_cmr, color, thickness) )
        
        # imgに実際に描画する
        
        # for _p in cmr.plot(200):
            # self.img[int(_p[1]), int(_p[0])] = (0,0,255)
            # cv2.circle(self.img,
            #         center=(_x, _y),
            #         radius=2,
            #         color=(0, 255, 0),
            #         thickness=-1,
            #         lineType=cv2.LINE_4,
            #         shift=0)
            # cv2.line(self.img, self.prev_pt, (x, y), (0, 0, 0), 1, 16)
        
        return 
        
    def removeCurve(self, idx):
        # self.Stroke.remove(idx)
        del self.Stroke[idx]
        return
    
# class StrokeManager:
    
#     def __init__(self) -> None:
#         self.pt = []
#         pass
    
#     def add(self, x, y):
#         self.pt.append(  (x, y) )
        

class VectorPen(ToolOperater):
    def __init__(self, canvas) -> None:
        super().__init__(canvas)
        # self.prev_pt = (0,0)
        
        self.color = (255, 0, 0)
        self.thickness = 1
        
        self.points = []
        
        
        pass
    
    def mouseMove(self, x, y):
        return
    
    def LButtonDown(self, x, y):
        self.canvas.getCurrentLayer().img[y, x] = (0,255,0)
        # self.prev_pt = (x, y)
        self.points.append((x, y))
        
        # self.canvas.getCurrentLayer().ベクター線の描画開始()
        return
        
    def LButtonMove(self, x, y):
        cv2.line(self.canvas.getCurrentLayer().img,
            pt1=self.points[-1],
            pt2=(x, y),
            color=self.color,
            thickness=self.thickness,
            lineType=cv2.LINE_4,
            shift=0)
        
        # self.prev_pt = (x, y)
        self.points.append((x, y))
        return

    def LButtonUp(self, x, y):
        
        
        print("pen lb Up")
        
        # self.canvas.getCurrentLayer().ベクター線の描画()
        
        cmr = EditableCatmullRomCurve(self.points)
        # self.Stroke.append( Stroke(_cmr, color, thickness) )
        
        # imgに実際に描画する
        
        for _p in cmr.plot(200):
            _x, _y = int(_p[0]), int(_p[1])
            self.canvas.getCurrentLayer().img[_y, _x] = (0,0,255)
            # cv2.circle(self.img,
            #         center=(_x, _y),
            #         radius=2,
            #         color=(0, 255, 0),
            #         thickness=-1,
            #         lineType=cv2.LINE_4,
            #         shift=0)
            # cv2.line(self.img, self.prev_pt, (x, y), (0, 0, 0), 1, 16)
        
        self.points.clear()
        
        return

    def RButtonDown(self, x, y):pass
    def RButtonUp(self, x, y):pass
    def RButtonMove(self, x, y):pass

# class CVInput(InputHandler):
class CVInput:
    def __init__(self, tool):
        # self.canvas: Canvas = canvas
        self.tool: ToolOperater = tool
        self.lb_flag = False
        self.rb_flag = False
    
    def callback(self, event, x, y, flags=None, param=None):
        if event == cv2.EVENT_LBUTTONDOWN: 
            self.lb_flag = True
            self.tool.LButtonDown(x, y)
            
        elif event == cv2.EVENT_LBUTTONUP and self.lb_flag :
            self.lb_flag = False
            self.tool.LButtonUp(x, y)
            
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.rb_flag = True
            self.tool.RButtonDown(x, y)
            
        elif event == cv2.EVENT_RBUTTONUP and self.rb_flag :
            self.rb_flag = False
            self.tool.RButtonUp(x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.lb_flag:
                self.tool.LButtonMove(x,y)
            elif self.rb_flag:
                self.tool.RButtonMove(x,y)
            if self.lb_flag == False and self.rb_flag == False:
                self.tool.mouseMove(x, y)



canvas = Canvas(1080, 800)
tool = VectorPen( canvas )
# ma = CVInput(canvas, tool)
ma = CVInput(tool)

cv2.namedWindow('image')
cv2.setMouseCallback('image', ma.callback)


while(1):
    # cv2.imshow('image', img)
    cv2.imshow('image', canvas.getMat() )
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        pass
        
    elif key == ord('q'):
        break
    
    
# 線をつまんで編集できる、CLIPSTUDIOのベクターレイヤーを実装する

# 