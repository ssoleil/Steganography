from PIL import Image
import numpy as np
from lib import D_B, B_D, v, w, ro
import matplotlib.pyplot as plt

img = Image.open("tiger.bmp")
height, width, p = np.array(img).shape

# open text file with the secret message, 
# write a list of ASCII symbols
# translate to the common binary string format
m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b, m_ba = '', []
for i in m_ascii:
    m_b += D_B(i, 8)

# ---------------------Hadamard's matrix----------------------------------

# parse the secret message according to the format "1/-1"
for i in m_b:
    if i == '0':
        m_ba.append(-1)
    elif i == '1':
        m_ba.append(1)

print("Encoded message is: ", m_ba[:100], '...')

# g stands for signal energy, increases the accuracy of the extraction
# k determines the number of information bits embedded in one fragment (in one line) of the container
k, g = 4, 2
# Hadamard's matrix size
n = 8
res, signals = 0, [0] * height

# initialize Hadamard's matrix
H = np.array([[1]])

# form Hadamard's matrix 256х256 (2^n = 2^8)
for i in range(0, n):
    H = np.vstack((np.hstack((H, H)), np.hstack((H, -H))))
print('\nFirst Hadamard.s row\n', H[1][:50], '\nSecond Hadamard.s row\n', H[2][:50])

# multiply by one of k discrete Walsh-Hadamard signals 
# including energy g 
for y in range(height):
    for j in range(k):
        res += g * (m_ba[k * y + j] * H[j + 1])
    signals[y] = res
    res = [0] * 256

print('\nCoding with complex discrete signals: (k = ', k, ', g = ', g, ')\n', signals[0])
print('\nThe len of signals is ', len(signals))

# --------------------encoding-----------------------------------

# summation of a red channel pixel with a previous discrete signal
for x in range(height):
    for y in range(len(signals[0])):
        pixel = list(img.getpixel((y, x)))
        pixel[0] = pixel[0] + signals[x][y]
        if pixel[0] > 255: pixel[0] = 255
        if pixel[0] < 0: pixel[0] = 0
        img.putpixel((y, x), tuple(pixel))
img.save("secret_img_WH.bmp", "BMP")

print('ro of hadamard mtx vectors should be 0. check res: ', ro(H[0], H[1]))
print('ro sign should equal +1 (256): ', ro(signals[0], H[1]))
print('ro sign should equal +1 (256): ', ro(signals[0], H[2]))
print('ro sign should equal -1 (-256): ', ro(signals[0], H[3]))
print('ro sign should equal +1 (256): ', ro(signals[0], H[4]))
print('ro sign should equal +1 (256): ', ro(signals[1], H[1]))

# --------------------decoding-----------------------------------

secret_img = Image.open("secret_img_WH.bmp")
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

# decoding by sign of correlation function calculated for 
# the current row and four signals from the Hadamard matrix
for i in range(height):
    for j in range(k):
        if ro(red[i], H[j + 1]) > 0:
            m_b1 += '1'
        elif ro(red[i], H[j + 1]) <= 0:
            m_b1 += '0'
print('\nComparing decoded and secret messages:\n', m_b1[:50], '\n', m_b[:50])

# ---------------------------------------------------------------------------

p0 = 0
for i in range(len(m_b1)):
    if m_b1[i] != m_b[i]:
        p0 += 1
    p0 = p0 / height
print("\nErrors: ", p0, ' with message length', len(m_b1))

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(m_b1), 8):
    tmp = m_b1[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_WH.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()

# -----------------------------------------------------------------
# calculate various metrics and build the plots

print('v: ', v(m_b, m_b1))
print('w: ', w(secret_img))

v_w_k = [[2 ** x for x in range(1, 7)], [0] * 6]
v_w_g = [[x for x in range(1, 5)], [0] * 4]

with open('v_w_k.txt', 'r') as f:
    for eachLine in f:
        v_w_k[1] = [float(x) for x in eachLine.split(',')]
        plt.plot(v_w_k[0], v_w_k[1])
        plt.show()

with open('v_w_g.txt', 'r') as f:
    for eachLine in f:
        v_w_g[1] = [float(x) for x in eachLine.split(',')]
        plt.plot(v_w_g[0], v_w_g[1])
        plt.show()
