import numpy as np

def intr(s):
    global s1, s2, int_c, int_r, int_i, a, l
    if int_i == -1:
        int_i += 1
        return
    print(int_i, int_c, int_r)
    print(res)
    lv = list(s)
    s2 += ''.join([lv.pop(ind) for ind in l])
    s1 += ''.join(lv)
    if int_i < (a.shape[2] - 1): int_i += 1
    else:
        print('Write')
        res[int_r, int_c] = s1 + s2
        s1, s2 = '', ''
        int_i = 0
        if int_c < (a.shape[1] - 1): int_c += 1
        else:
            int_c = 0
            int_r += 1
    return
def srs(s, i):
    global sres
    sres += s[i]
    return

a = np.array([[['000', '001'], ['010', '011']], [['100', '101'], ['110', '111']], [['200', '201'], ['210', '211']]])
# a = np.array([[['1123', '1456'], ['123', '456']], [['123', '456'], ['123', '456']], [['123', '456'], ['123', '456']]])
res = np.full(a.shape[:2], fill_value = ('-' * 6))
l = [2]
int_r, int_c, int_i = 0, 0, -1
s1, s2 = '', ''
np.vectorize(lambda s: intr(s))(a)
lres = []
for r in res:
    lc = []
    for i in range(6):
        sres = ''
        np.vectorize(lambda sc: srs(sc, i))(r)
        lc.append(sres[1:])
    lres.append(lc)
nres = np.array(lres)
print(nres)
