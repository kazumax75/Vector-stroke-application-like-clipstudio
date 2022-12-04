import itertools
from re import A
import cv2
import numpy as np
import copy




class CatmullRomSpline:
    
    # class MyIterator(object):
    #     # イテレータ
    #     def __init__(self, points, length, division):
    #         self.points = points
    #         self.length = length
    #         self.division = division
    #         self.__i = 0

    #     def __iter__(self):
    #         # __next__()はselfが実装してるのでそのままselfを返す
    #         return self
            
    #     def __next__(self):  # Python2だと next(self) で定義
    #         if self._i >= self.length:
    #             raise StopIteration()
    #         # value = self._numbers[self._i]
    #         value = getValue(i, j / div)
    #         self._i += 1
    #         return value
    #     def getValue(self, idx, t):
    #         if not 0 <= t <= 1.0: return 
            
    #         p1 = self.__points[idx]
    #         p2 = self.__points[idx+1]
    #         p3 = self.__points[idx+2]
    #         p4 = self.__points[idx+3]
            
    #         v0 = (p3 - p1) * 0.5
    #         v1 = (p4 - p2) * 0.5
            
    #         return (
    #             self.calcVal(p2[0], p3[0], v0[0], v1[0], t),
    #             self.calcVal(p2[1], p3[1], v0[1], v1[1], t),
    #         )
        
    def __init__(self):
        self.points = None
        print("constoert")

    def set(self, pts):
        # self.points.clear()
        _points = []
        _points = copy.deepcopy(pts)
        _points.insert(0, pts[0])
        _points.insert(-1, pts[-1])
        
        self.points = np.array(_points)
        # self.iterator = self.MyIterator(5,6,7,8)
        
        # self.iterator = self.MyIterator(self.points, len(pts)-1, 100)
        
        
        # for i in range(len(pts) - 1):
            
            
        # for pt in keyPoints():
        #     img[pt[1], pt[0]] = (0,0,0)
            
        # for pt in interpolatPoints(div):
        #     img[pt[1], pt[0]] = (255,0,0)
        
        
        
        
        
        # for i in range(len(pts) - 1):
        #     div = 80 # 分割数
        #     for j in range(div):
        #         _p = cmr.getValue(i, j / div)
        #         # print("_p", _p[0])
        #         # print("_p", _p[1])
        #         img[int(_p[1]), int(_p[0])] = (255,0,0)
        
    def calcVal(self, x0, x1, v0, v1, t):
        return (2.0 * x0 - 2.0 * x1 + v0 + v1) * t**3 + (-3.0 * x0 + 3.0 * x1 - 2.0 * v0 - v1) * t**2 + v0 * t + x0
    
    def getValue(self, idx, t):
        if not 0 <= t <= 1.0: return 
        
        p1 = self.points[idx]
        p2 = self.points[idx+1]
        p3 = self.points[idx+2]
        p4 = self.points[idx+3]
        
        v0 = (p3 - p1) * 0.5
        v1 = (p4 - p2) * 0.5
        
        return (
            self.calcVal(p2[0], p3[0], v0[0], v1[0], t),
            self.calcVal(p2[1], p3[1], v0[1], v1[1], t),
        )
        
    
class EditableCatmullRomSpline(CatmullRomSpline):
    def __init__(self) -> None:
        super().__init__()
        
    
    def test(self):
        print(self.points)
        pass
    
    def dragPoint(self, pt):
        
        idx = self.近くの制御点のインデックス取得(pt)
        if idx == -1: return
        
        self.points[idx] = pt
        
        
    def 近くの制御点のインデックス取得(self, pt):
        if self.points is None: return -1
        
        for i, points in enumerate(self.points[1:-1]):
            distance = np.linalg.norm( np.array(pt) - points )
            # print(i, distance)
            if distance <= 10:
                print("match!!", i+1)
                return i + 1
        return -1
        
    
        

        # _points = self.points[1:-1]
        # _min = 1
        
        # for pt in _points:
            
        
        
        # return (_x, _y)
        
        
        
    

        
        
pt_list = []

lb_flag = False
rb_flag = False

prev_pt = (0,0)
def mouseCallback(event, x, y, flags, param):
    global img
    global lb_flag
    global prev_pt
    global pt_list
    global cmr
    global rb_flag
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print(param)
        lb_flag = True
        
        img[y, x] = (0,0,255)
        prev_pt = (x,y)
        
        pt_list.clear()
        pt_list.append((x,y))
        
        cv2.imshow('image', img)
        
        
    elif event == cv2.EVENT_MOUSEMOVE and lb_flag==True:
        
        img[y, x] = (0,0,255)
        cv2.line(img, prev_pt, (x, y), (0, 0, 0), 1, 16)
        prev_pt = (x,y)
        pt_list.append((x,y))
        
        pass
    elif event == cv2.EVENT_LBUTTONUP:
        lb_flag = False
        
        
        # approxPolyDP(
        # 			cv::Mat(line_pt), 
        # 			output_approx, 
        # 			EPSILON * cv::arcLength(line_pt, false),
        # 			false
        # 		);
        
        contour = np.array(
            pt_list,
            dtype = np.int32
        )
        # print(contour)
        
        # contour = np.array(
        # [
        #     [1, 2],
        #     [1, 4],
        #     [5, 4],
        #     [5, 2]
        # ],
        # dtype = np.int32
        # )
        # print(contour)
    
        
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

        # print("approx", np.squeeze(approx) )
        
        _points = list(np.squeeze(approx))
        # _points = pt_list
        
        # cmr = CatmullRomSpline()
        
        cmr.set(_points)
        cmr.test()
        
        # cmr.近くの制御点のインデックス取得( (0,0) )
        
       
        div = 80 # 分割数
        for i, j in itertools.product(range(len(_points)-1), range(div)): #Xの10通り、Yの10通りの全組み合わせ
            _p = cmr.getValue(i, j/div)
            img[int(_p[1]), int(_p[0])] = (255,0,0)
        # for num in cmr.iterator:
        #     print('hello %d' % num)

        
        # for i in range(len(pt_list) - 1):
        #     div = 80 # 分割数
        #     for j in range(div):
        #         _p = cmr.getValue(i, j / div)
        #         # print("_p", _p[0])
        #         # print("_p", _p[1])
        #         img[int(_p[1]), int(_p[0])] = (255,0,0)
                
        # for x, y in itertools.product(range(10), range(10)): #Xの10通り、Yの10通りの全組み合わせ

        
                
        
        
        
        
    elif event == cv2.EVENT_MOUSEMOVE and lb_flag==False:
        idx = cmr.近くの制御点のインデックス取得( (x,y) )
        
        if idx == -1: return
        
        print( cmr.points[idx] )
        
        
        # cv2.circle(img,
        #     center=(cmr.points[idx][0], cmr.points[idx][1]) ,
        #     radius=6,
        #     color=(0, 255, 255),
        #     thickness=-1,
        #     lineType=cv2.LINE_4,
        #     shift=0)
                
        
        pass
    
    
    elif event == cv2.EVENT_MOUSEMOVE and rb_flag==True:
        # ret = cmr.dragPoint( (x,y) )
        
        print("dragPoint")
        
        # cv2.circle(img,
        #     center=(cmr.points[idx][0], cmr.points[idx][1]) ,
        #     radius=6,
        #     color=(0, 255, 255),
        #     thickness=-1,
        #     lineType=cv2.LINE_4,
        #     shift=0)
                
        
        pass
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        rb_flag = True
        print("EVENT_RBUTTONDOWN")
        
        pass
    elif event == cv2.EVENT_RBUTTONUP:
        rb_flag = False
        pass
    
cmr = EditableCatmullRomSpline()
  
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouseCallback)

img = np.zeros((800, 1080, 3), dtype=np.uint8)
img += 255

while(1):
    cv2.imshow('image', img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        pass
        
    elif key == ord('q'):
        break
    