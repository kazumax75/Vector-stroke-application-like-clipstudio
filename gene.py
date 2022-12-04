


        
# def gen_combinations(n):
#     v = 1
#     for k in range(n+1):
#         yield v
#         v *= (n-k)
#         v //= (k+1)
# def gen_combinations(n):
#     v = 5
#     for k in range(n):
#         yield k + v

def gen_combinations(n, m):
    v = 5
    for i in range(v):
        for k in range(m):
            yield k

s = 0
for v in gen_combinations(1, 6):
    print(v)
    s += 1

print("x", s)

# class CL:
#     def __init__(self) -> None:
#         self.length = 7
        
    
#     def genei(div):
#         for
    
# for pt in 