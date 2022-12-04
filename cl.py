
class CL1:
    
    def __init__(self) -> None:
        
        self._a = 555
        self._b = 1555
        
        pass
    
class CL2(CL1):
    
    def __init__(self) -> None:
        super().__init__()
        
    def test(self):
        return self._a + self._b
        

cl = CL1()
cll = CL2()
print(cll.test() )