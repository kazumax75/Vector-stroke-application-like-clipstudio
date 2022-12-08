import itertools
import math
import cv2
import numpy as np
import copy
from typing import List
import CatmullRomSpline as cmr
from typing import Tuple
import dataclasses
from abc import ABCMeta, abstractmethod
    
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
    curve: cmr.CatmullRomSpline
    color: Tuple[int, int, int]
    thickness: int
    
@dataclasses.dataclass
class PointMap:
    curve_index: int
    points: List[Tuple[int, int]]
    
class VectorLayer(ILayer):
    def __init__(self, width, height) -> None:
        self.img = np.zeros((height, width, 3), dtype=np.uint8)
        self.img.fill(255)
        
        self.temp_img = self.img.copy()
        self.stroke = []
        
        
        rows = math.ceil(width / 10)
        cols = math.ceil(height / 10)
        
        print(rows, cols)

        self.map = [[ [] for j in range(cols)] for i in range(rows)]
        
        print("w", len(self.map))
        print("h", len(self.map[0]))
        # self.map[2][3] = 99
        # print("mamp",self.map)
        # print(  )
    
    # def addCurve(self, )
    
    
    def ベクター線の描画開始(self):
        self.temp_img = self.img.copy()
        
        
    def ベクター線の描画(self):
        # 描画途中の線を消去した上で、改めてスプライン曲線を描画する。
        self.img = self.temp_img.copy()
        return 
    
    def カーブを追加(self, stroke):
        # Stroke(curve, self.color, self.thickness)
        self.stroke.append(stroke)
        
        for pt in stroke.curve.getKeyPoints():
            _x = int(pt[0] / 10)
            _y = int(pt[1] / 10)
            
            self.map[_x][_y].append(
                PointMap( len(self.stroke)-1, pt )
            )
            
            
        
        
        return 
        
    def removeCurve(self, idx):
        # self.stroke.remove(idx)
        del self.stroke[idx]
        return
        
    def 近くの制御点のインデックス取得(self, pt):
        if not self.stroke: return -1
        
        for i, st in enumerate(self.stroke):
            
            
            pass
        
        # for i, points in enumerate(self.points[1:-1]):
        #     distance = np.linalg.norm( np.array(pt) - points )
        #     # print(i, distance)
        #     if distance <= 10:
        #         return i + 1
        # return -1
    
# class StrokeManager:
    
#     def __init__(self) -> None:
#         self.pt = []
#         pass
    
#     def add(self, x, y):
#         self.pt.append(  (x, y) )
        

class VectorPen(ToolOperater):
    def __init__(self, canvas) -> None:
        super().__init__(canvas)
        
        self.color = (23, 115, 255)
        self.thickness = 1
        
        self.points = []
        
        pass
    
    def setColor(self, color):
        self.color = color
        
    def setThickness(self, thickness):
        self.thickness = thickness
        
    # def 近くの制御点のインデックス取得(self, pt):
    #     if self.points is None: return -1
        
    #     for i, points in enumerate(self.points[1:-1]):
    #         distance = np.linalg.norm( np.array(pt) - points )
    #         # print(i, distance)
    #         if distance <= 10:
    #             return i + 1
    #     return -1
    
    def mouseMove(self, x, y):
        return
    
    def LButtonDown(self, x, y):
        # self.canvas.getCurrentLayer().img[y, x] = (0,255,0)
        
        cv2.circle(self.canvas.getCurrentLayer().img,
            center=(x, y),
            radius=1 ,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_4,
            shift=0)


        # self.prev_pt = (x, y)
        self.points.append((x, y))
        
        self.canvas.getCurrentLayer().ベクター線の描画開始()
        return
        
    def LButtonMove(self, x, y):
        cv2.line(self.canvas.getCurrentLayer().img,
            pt1=self.points[-1],
            pt2=(x, y),
            color=self.color,
            thickness=self.thickness,
            lineType=cv2.LINE_AA,
            shift=0)
        
        # self.prev_pt = (x, y)
        self.points.append((x, y))
        return

    def LButtonUp(self, x, y):
        cv2.line(self.canvas.getCurrentLayer().img,
            pt1=self.points[-1],
            pt2=(x, y),
            color=self.color,
            thickness=self.thickness,
            lineType=cv2.LINE_AA,
            shift=0)
        self.points.append((x, y))
        print("pen lb Up")
        
        self.canvas.getCurrentLayer().ベクター線の描画()
        
        # self.points[2] = (self.points[2][0]+50, self.points[2][0] - 12)
        
        # 間引きする
        contour = np.array(self.points, dtype = np.int32)
        
        epsilon = 0.0008 * cv2.arcLength(contour, False)
        approx = cv2.approxPolyDP(contour, epsilon, False)
        approx = np.squeeze(approx, 1)
        
        curve = cmr.CatmullRomSpline(approx.tolist())
        curve.getKeyPoints()
        
        px = py = 0
        for i, _p in enumerate(curve.plot(1), 0):
            # print(int(_p[0]), int(_p[1]))
            if i == 0:
                px, py = int(_p[0]), int(_p[1])
                continue
            # print(i)
            _x, _y = int(_p[0]), int(_p[1])
            # self.canvas.getCurrentLayer().img[_y, _x] = (0,0,255)
            # cv2.circle(self.img,
            #         center=(_x, _y),
            #         radius=2,
            #         color=(0, 255, 0),
            #         thickness=-1,
            #         lineType=cv2.LINE_4,
            #         shift=0)
            cv2.line(
                self.canvas.getCurrentLayer().img , 
                (px, py), 
                (_x, _y), 
                self.color, 
                # (255,9,0),
                thickness=self.thickness, 
                lineType=cv2.LINE_AA
            )
            px, py = int(_p[0]), int(_p[1])
            
            
            
        # debug 制御点表示
        # for pt in curve.getKeyPoints():cv2.circle(self.canvas.getCurrentLayer().img,center=(pt[0], pt[1]),radius=3,color=(0, 0, 0),thickness=1,lineType=cv2.LINE_4,shift=0)
        
        
        # self.canvas.getCurrentLayer().stroke.append( Stroke(curve, self.color, self.thickness) )
        self.canvas.getCurrentLayer().カーブを追加( Stroke(curve, self.color, self.thickness) )
        
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
    
    def mouseCallback(self, event, x, y, flags=None, param=None):
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

    def keyInput(self, ):
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            pass
            
        elif key == ord('q'):
            cv2.destroyAllWindows()
            exit()


canvas = Canvas(1080, 800)
tool = VectorPen( canvas )
# ma = CVInput(canvas, tool)
ma = CVInput(tool)

cv2.namedWindow('image')
cv2.setMouseCallback('image', ma.mouseCallback)


while(1):
    # cv2.imshow('image', img)
    cv2.imshow('image', canvas.getMat() )
    
    ma.keyInput()
    
# 線をつまんで編集できる、CLIPSTUDIOのベクターレイヤーを実装する

# 