from PIL import Image
import numpy as np
from lib import D_B, B_D, DCT, IDCT

img = np.array(Image.open("tiger.bmp"))
width, height = len(img[0]), len(img)

sliced = []
# number of blocks
block = 8
# certain positive value - threshold - for encoding and decoding
pr = 10

c = [0.707, 1, 1, 1, 1, 1, 1, 1]

m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = ''
for i in m_ascii:
    m_b += D_B(i)
print("Encoded message is " + m_b[:100] + '...')

# divide an image into blocks
y = 0
for i in range(block, height + 1, block):
    x = 0
    for j in range(block, width + 1, block):
        sliced.append(img[y:i, x:j])
        x = j
    y = i


# value replacement rule for coefficients difference
# pr specifies a sufficient value of difference between the DCT coefficients
def h(h1, h2):
    tmp = abs(h1) - abs(h2)
    if tmp > pr:
        return 1
    elif tmp < (-pr):
        return 0
    elif (-pr) <= tmp <= pr:
        return -1


# basic rule for modifying the coefficients according to the embedded bit
def output(mtx8x8, m1):
    # print('abs of 8x8')
    # print(abs(mtx8x8[3][1]), abs(mtx8x8[1][3]))
    if m1 == '1' and h(mtx8x8[3][1], mtx8x8[1][3]) != m1:
        if mtx8x8[3][1] > 0:
            mtx8x8[3][1] = abs(mtx8x8[1][3]) + pr
        elif mtx8x8[3][1] <= 0:
            mtx8x8[3][1] = -(abs(mtx8x8[1][3])) - pr
    if m1 == '0' and h(mtx8x8[3][1], mtx8x8[1][3]) != m1:
        if mtx8x8[1][3] > 0:
            mtx8x8[1][3] = abs(mtx8x8[3][1]) + pr
        elif mtx8x8[1][3] <= 0:
            mtx8x8[1][3] = -(abs(mtx8x8[3][1])) - pr
    return mtx8x8


def encode(mtx, m):
    idx = 0
    mtx1 = []
    for y in range(len(mtx)):
        if idx >= len(m) - 1: break
        mtx1.append(output(mtx[y], m[idx]))
        idx += 1
    return mtx1


# -------------------------------------------------------
# do DCT for each image block
print('\nStarting DCT...\n')

dct_mtx = []
for part in sliced:
    dct_mtx.append(DCT(part))

print('DCT has finished.\n')

# ----------------------encoding----------------------
# print(dct_mtx[1])
dct_mtx = encode(dct_mtx, m_b)
# print(dct_mtx[1])

# -------------------------------------------------------
# do IDCT for each transformed image block
print('Starting IDCT...\n')

idct_mtx = []
for part in dct_mtx:
    idct_mtx.append(IDCT(part))

row = 0
rowNcol = []
for j in range(int(width / block), len(idct_mtx) + 1, int(width / block)):
    rowNcol.append(np.hstack((idct_mtx[row:j])))
    row = j
res = np.vstack((rowNcol))

# processing an array of blocks into an image
res_img = Image.fromarray(res)
if res_img.mode != 'RGB':
    res_img = res_img.convert('RGB')
res_img.save("secret_img_KZ.bmp", "BMP")

# -----------------------------------------------------------------------
clear_img = Image.open("tiger.bmp")
secret_img = Image.open("secret_img_KZ.bmp")
diff = 0
for x in range(width):
    for y in range(height):
        pixel2 = list(clear_img.getpixel((x, y)))[0]
        pixel1 = list(secret_img.getpixel((x, y)))[0]
        diff += abs(pixel1 - pixel2)
    diff = diff / (height * width)
print('Difference between red channels: ', diff)

# -----------------------------------------------------------------------
secret_img = np.array(secret_img)
sliced = []
y = 0
for i in range(block, height + 1, block):
    x = 0
    for j in range(block, width + 1, block):
        sliced.append(secret_img[y:i, x:j])
        x = j
    y = i

print('\nStarting DCT...\n')

dct_mtx1 = []
for part in sliced:
    dct_mtx1.append(DCT(part))

print('DCT has finished.\n')

# ----------------------decoding----------------------

m_b1 = ''
for y in range(len(dct_mtx1)):
    if abs(dct_mtx1[y][3][1]) > abs(dct_mtx1[y][1][3]):
        m_b1 += '1'
    if abs(dct_mtx1[y][3][1]) <= abs(dct_mtx1[y][1][3]):
        m_b1 += '0'

print('Decoded message is: ' + m_b1[:100] + '...')

p0 = 0
for i in range(len(m_b1)):
    if m_b1[i] != m_b[i]:
        p0 += 1
    p0 = p0 / len(m_b)
print("Errors in message extracting: ", p0)

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(m_b1), 8):
    tmp = m_b1[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_KZ.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
