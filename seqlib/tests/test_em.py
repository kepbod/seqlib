
'''
Testing em.py
'''

import numpy as np
from seqlib.em import squarem


def iter_p(p, y):
    pnew = [0] * 3
    i = list(range(len(y)))
    zi = (p[0] * np.exp(-p[1]) * np.power(p[1], i) /
          (p[0] * np.exp(-p[1]) * np.power(p[1], i) +
           (1 - p[0]) * np.exp(-p[2]) * np.power(p[2], i)))
    pnew[0] = np.sum(y * zi) / np.sum(y)
    pnew[1] = np.sum(y * i * zi) / np.sum(y * zi)
    pnew[2] = np.sum(y * i * (1 - zi)) / np.sum(y * (1 - zi))
    return np.array(pnew)


def test_em():
    y = np.array([162, 267, 271, 185, 111, 61, 27, 8, 3, 1])
    p0 = np.array([0.73462845, 2.06566338, 1.38867049])
    p = squarem(p0, iter_p, y)
    p_final = np.array(list(round(x, 3) for x in p))
    p_correct = np.array([0.640, 2.663, 1.256])
    assert np.array_equal(p_final, p_correct)
