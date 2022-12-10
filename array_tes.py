import numpy as np
import pprint


a = np.frompyfunc(list, 0, 1)(np.empty((6, 8), dtype=object))

a[1, 2].append(5)
a[1, 2].append(5)
a[1, 2].append(5)
a[1, 2].append(5)


# print(a[0:3, 0:4])

print(
    np.ravel(a[0:3, 0:4])
)

for v in np.ravel(a[0:3, 0:4]):
    if not v: continue
    print(v)


# # a = np.zeros((3, 4, 2))
# b = np.zeros((3, 4, 4))
# # a = np.full((3, 4, 2), )
# # b = np.zeros((3, 4))
# # np.dtype

# # c = np.array([
# #     [[5,6], [5,6], [5,6]],
# #   


# arr = [
#     [1,2,3],
#     [11,12,13],
#     [21,22,23],
# ]

# print(arr[1:3][0])



# a = np.array([list([]), list([])], dtype=object) 
# a[0].append(555)
# print(a)

# # np.full((3, 4), [], dtype=object)

# # 3x3の右下の正方形となる４つをとり出したかったのですが



