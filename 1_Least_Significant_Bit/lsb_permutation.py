from PIL import Image
from math import floor
import numpy as np

img = Image.open("tiger.bmp")
width, height = img.size
i = 0


# translate a digit from decimal system to binary system
def D_B(x):
    v = list()
    for i in range(8):
        v.append(x % 2)
        x = floor(x / 2)
    return v


# translate a digit from binary system to decimal system
def B_D(binary):
    str1 = str(binary)
    decimal = 0
    for i in range(len(str1)):
        decimal = decimal + (int(str1[i]) * (2 ** i))
    return decimal


# read a file with the secret message
m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = []
for i in m_ascii:
    m_b.append(D_B(i))

# set the permutation matrix to achieve higher
# resistance from cryptanalysis
p = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1]])

m_b = np.array(m_b)
# apply permutation to the secret message
m_b_p = m_b.dot(p)

# go from 2D array to 1D string
m_b_ps = ''
for i in range(len(m_b_p)):
    for j in range(len(m_b_p[0])):
        m_b_ps += str(m_b_p[i][j])

# --------------------LSB encoding---------------------------
i = 0
for x in range(width):
    for y in range(height):
        pixel = list(img.getpixel((x, y)))
        if i < len(m_b_ps):
            # print(pixel[0], int(m_b_ps[i]))
            pixel[0] = pixel[0] & ~1 | int(m_b_ps[i])
            i += 1
        img.putpixel((x, y), tuple(pixel))
img.save("secret_img_p.bmp", "BMP")

# --------------------LSB decoding---------------------------
secret_img = Image.open("secret_img_p.bmp")
width, height = secret_img.size
m_b1, byte = [], []
for x in range(width):
    for y in range(height):
        pixel = list(secret_img.getpixel((x, y)))
        m_b1.append(pixel[0] & 1)

data, res_str = ''.join([str(i) for i in m_b1]), ''

# go from 1D string to 2D array
data_arr = []
for i in range(1, len(data), 8):
    data_arr.append([int(x) for x in data[i - 1:i + 7]])

# the rule for permutation decryption:
# multiplication by inverse of the matrix P
data_arr = np.array(data_arr)
p1 = np.linalg.inv(p)
print(p1)
result = data_arr.dot(p1)

# go from 2D array to 1D string
rs = ''
for i in range(len(result)):
    for j in range(len(result[0])):
        rs += str(int(result[i][j]))

# gain ASCII-code from the binary string 
for i in range(1, len(rs), 8):
    tmp = rs[i - 1:i + 7]
    m_b1 = B_D(tmp)
    res_str += chr(m_b1)

# print(res_str)

stego = open('stego_p.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
