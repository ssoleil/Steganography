from PIL import Image
import numpy as np
from math import ceil
from random import randrange
from lib import D_B, B_D, ro, v, w
import matplotlib.pyplot as plt

img = Image.open("tiger.bmp")
height, width, p = np.array(img).shape

# open text file with the secret message, 
# write a list of ASCII symbols
# translate to the common binary string format
m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b, m_ba, m_b10 = '', [], []
for i in m_ascii:
    m_b += D_B(i, 8)

# parse the secret message according to the format "1/-1"
for i in m_b:
    if i == '0':
        m_ba.append(-1)
    elif i == '1':
        m_ba.append(1)
print("Encoded message is: ", m_ba[:100], '...\n')

# ------------------------------------------------------------

# generation of pseudorandom quasi-orthogonal signals
quasi = [[0] * 256] * 2047
tmp = [0] * 256
for i in range(2047):
    for j in range(256):
        b = ceil(randrange(0, 2))
        if b == 0: tmp[j] = -1
        if b == 1:  tmp[j] = 1
    quasi[i] = tmp
    tmp = [0] * 256
print("Quasi: ", np.array(quasi))
print("The ro of quasi-orthogonal signals is: ", ro(quasi[0], quasi[1]))

# split message by 9 bits and translate to decimal system
for i in range(1, len(m_b), 9):
    tmp = m_b[i - 1:i + 9]
    m_b10.append(B_D(tmp))
print("\nChanged message: ", m_b10[:50], '...\n')

# --------------------encoding--------------------------------

signals = []
# increase the signals energy
g = 40
for y in range(height):
    signals.append([g * x for x in quasi[m_b10[y]]])

# print(np.array(signals).shape)
# print(signals[0][:50])

for x in range(height):
    for y in range(len(signals[0])):
        pixel = list(img.getpixel((y, x)))
        pixel[0] = pixel[0] + signals[x][y]
        if pixel[0] > 255: pixel[0] = 255
        if pixel[0] < 0: pixel[0] = 0
        img.putpixel((y, x), tuple(pixel))
img.save("secret_img_quasi.bmp", "BMP")

# --------------------decoding--------------------------------

secret_img = Image.open("secret_img_quasi.bmp")
width, height = secret_img.size
red, tmp = [[0] * height] * 256, [0] * 256
m_b1 = ''

# pre-save red pixels
for x in range(height):
    for y in range(len(signals[0])):
        pixel = list(img.getpixel((y, x)))
        tmp[y] = pixel[0]
    red[x] = tmp
    tmp = [0] * 256

# determine with which of the quasi-orthogonal signals 
# the row has the highest correlation, save its index
m_b10_1, a = [0] * height, 0
for i in range(height):
    for j in range(2047):
        if ro(red[i], quasi[j]) > a:
            a = ro(red[i], quasi[j])
            m_b10_1[i] = j
    a = 0
print('\nDecoded message is ', m_b10_1[:50])

res = ''
for i in m_b10_1:
    res += D_B(i, 9)
print('\nDecoded bits: ', res[:50])
print('Plain bits: ', m_b[:50])

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(res), 8):
    tmp = res[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_quasi.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()

# ---------------------------------------------------------------------------
# calculate various metrics and build the plots

print('\nv: ', v(m_b10, m_b10_1))
print('w: ', w(secret_img))

v_w_k = [[5 * x for x in range(0, 9)], [0] * 9]

with open('v_w_quasi.txt', 'r') as f:
    for eachLine in f:
        v_w_k[1] = [float(x) for x in eachLine.split(',')]
        plt.plot(v_w_k[0], v_w_k[1])
        plt.show()
