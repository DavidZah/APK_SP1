res = 1.7881393432617188e-07

def to_num(x):
    ret = x/res
    return ret

def from_num(x):
    ret = res*x
    return ret

x = 0.1809189643531
y = to_num(x)

y = int(round(y))

print(from_num(y))