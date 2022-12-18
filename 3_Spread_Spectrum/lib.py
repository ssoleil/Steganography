from PIL import Image
import numpy as np
from math import floor


# translate a digit from decimal system to binary system
def D_B(x, n):
    v = ''
    for i in range(n):
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


# correlation of two vectors (orthogonal signals have 0)
def ro(a, b):
    x = 0
    for i in range(len(b)):
        x += a[i] * b[i]
    return x


# evaluation of the decrypted message correctness
def v(a, b):
    v = 0
    for i in range(len(b)):
        if b[i] != a[i]:
            v += 1
    return v / len(b)


# the magnitude of the image distortion
def w(secret_img):
    w = 0
    height, width, p = np.array(secret_img).shape
    img = Image.open("tiger.bmp")
    for x in range(height):
        for y in range(width):
            w += abs(secret_img.getpixel((y, x))[0] - img.getpixel((y, x))[0])
    return (w * 100) / (height * width * 256)
