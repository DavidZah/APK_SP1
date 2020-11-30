from math import floor
import numpy as np
import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve
import ctypes
from sys import getsizeof

from numcompress import compress, decompress






def load(infile):
    data = {}
    data['c1'] = []
    data['c2'] = []
    data['c3'] = []
    data['c4'] = []
    data['c5'] = []
    data['c6'] = []
    data['c7'] = []
    fin = open(infile, "rt")
    for line in fin:
        #check for free or corupted line, remove comments
        values = line.split()
        #check for free or corupted line, remove comments
        data['c1'].append(int(values[0]) )
        data['c2'].append(float(values[1]) )
        data['c3'].append(values[2] )
        data['c4'].append(float(values[3]) )
        data['c5'].append(float(values[4]) )
        data['c6'].append(float(values[5]) )
        data['c7'].append(int(values[6]) )
        #print int(values[0]), len(data['c1'])
    fin.close()
    return data

res = 0.0000000000001
distance = 0
last_distance = 0

def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)

def match(arr_x,arr_y,x_f,y_f):
    x_true = indices(arr_x,x_f)
    y_true = indices(arr_y,y_f)
    if(len(x_true) and len(y_true)):
        print("find")
    return False


x1 = np.linspace(0, 2, 15, endpoint = True)

data = load('demo-real-small.txt')
arr = data['c2']
arr2 = data['c4']

oper_arr = []
oper_arr_2 = []
for x in arr:
    oper_arr.append(int(x*10000000000000))

for x in arr2:
    oper_arr_2.append(int(x*10000000000000))


deltas = []
deltas_2 = []

for x in range(0,len(oper_arr)-1):
    deltas.append(oper_arr[x]-oper_arr[x+1])

for x in range(0,len(oper_arr_2)-1):
    deltas_2.append(oper_arr_2[x]-oper_arr_2[x+1])

arr_pow = []
arr2_pow = []

deltas.sort()
deltas_2.sort()
#arr.sort()


plt.plot(deltas_2,deltas,'bo')
print(bin(ctypes.c_uint.from_buffer(ctypes.c_float(oper_arr[len(deltas)-1])).value))
plt.ylabel('some numbers')
plt.show()

"""
def arry_to_one(arry,arrx):
    for x in arry:
        arrx.append(x)
    return arrx

data = load("demo-real-med.txt")


arr = arry_to_one(data['c2'],data['c4'])
print(len(arr))

x = compress(arr,precision=8)
print(getsizeof(x))
print(getsizeof(arr))
"""
