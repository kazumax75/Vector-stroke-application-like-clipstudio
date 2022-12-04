import itertools
import cv2
import numpy as np
import copy

import CatmullRomSpline as cmr

class EditableCatmullRomCurve(cmr.CatmullRomSpline):
    def __init__(self) -> None:
        super().__init__()
    
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
    
    
class CVInputManager:
    def __init__(self, img):
        self.img = img
        self.pt_list = []
        self.lb_flag = False
        self.rb_flag = False
        self.drag_point_idx = -1
        self.prev_pt = (0,0)
        self._points=[]
    
    def mouseCallback(self, event, x, y, flags, param):
        #########################################################################
        ##  左クリック
        #########################################################################
        if event == cv2.EVENT_LBUTTONDOWN:
            self.lb_flag = True
            
            self.img[y, x] = (0,0,255)
            self.prev_pt = (x,y)
            
            self.pt_list.clear()
            self.pt_list.append((x,y))
            
            cv2.imshow('image', self.img)
        elif event == cv2.EVENT_LBUTTONUP:
            self.lb_flag = False
            
            contour = np.array(self.pt_list, dtype = np.int32)
            
            epsilon = 0.001 * cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, epsilon, False)
            approx = np.squeeze(approx)
            
            for _x, _y in approx:
                cv2.circle(self.img,
                    center=(_x, _y),
                    radius=2,
                    color=(0, 255, 0),
                    thickness=-1,
                    lineType=cv2.LINE_4,
                    shift=0)
            
            self._points = list(np.squeeze(approx))
            
            # cmr = CatmullRomSpline()
            cmr.set(self._points)
            
            曲線を再描画する(self.img, cmr, 100)
        #########################################################################
        ##  右クリック
        #########################################################################
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.rb_flag = True
            self.drag_point_idx = cmr.近くの制御点のインデックス取得( (x,y) )
            
        elif event == cv2.EVENT_RBUTTONUP:
            self.rb_flag = False
            self.drag_point_idx = -1
        
        elif event == cv2.EVENT_MOUSEMOVE:
            #########################################################################
            ##  左ドラッグ中
            #########################################################################
            if self.lb_flag:
                self.pt_list.append((x,y))
                
                self.img[y, x] = (0,0,255)
                cv2.line(self.img, self.prev_pt, (x, y), (0, 0, 0), 1, 16)
                self.prev_pt = (x,y)
                
                pass
            #########################################################################
            ##  右ドラッグ中
            #########################################################################
            if self.rb_flag:
                
                if self.drag_point_idx > 0:
                    ret = cmr.movePoint( self.drag_point_idx, (x,y) )
                    曲線を再描画する(self.img, cmr, 100)
                    pass
                pass
            #########################################################################
            ##  ドラッグではなくマウスポインタ移動のみの時
            #########################################################################
            if self.lb_flag == False and self.rb_flag == False:
                idx = cmr.近くの制御点のインデックス取得( (x,y) )
            
                if idx == -1: return
                曲線を再描画する(self.img, cmr, 100)
                cv2.circle(self.img, radius=6, center=(cmr.points[idx][0], cmr.points[idx][1]) ,color=(0, 255, 255),thickness=-1,lineType=cv2.LINE_4,shift=0)
                pass
            
            pass  
    
    
    


img = np.zeros((800, 1080, 3), dtype=np.uint8)
img.fill(255)

cmr = EditableCatmullRomCurve()
ma = CVInputManager(img)

cv2.namedWindow('image')
cv2.setMouseCallback('image', ma.mouseCallback)


while(1):
    cv2.imshow('image', img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        pass
        
    elif key == ord('q'):
        break
    