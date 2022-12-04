import copy
import cv2
import numpy as np

class CatmullRomSpline:
    def __init__(self):
        self.points = None

    def set(self, pts):
        # self.points.clear()
        _points = []
        _points = copy.deepcopy(pts)
        _points.insert(0,  pts[0])
        _points.insert(-1, pts[-1])
        
        self.points = np.array(_points)
        
    def __calcVal(self, x0, x1, v0, v1, t):
        return (2.0 * x0 - 2.0 * x1 + v0 + v1) * t**3 + (-3.0 * x0 + 3.0 * x1 - 2.0 * v0 - v1) * t**2 + v0 * t + x0
    
    def __getValue(self, idx, t):
        if not 0 <= t <= 1.0: return 
        
        p1 = self.points[idx]
        p2 = self.points[idx+1]
        p3 = self.points[idx+2]
        p4 = self.points[idx+3]
        
        v0 = (p3 - p1) * 0.5
        v1 = (p4 - p2) * 0.5
        
        return (
            self.__calcVal(p2[0], p3[0], v0[0], v1[0], t),
            self.__calcVal(p2[1], p3[1], v0[1], v1[1], t),
        )
    
    def getKeyPoints(self):
        return self.points[1,-1]
        
    def plot(self, div): #補完した座標を返すジェネレータ
        length = len(self.points) - 2 - 1
        for i in range(length):
            for j in range(div):
                _p = self.__getValue(i, j / div)
                yield _p
                
