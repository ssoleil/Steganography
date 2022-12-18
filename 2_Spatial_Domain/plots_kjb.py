from PIL import Image
import numpy as np
from math import floor
import matplotlib.pyplot as plt

img = Image.open("tiger.bmp")
width, height = img.size
i = 0
delta, gama = 0, 3
m_b1, b1 = '', 0


def bright(x, y):
    return img.getpixel((x, y))[0] * 0.2989 + img.getpixel((x, y))[1] * 0.58662 + img.getpixel((x, y))[2] * 0.11448


def SV(x, y, b, d):
    return round(img.getpixel((x, y))[2] + (2 * b - 1) * d * bright(x, y))


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


m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = ''
for i in m_ascii:
    m_b += D_B(i)


def encode(d):
    for i in range(gama, height - gama):
        b = SV(i, i, int(m_b[i - gama]), d)
        pixel = list(img.getpixel((i, i)))
        if 0 <= b <= 255:
            pixel[2] = b
        elif b > 255:
            pixel[2] = 255
        elif b < 0:
            pixel[2] = 0
        img.putpixel((i, i), tuple(pixel))
    img.save("secret_img_kjb.bmp", "BMP")


def decode():
    secret_img = Image.open("secret_img_kjb.bmp")
    width, height = secret_img.size
    global m_b1
    m_b1 = ''
    for y in range(gama, height - gama):
        tmp = 0
        for i in range(y - gama, y):
            tmp += secret_img.getpixel((y, i))[2]
        for i in range(y - gama, y):
            tmp += secret_img.getpixel((i, y))[2]
        for i in range(y + 1, y + gama + 1):
            tmp += secret_img.getpixel((y, i))[2]
        for i in range(y + 1, y + gama + 1):
            tmp += secret_img.getpixel((i, y))[2]

        b1 = tmp / (4 * gama)

        if b1 < secret_img.getpixel((y, y))[2]:
            m_b1 += '1'
        elif b1 > secret_img.getpixel((y, y))[2]:
            m_b1 += '0'
    return secret_img


def v():
    v = 0
    for i in range(len(m_b1)):
        if m_b1[i] == m_b[i]:
            v += 1
    return v / len(m_b1)


def w(secret_img):
    w = 0
    img = Image.open("tiger.bmp")
    for i in range(gama, height - gama):
        w += abs(secret_img.getpixel((i, i))[2] - img.getpixel((i, i))[2])

    return (w * 100) / (len(m_b1) * 256)


vv = list(list())
ww = list(list())

# fill the array with different metrics of coding
for delta in np.arange(0.01, 1, 0.05):
    encode(delta)
    s_img = decode()
    vv.append([delta, v()])
    ww.append([delta, w(s_img)])

# rotate the 2d array by 90 degrees
vv = list(zip(*vv))
ww = list(zip(*ww))
print(vv)
print(ww)

# build plots
plt.plot(vv[0], vv[1])
plt.show()
plt.plot(ww[0], ww[1])
plt.show()
plt.plot(vv[1], ww[1])
plt.show()
