from PIL import Image
from math import floor

img = Image.open("tiger.bmp")
width, height = img.size
i = 0

delta, gama = 0.5, 5


def bright(x, y):
    """function of computing the full-color brightness of a pixel with provided coordinates (x, y)"""

    pix = img.getpixel((x, y))
    return pix[0] * 0.2989 + pix[1] * 0.58662 + pix[2] * 0.11448


def SV(x, y, b):
    """function of pixel blue channel modification"""

    return round(img.getpixel((x, y))[2] + (2 * b - 1) * delta * bright(x, y))


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


# open text file with the secret message, 
# write a list of ASCII symbols
# translate to the common binary string format
m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = ''
for i in m_ascii:
    m_b += D_B(i)

# ----------------------encoding----------------------
b = 0
for i in range(gama, height - gama):
    b = SV(i, i, int(m_b[i - gama]))
    pixel = list(img.getpixel((i, i)))
    if 0 <= b <= 255:
        pixel[2] = b
    elif b > 255:
        pixel[2] = 255
    elif b < 0:
        pixel[2] = 0
    img.putpixel((i, i), tuple(pixel))
img.save("secret_img_kjb.bmp", "BMP")

# print red
# for x in range(width):
#    for y in range(height):
#        pixel = list(img.getpixel((x, y)))
#        print(pixel)

# ----------------------decoding----------------------
secret_img = Image.open("secret_img_kjb.bmp")
width, height = secret_img.size
m_b1, b1 = '', 0

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

print(m_b1)
print(len(m_b1))

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(m_b1), 8):
    tmp = m_b1[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_kjb.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
