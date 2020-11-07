import ast
import binascii
import json
import struct
from urllib.request import urlretrieve
import os
import matplotlib.pyplot as plt
import numpy as np
import zlib

res = 1.7881393432617188e-07

def to_num(x):
    ret = x/res
    ret = int(round(ret))
    return ret

def from_num(x):
    ret = res*x
    return ret

def get_size(filename):
    f = open(filename, 'rb')
    f.seek(0, 2)  # Seek the end
    num_bytes = f.tell()  # Get the file size
    f.close
    return num_bytes

def compare_data(A, B):
    # compare dictionaries with real_data
    errors = 0
    errors += sum(i != j for i, j in zip(A['c1'], B['c1']))  # c1
    errors += sum(i > 1e-5 for i in abs(np.asarray(A['c2']) - np.asarray(B['c2'])))  # c2
    errors += sum(i != j for i, j in zip(A['c3'], B['c3']))  # c3
    errors += sum(i > 1e-5 for i in abs(np.asarray(A['c4']) - np.asarray(B['c4'])))  # c4
    errors += sum(i > 1e-2 for i in abs(np.asarray(A['c5']) - np.asarray(B['c5'])))  # c5
    errors += sum(i > 1e-5 for i in abs(np.asarray(A['c6']) - np.asarray(B['c6'])))  # c6
    errors += sum(i != j for i, j in zip(A['c7'], B['c7']))  # c7
    # print(errors)
    return errors


def compare_data_detail(A, B):
    # compare dictionaries with real_data
    errors = 0
    print('c1', sum(i != j for i, j in zip(A['c1'], B['c1'])))  # c1
    print('c2', sum(i > 1e-5 for i in abs(np.asarray(A['c2']) - np.asarray(B['c2']))))  # c2
    print('c3', sum(i != j for i, j in zip(A['c3'], B['c3'])))  # c3
    print('c4', sum(i > 1e-5 for i in abs(np.asarray(A['c4']) - np.asarray(B['c4']))))  # c4
    print('c5', sum(i > 1e-2 for i in abs(np.asarray(A['c5']) - np.asarray(B['c5']))))  # c5
    print('c6', sum(i > 1e-5 for i in abs(np.asarray(A['c6']) - np.asarray(B['c6']))))  # c6
    print('c7', sum(i != j for i, j in zip(A['c7'], B['c7'])))  # c7
    return compare_data(A, B)

def download(url, file):
    if not os.path.isfile(file):
        print("Download file... " + file + " ...")
        urlretrieve(url,file)
        print("File downloaded")

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

def compress(infile, outfile):
    data = load(infile)

    with open(outfile, "wb") as fout:
        for x in range(0,len(data['c1'])):
            compressed_c2 = to_num(data['c2'][x])
            compressed_c4 = to_num(data['c4'][x])

            c1_1 = np.uint8(compressed_c2>>16)
            c1_2 = np.uint8(compressed_c2>>8)
            c1_3 = np.uint8(compressed_c2)

            c2_1 = np.uint8(compressed_c4 >> 16)
            c2_2 = np.uint8(compressed_c4 >> 8)
            c2_3 = np.uint8(compressed_c4)

            fout.write(struct.pack('BBBBBB', c1_1, c1_2,c1_3,c2_1,c2_2,c2_3))

    return data


def get_color(f1,f2):
    colors = ['blue','green','yellow','red','magenta','green']
    color_num = 0
    if(f1<1):
        if(f2<1):
            color_num = 0
        if(f2>1):
            color_num = 3
    elif(f1>1 and f1<2):
        if(f2<1):
            color_num = 1
        if(f2>1):
            color_num = 4
    elif(f1>2):
        if(f2<1):
            color_num = 2
        if(f2>1):
            color_num = 5
    return color_num, colors[color_num]


def decompress(infile):
    fin = open(infile, "rb")
    ssize = struct.calcsize('BBBBBB')
    output = dict()
    output['c1'] = []
    output['c2'] = []
    output['c3'] = []
    output['c4'] = []
    output['c5'] = []
    output['c6'] = []
    output['c7'] = []
    counter = 0
    while True:
        data = fin.read(ssize)
        if data:
            values = struct.unpack('BBBBBB', data)


            c1 = from_num((values[0]<<16)+(values[1]<<8)+values[2])
            c2 = from_num((values[3]<<16)+(values[4]<<8)+values[5])

            #print values
            output['c1'].append(counter)
            output['c2'].append(c1)
            output['c4'].append(c2)
            output['c5'].append(c1/c2)
            output['c6'].append(c1+0.630245158737)
            color_num ,color = get_color(c1,c2)
            output['c3'].append(color)
            output['c7'].append(color_num)
            counter = counter+1
        else:
            # end of file (or corupted file)
            break
    fin.close()
    return output



# komprese
data = compress('demo-real-med.txt', 'demo-real-med.bin')



# dekomprese dat
out_data = decompress('demo-real-med.bin')

# vyhodocení
src_size = get_size('demo-real-med.txt')
bin_size = get_size('demo-real-med.bin')
num_err = compare_data(data, out_data)

print("Počet chyb: ", num_err)
print("Komprese:   ", src_size/bin_size)




