from abc import ABCMeta, abstractmethod
import cv2
import numpy as np

class InputHandler(metaclass=ABCMeta):
    def __init__(self, tool):
        self.tool = tool
        self.lb_flag = False
        self.rb_flag = False
    
    @abstractmethod
    def callback(self, event, x, y, flags=None, param=None):
        pass
    
    def setTool(self, tool):
        self.lb_flag = self.rb_flag = False
        self.tool = tool
    
class ToolOperater(metaclass=ABCMeta):
    @abstractmethod
    def LButtonDown(self):
        pass
    @abstractmethod
    def LButtonUp(self):
        pass
    @abstractmethod
    def LButtonMove(self):
        pass
    @abstractmethod
    def RButtonDown(self):
        pass
    @abstractmethod
    def RButtonUp(self):
        pass
    @abstractmethod
    def RButtonMove(self):
        pass
    @abstractmethod
    def mouseMove(self):
        pass
    
class ILayer(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, width, height) -> None:
        self.img = None
        
        
        pass
    
class IDraw(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, ) -> None:
        # self.img = None
        
        
        pass
    
    @abstractmethod
    def dot(self, img, x, y, size):
        pass
    @abstractmethod
    def line(self, img, x, y, color,size):
        pass
    @abstractmethod
    def circle(self, img, x, y, color, size):
        pass
    @abstractmethod
    def rectangle(self, img, x, y, color, size):
        pass
    
    
class CVDraw():
    def dot(self, img, pt, color):
        img[pt[1], pt[2]] = color
        pass
    
    def line(self, img, p1, p2, color, size):
        cv2.line(img,
            pt1=p1,
            pt2=p2,
            color=color,
            thickness=size,
            lineType=cv2.LINE_4,
            shift=0)
        pass
    
    def circle(self, img, pt, color, size):
        cv2.circle(img,
           center=pt,
           radius=size,
           color=color,
           thickness=-1,
           lineType=cv2.LINE_4,
           shift=0)
        
        pass
    def rectangle(self, img, p1, p2, color, size):
        cv2.rectangle(img,
              pt1=p1,
              pt2=p2,
              color=color,
              thickness=-1,
              lineType=cv2.LINE_4,
              shift=0)

    
class NomalLayer(ILayer):
    def __init__(self, width, height) -> None:
        self.img = np.zeros((height, width, 3), dtype=np.uint8)
        self.img.fill(255)
    
class VectorLayer(ILayer):
    def __init__(self, width, height) -> None:
        self.img = np.zeros((height, width, 3), dtype=np.uint8)
        self.img.fill(255)
        
        self.curves = []
        
    def addCurve(self, ):
        pass
    def removeCurve(self, idx):
        pass
    def addCurve(self, ):
        pass
        
#################################

class LayerManager:
    def __init__(self, width, height) -> None:
        self.topLevelLayer: ILayer = []
        self.layers: ILayer = []
        self.width = width
        self.height = height
        self.current_idx = 0
        
        # デフォルトの１枚目のレイヤー作成
        self.layers.append( NomalLayer(width, height) )
        pass
    
    def getCurrentLayer(self):
        return self.layers[ self.current_idx ]
    
    def addLayer(self, _layer):
        self.layers.append(_layer)
        
    def removeLayer(self, idx):
        self.layers.remove(idx)
    
    def show(self):
        #debug
        cv2.imshow('layer manager', self.layers[0].img)
    
    
class CVInput(InputHandler):
    def __init__(self, tool):
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
            if self.lb_flag:   self.tool.LButtonMove(x,y)
            elif self.rb_flag: self.tool.RButtonMove(x,y)
            if self.lb_flag == False and self.rb_flag == False:
                self.tool.mouseMove(x, y)
    
class Pen(ToolOperater):
    
    
    def __init__(self,) -> None:
        self.prev_pt = (0,0)
        pass
    
    def LButtonDown(self, x, y):
        global img
        img[y, x] = (255,0,0)
        self.prev_pt = (x, y)
        pass
    def LButtonMove(self, x, y):
        
        global img
        cv2.line(img,
            pt1=self.prev_pt,
            pt2=(x, y),
            color=(255, 0, 0),
            thickness=1,
            lineType=cv2.LINE_4,
            shift=0)
        self.prev_pt = (x, y)
        pass

    def LButtonUp(self, x, y):
        print("pen lb Up")
        pass

    

    def RButtonDown(self, x, y):
        pass

    def RButtonUp(self, x, y):
        pass

    def RButtonMove(self, x, y):
        pass

    def mouseMove(self, x, y):
        pass
    
class VectorPen(ToolOperater):
    
    
    def __init__(self,) -> None:
        self.prev_pt = (0,0)
        pass
    
    def mouseMove(self, x, y):
        pass
    
    def LButtonDown(self, x, y):
        global img
        img[y, x] = (255,0,0)
        self.prev_pt = (x, y)
        pass
    def LButtonMove(self, x, y):
        
        global img
        cv2.line(img,
            pt1=self.prev_pt,
            pt2=(x, y),
            color=(255, 0, 0),
            thickness=1,
            lineType=cv2.LINE_4,
            shift=0)
        self.prev_pt = (x, y)
        pass

    def LButtonUp(self, x, y):
        print("pen lb Up")
        
        pass

    

    def RButtonDown(self, x, y):
        pass

    def RButtonUp(self, x, y):
        pass

    def RButtonMove(self, x, y):
        pass

    

class Fill(ToolOperater):
    def LButtonDown(self, x, y):
        # print("Fill lb Down"
        global img
        _, newImg, _, _ = cv2.floodFill(
            img,
            mask=None,
            seedPoint=(x, y),
            newVal=(0, 0, 255), # red
            loDiff=(7,7,7),
            upDiff=(7,7,7),
            flags = 4 | 255 << 8,
        )
    
        pass

    def LButtonUp(self, x, y):
        # print("Fill lb Up")
        pass

    def LButtonMove(self, x, y):
        
        # print("Fill lb Drag")
        pass

    def RButtonDown(self, x, y):
        pass

    def RButtonUp(self, x, y):
        pass

    def RButtonMove(self, x, y):
        pass

    def mouseMove(self, x, y):
        pass
    pass
    

    
def main():
    global img
    
    layerManager: LayerManager = LayerManager(1280, 960)
    input: InputHandler = CVInput( Pen() )
    
    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', input.callback)
    img = np.zeros((800, 1080, 3), dtype=np.uint8)
    img.fill(255)
    
    while(1):
        cv2.imshow('image', img)
        
        layerManager.show()
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            
            input.setTool( Pen() )
            pass
        elif key == ord('v'):
            input.setTool( Fill() )
            pass
        # 終了
        elif key == ord('q'):
            break
    

if __name__ == '__main__':
    main()