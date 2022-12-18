import numpy as np
import math
from math import floor, cos


# translate a digit from decimal system to binary system
def D_B(x):
    v = ''
    for i in range(8):
        v += (str)(x % 2)
        x = floor(x / 2)
    return v


# translate a digit from binary system to decimal system
def B_D(binary):
    str1 = str(binary)
    decimal = 0
    for i in range(len(str1)):
        decimal = decimal + (int(str1[i]) * (2 ** i))
    return decimal


c = [0.707, 1, 1, 1, 1, 1, 1, 1]


# discrete cosine transform
def DCT(img):
    n = len(img)
    dct1 = 0
    dct = []
    for i in range(n):
        for j in range(n):
            sumd = 0
            for x in range(n):
                for y in range(n):
                    dct1 = img[x, y][0] * cos((2 * x + 1) * i * math.pi / (2 * n)) * cos(
                        (2 * y + 1) * j * math.pi / (2 * n))
                    sumd += dct1

            dct.append(int(sumd * (2 / n) * c[i] * c[j]))
    return np.array(dct).reshape(n, n)


# inverse discrete cosine transform
def IDCT(img):
    n = len(img)
    dct1 = 0
    idct = []

    for i in range(n):
        for j in range(n):
            sumd = 0
            for x in range(n):
                for y in range(n):
                    dct1 = (2 / n) * c[x] * c[y] * img[x, y] * cos((2 * i + 1) * x * math.pi / (2 * n)) * cos(
                        (2 * j + 1) * y * math.pi / (2 * n))
                    sumd += dct1
            idct.append(sumd)
    return np.array(idct).reshape(n, n)
