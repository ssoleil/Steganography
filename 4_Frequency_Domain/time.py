from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from math import cos, ceil, pi
import time

img = np.array(Image.open("tiger.bmp"))
width, height = len(img[0]), len(img)
i = 0
sliced, sliced1 = [], []
block = 8

c = [0.707, 1, 1, 1, 1, 1, 1, 1]


def DCT(img):
    n = len(img)
    dct1 = 0
    dct = []
    for i in range(n):
        for j in range(n):
            sumd = 0
            for x in range(n):
                for y in range(n):
                    dct1 = img[x, y][0] * cos((2 * x + 1) * i * pi / (2 * n)) * cos((2 * y + 1) * j * pi / (2 * n))
                    sumd += dct1

            dct.append(sumd * (2 / n) * c[i] * c[j])
    return np.array(dct).reshape(n, n)


def IDCT(img):
    n = len(img)
    dct1 = 0
    idct = []

    for i in range(n):
        for j in range(n):
            sumd = 0
            for x in range(n):
                for y in range(n):
                    dct1 = (2 / n) * c[x] * c[y] * img[x, y] * cos((2 * i + 1) * x * pi / (2 * n)) * cos(
                        (2 * j + 1) * y * pi / (2 * n))
                    sumd += dct1
            idct.append(ceil(sumd))
    return np.array(idct).reshape(n, n)


y = 0
for i in range(block, height + 1, block):
    x = 0
    for j in range(block, width + 1, block):
        sliced.append(img[y:i, x:j])
        x = j
    y = i

y = 0
for i in range(block, height + 1, block):
    x = 0
    for j in range(block, width + 1, block):
        sliced1.append(img[y:i, x:j][0])
        x = j
    y = i

# cv2.dct requires float32 input
imf = [np.float32(img) for img in sliced1]

# --------------------------------------------------------------------------

print('Parameters: \n\timage - ', width, 'x', height, '\n\tblock size - ', block)

start_time = time.time()
dct_mtx = []
for part in sliced:
    dct_mtx.append(DCT(part))
print("--- DCT %s seconds ---" % (time.time() - start_time))

start_time = time.time()
idct_mtx = []
for part in dct_mtx:
    idct_mtx.append(IDCT(part))
print("--- IDCT %s seconds ---" % (time.time() - start_time))

print('-------------------------------------------------')

start_time = time.time()
DCT = []
for part in imf:
    curr = cv2.dct(part)
    DCT.append(curr)
print("--- DCT cv2 %s seconds ---" % (time.time() - start_time))

start_time = time.time()
invList = []
for ipart in DCT:
    curriDCT = cv2.idct(ipart)
    invList.append(curriDCT)
print("--- IDCT cv2 %s seconds ---" % (time.time() - start_time))

# --------------------------------------------------------------

dctt = [[x for x in range(1, 5)], [0] * 4, [0] * 4]
idctt = [[x for x in range(1, 5)], [0] * 4, [0] * 4]

idx = 1
with open('plot_dct.txt', 'r') as f:
    for eachLine in f:
        dctt[idx] = [float(x) for x in eachLine.split(',')]
        idx += 1

idx = 1
with open('plot_idct.txt', 'r') as f:
    for eachLine in f:
        idctt[idx] = [float(x) for x in eachLine.split(',')]
        idx += 1

plt.figure(figsize=(24, 30))

plt.subplot(2, 2, 1)
plt.plot(dctt[0], dctt[1])
plt.title('DCT', fontsize=15)
plt.ylabel('Seconds', fontsize=12, color='blue')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(dctt[0], dctt[2])
plt.title('DCT CV2', fontsize=15)
plt.xlabel('No of experiment', fontsize=12, color='blue')
plt.ylabel('Seconds', fontsize=12, color='blue')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(idctt[0], idctt[1])
plt.title('IDCT', fontsize=15)
plt.ylabel('Seconds', fontsize=12, color='blue')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(idctt[0], idctt[2])
plt.title('IDCT CV2', fontsize=15)
plt.xlabel('No of experiment', fontsize=12, color='blue')
plt.ylabel('Seconds', fontsize=12, color='blue')
plt.grid(True)
plt.show()
