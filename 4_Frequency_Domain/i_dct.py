from PIL import Image
import numpy as np
import math
from math import cos, ceil

img = np.array(Image.open("tiger.bmp"))
width, height = len(img[0]), len(img)
i = 0
sliced = []
block = 8

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

            dct.append(sumd * (2 / n) * c[i] * c[j])
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
            idct.append(ceil(sumd))
    return np.array(idct).reshape(n, n)


# divide an image into blocks
y = 0
for i in range(block, height + 1, block):
    x = 0
    for j in range(block, width + 1, block):
        sliced.append(img[y:i, x:j])
        x = j
    y = i

# do DCT for each image block
print('\nStarting DCT...\n')

dct_mtx = []
for part in sliced:
    dct_mtx.append(DCT(part))

print('DCT has finished.\n')

print('Transform DCT high-frequency coefficients by 1000%...\n')
for x in range(len(dct_mtx)):
    dct_mtx[x][7][7] = dct_mtx[x][7][7] * 10

# do IDCT for each transformed image block
print('Starting IDCT...\n')

idct_mtx = []
for part in dct_mtx:
    idct_mtx.append(IDCT(part))

print('The results are: input block \t DCT block \t IDCT block\n')
for i in range(8):
    print(sliced[0][i], '\t', np.array(dct_mtx[0][i]), '\t', idct_mtx[0][i])

# -----------------------------------------------------------------------
row = 0
rowNcol = []
for j in range(int(width / block), len(idct_mtx) + 1, int(width / block)):
    rowNcol.append(np.hstack((idct_mtx[row:j])))
    row = j
print("\nNumber of image blocks is ", len(idct_mtx))
res = np.vstack((rowNcol))

res_img = Image.fromarray(res)
if res_img.mode != 'RGB':
    res_img = res_img.convert('RGB')
res_img.save("dcthigh.bmp", "BMP")
