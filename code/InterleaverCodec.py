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

# a = np.array([[['000', '001'], ['010', '011']], [['100', '101'], ['110', '111']], [['200', '201'], ['210', '211']]])
a = np.array([[['123', '456'], ['123', '456']], [['456', '456'], ['123', '456']], [['123', '456'], ['123', '456']]])
res = np.full(a.shape[:2], fill_value = ('-' * 6))
list_of_correction_bit_positions = [0, 1, 3, 7]
int_r, int_c, int_i = 0, 0, -1
s1, s2 = '', ''
np.vectorize(lambda s: intr(s))(a)
print(res)
