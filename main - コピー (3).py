import itertools
import cv2
import numpy as np
import copy

import CatmullRomSpline as crm

class EditableCatmullRomCurve(crm.CatmullRomSpline):
    def __init__(self) -> None:
        super().__init__()
    
    def dragPoint(self, idx, pt):
        self.points[idx] = pt
        return self.points[idx]
        
        
    def 近くの制御点のインデックス取得(self, pt):
        if self.points is None: return -1
        
        for i, points in enumerate(self.points[1:-1]):
            distance = np.linalg.norm( np.array(pt) - points )
            # print(i, distance)
            if distance <= 10:
                # print("match!!", i+1)
                return i + 1
        return -1
    
def 曲線を再描画する(img, cmr, div):
    img.fill(255)
    for _p in cmr.plot(200):
        img[int(_p[1]), int(_p[0])] = (0,0,255)
    
        
pt_list = []
lb_flag = False
rb_flag = False
drag_point_idx = -1
prev_pt = (0,0)
_points=[]

def mouseCallback(event, x, y, flags, param):
    global img
    global lb_flag
    global prev_pt
    global pt_list
    global cmr
    global rb_flag
    global drag_point_idx
    global _points
    #########################################################################
    ##  左クリック
    #########################################################################
    if event == cv2.EVENT_LBUTTONDOWN:
        lb_flag = True
        
        img[y, x] = (0,0,255)
        prev_pt = (x,y)
        
        pt_list.clear()
        pt_list.append((x,y))
        
        cv2.imshow('image', img)
    elif event == cv2.EVENT_LBUTTONUP:
        lb_flag = False
        
        contour = np.array(pt_list, dtype = np.int32)
        
        epsilon = 0.001 * cv2.arcLength(contour, False)
        approx = cv2.approxPolyDP(contour, epsilon, False)
        approx = np.squeeze(approx)
        
        for _x, _y in approx:
            cv2.circle(img,
                center=(_x, _y),
                radius=2,
                color=(0, 255, 0),
                thickness=-1,
                lineType=cv2.LINE_4,
                shift=0)
        
        _points = list(np.squeeze(approx))
        
        # cmr = CatmullRomSpline()
        cmr.set(_points)
        
        曲線を再描画する(img, cmr, 100)
    #########################################################################
    ##  右クリック
    #########################################################################
    elif event == cv2.EVENT_RBUTTONDOWN:
        rb_flag = True
        drag_point_idx = cmr.近くの制御点のインデックス取得( (x,y) )
        
    elif event == cv2.EVENT_RBUTTONUP:
        rb_flag = False
        drag_point_idx = -1
    
    elif event == cv2.EVENT_MOUSEMOVE:
        #########################################################################
        ##  左ドラッグ中
        #########################################################################
        if lb_flag:
            pt_list.append((x,y))
            
            img[y, x] = (0,0,255)
            cv2.line(img, prev_pt, (x, y), (0, 0, 0), 1, 16)
            prev_pt = (x,y)
            
            pass
        #########################################################################
        ##  右ドラッグ中
        #########################################################################
        if rb_flag:
            
            if drag_point_idx > 0:
                ret = cmr.dragPoint( drag_point_idx, (x,y) )
                # print("dragPoint", ret)
                
                # div = 80 # 分割数
                # for i, j in itertools.product(range(len(_points)-1), range(div)): #Xの10通り、Yの10通りの全組み合わせ
                #     _p = cmr.getValue(i, j/div)
                #     img[int(_p[1]), int(_p[0])] = (255,0,0)
                曲線を再描画する(img, cmr, 100)
                pass
        
            
            
            # cv2.circle(img,center=(ret[0], ret[1]) ,radius=6,color=(0, 0, 255),thickness=-1,lineType=cv2.LINE_4,shift=0)
            pass
        #########################################################################
        ##  ドラッグしない
        #########################################################################
        if lb_flag == False and rb_flag == False:
            idx = cmr.近くの制御点のインデックス取得( (x,y) )
        
            if idx == -1: return
            
            
            # print( cmr.points[idx] )
            
            曲線を再描画する(img, cmr, 100)
            cv2.circle(img,radius=6, center=(cmr.points[idx][0], cmr.points[idx][1]) ,color=(0, 255, 255),thickness=-1,lineType=cv2.LINE_4,shift=0)
            pass
        
        
        pass


    
    
    
    

cmr = EditableCatmullRomCurve()

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouseCallback)

img = np.zeros((800, 1080, 3), dtype=np.uint8)
img.fill(255)

while(1):
    cv2.imshow('image', img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        pass
        
    elif key == ord('q'):
        break
    