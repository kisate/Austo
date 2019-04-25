def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[2], b[2])
    h = min(a[3], b[3])
    if w<0 or h<0: return (0, 0, 0, 0)
    return (x, y, w, h)

def area(a):
    return (a[2] - a[0]) * (a[3] - a[1])

def midOfRect(r):
    return ( int((r[3] + r[1]) * 640) // 2, int((r[2] + r[0]) * 480) // 2)

