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
        self.prev_img = self.img.copy()
        self.stroke = []
        
        rows = width
        cols = height
        self.map = [[ [] for j in range(cols)] for i in range(rows)]
        
        self.selected_key_point = None
        print("w", len(self.map))
        print("h", len(self.map[0]))
    
    def 現在のイメージを記録する(self):
        self.temp_img = self.img.copy()
        
    def 線の描画前のイメージに戻す(self):
        self.img = self.temp_img.copy()
    
    def カーブを追加(self, stroke):
        self.stroke.append(stroke)
        for pt in stroke.curve.getKeyPoints():
            self.map[pt[0]][pt[1]].append( PointMap( len(self.stroke)-1, pt)  )
            
        return
        
    def 入力座標近くの制御点とカーブを取得(self, x, y):
        
        for i, st in enumerate(self.stroke):
            for j, pt in enumerate(st.curve.getKeyPoints()):
                distance = np.linalg.norm( np.array(pt) - np.array((x,y)) )
                if distance <= 10:
                    self.線の描画前のイメージに戻す()
                    self.制御点を表示する()
                    self.selected_key_point = [i, j]
                    
                    # print(self.selected_key_point)
                    
                    cv2.circle(
                        self.img,
                        center=(pt[0], pt[1]),
                        radius=5,color=(0, 0, 0),thickness=-1,lineType=cv2.LINE_4,shift=0)
                    
                    return 
        self.線の描画前のイメージに戻す()
        self.制御点を表示する()
        self.selected_key_point = None
        
        return 
    def 選択中のカーブ制御点を移動する(self, x, y):
        if not self.selected_key_point: return 
        if self.selected_key_point is None: return 
        
        # todo 最初、末尾の点は、別途処理がいる

        self.stroke[self.selected_key_point[0]].curve.points[self.selected_key_point[1] + 1] = [x, y]
        
    def removeCurve(self, idx):
        del self.stroke[idx]
        return
        
    def 全ストローク再描画(self, div=100):
        self.img.fill(255)
        for st in self.stroke:
            
            for i, _p in enumerate(st.curve.plot(div), 0):
                if i == 0:
                    px, py = int(_p[0]), int(_p[1])
                    continue
                
                _x, _y = int(_p[0]), int(_p[1])
                cv2.line(
                    self.img , 
                    (px, py), 
                    (_x, _y), 
                    st.color,
                    # (255,0,0),
                    thickness=st.thickness, 
                    lineType=cv2.LINE_AA)
                px, py = int(_p[0]), int(_p[1])
        self.制御点を表示する()
        
    def 制御点を表示する(self):
        
        for st in self.stroke:
            for pt in st.curve.getKeyPoints():
                cv2.circle(
                    self.img,
                    center=(pt[0], pt[1]),
                    radius=3,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4,
                    shift=0
                )

class VectorPen(ToolOperater):
    def __init__(self, canvas) -> None:
        super().__init__(canvas)
        
        self.color = (23, 115, 255)
        self.thickness = 1
        self.points = []
        self.selectable_key_point = True
    
    def setColor(self, color):
        self.color = color
        
    def setThickness(self, thickness):
        self.thickness = thickness
        
    def mouseMove(self, x, y):
        if not self.selectable_key_point: return
        
        self.canvas.getCurrentLayer().入力座標近くの制御点とカーブを取得(x, y)
        return
    
    def LButtonDown(self, x, y):
        cv2.circle(self.canvas.getCurrentLayer().img,
            center=(x, y),
            radius=1 ,
            color=self.color,
            thickness=-1,
            lineType=cv2.LINE_4,
            shift=0)
            
        self.points.append((x, y))
        
        return
        
    def LButtonMove(self, x, y):
        cv2.line(self.canvas.getCurrentLayer().img,
            pt1=self.points[-1],
            pt2=(x, y),
            color=self.color,
            thickness=self.thickness,
            lineType=cv2.LINE_AA,
            shift=0)
            
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
        
        # 直前の画像に戻す。未確定の線を消した上でカーブの描画を行うため
        self.canvas.getCurrentLayer().線の描画前のイメージに戻す()
        
        # self.points[2] = (self.points[2][0]+50, self.points[2][0] - 12)
        
        # 間引きする
        contour = np.array(self.points, dtype = np.int32)
        
        epsilon = 0.0018 * cv2.arcLength(contour, False)
        # epsilon = 0.0008 * cv2.arcLength(contour, False)
        approx = cv2.approxPolyDP(contour, epsilon, False)
        approx = np.squeeze(approx, 1)
        
        curve = cmr.CatmullRomSpline(approx.tolist())
        curve.getKeyPoints()
        
        px = py = 0
        for i, _p in enumerate(curve.plot(100), 0):
            if i == 0:
                px, py = int(_p[0]), int(_p[1])
                continue
            _x, _y = int(_p[0]), int(_p[1])
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
            
            
        self.canvas.getCurrentLayer().現在のイメージを記録する()
        # # debug 制御点表示
        # for pt in curve.getKeyPoints():cv2.circle(self.canvas.getCurrentLayer().img,center=(pt[0], pt[1]),radius=3,color=(0, 0, 0),thickness=1,lineType=cv2.LINE_4,shift=0)
        
        
        # self.canvas.getCurrentLayer().stroke.append( Stroke(curve, self.color, self.thickness) )
        self.canvas.getCurrentLayer().カーブを追加( Stroke(curve, self.color, self.thickness) )
        self.canvas.getCurrentLayer().制御点を表示する()
        
        self.points.clear()
        
        return
        
    
    def RButtonDown(self, x, y):
        # self.canvas.getCurrentLayer().線の描画前のイメージに戻す()
        # self.canvas.getCurrentLayer().選択中のカーブ制御点を移動する(x, y)
        # self.canvas.getCurrentLayer().全ストローク再描画()

        pass
    
    def RButtonMove(self, x, y):
        # self.canvas.getCurrentLayer().線の描画前のイメージに戻す()
        self.canvas.getCurrentLayer().選択中のカーブ制御点を移動する(x, y)
        self.canvas.getCurrentLayer().全ストローク再描画(div=7)
        
        pass
    def RButtonUp(self, x, y):
        self.canvas.getCurrentLayer().全ストローク再描画()
        self.canvas.getCurrentLayer().現在のイメージを記録する()
        
        pass
    
    
    def keyInput(self, key):
        if key == ord('c'):
            self.selectable_key_point = not self.selectable_key_point
            
            print("bole", self.selectable_key_point)
            pass
        elif key == ord('w'):
            
            self.canvas.getCurrentLayer().全ストローク再描画()
            pass
        
        elif key == ord('q'):
            pass
        
        

# class CVInput(InputHandler):
class CVInput:
    def __init__(self, tool):
        # self.canvas: Canvas = canvas
        self.tool: ToolOperater = tool
        self.lb_flag = False
        self.rb_flag = False
    
    def mouseCallback(self, event, x, y, flags=None, param=None):
        if not 0 <= x < self.tool.canvas.width  : return 
        if not 0 <= y < self.tool.canvas.height : return 
            
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
        
        self.tool.keyInput(key)
        
        if key == ord('c'):
            pass
            
        elif key == ord('q'):
            cv2.destroyAllWindows()
            exit()


canvas = Canvas(1080, 800)
tool = VectorPen( canvas )
ma = CVInput(tool)

cv2.namedWindow('image')
cv2.setMouseCallback('image', ma.mouseCallback)


while(1):
    # cv2.imshow('image', img)
    cv2.imshow('image', canvas.getMat() )
    
    ma.keyInput()
    
# 線をつまんで編集できる、CLIPSTUDIOのベクターレイヤーを実装する

# 