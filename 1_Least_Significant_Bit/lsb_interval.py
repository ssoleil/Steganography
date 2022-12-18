from PIL import Image
from math import floor
from random import randrange

img = Image.open("tiger.bmp")
width, height = img.size
i = 0


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

# define secret random permutation rule 
# for embedding bits into the container
key = [floor(randrange(0, width)) for i in range(width)]

# --------------------LSB encoding---------------------------
i = 0
for x in key:
    for y in range(height):
        pixel = list(img.getpixel((x, y)))
        if i < len(m_b):
            pixel[0] = pixel[0] & ~1 | int(m_b[i])
            i += 1
        img.putpixel((x, y), tuple(pixel))
img.save("secret_img_i.bmp", "BMP")

# --------------------LSB decoding---------------------------
secret_img = Image.open("secret_img_i.bmp")
width, height = secret_img.size
m_b1, byte = [], []

# use the same secret rule to obtain correct order of bits
for x in key:
    for y in range(height):
        pixel = list(secret_img.getpixel((x, y)))
        m_b1.append(pixel[0] & 1)

data, res_str = ''.join([str(i) for i in m_b1]), ''

for i in range(1, len(data), 8):
    tmp = data[i - 1:i + 7]
    m_b1 = B_D(tmp)
    res_str += chr(m_b1)

stego = open('stego_i.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
