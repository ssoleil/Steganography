from PIL import Image
from math import ceil, floor
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


# open text file with the secret message, 
# write a list of ASCII symbols
# translate to the common binary string format
m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = ''
for i in m_ascii:
    m_b += D_B(i)
print("encode message is: \n" + m_b)

# calculate a random key table of differences between adjacent pixels
d = [[i - 255 for i in range(512)],
     [ceil(randrange(0, 2)) for i in range(512)]]

# for i in range(510):
#    print(d[0][i], d[1][i])

# ----------------------encoding----------------------
# calculate the difference b between adjacent (red) pixels of each row
# if the bit value of the key for the given difference does not match 
# the embedded bit, then search (to the right) for the nearest matching bit
i, b = 0, 0
for y in range(height):
    b = img.getpixel((0, y))[0] - img.getpixel((1, y))[0]
    if int(m_b[i]) == d[1][b + 255]:
        i += 1
        continue
    elif i < len(m_b):
        j = 0
        while int(m_b[i]) != d[1][b + 255 + j] and j < 255:
            j += 1
        pixel = list(img.getpixel((0, y)))
        pixel[0] = pixel[0] + d[0][b + 255 + j] - b
        i += 1
    img.putpixel((0, y), tuple(pixel))
img.save("secret_img_quant.bmp", "BMP")

# print red
# for x in range(width):
#    for y in range(height):
#        pixel = list(img.getpixel((x, y)))
#        print(pixel)

# ----------------------decoding----------------------
secret_img = Image.open("secret_img_quant.bmp")
width, height = secret_img.size
m_b1, b1 = '', 0

for y in range(height):
    b1 = secret_img.getpixel((0, y))[0] - secret_img.getpixel((1, y))[0]
    m_b1 += str(d[1][b1 + 255])

print("\ndecode message is: \n" + m_b1)
print("length of decode message is: ", len(m_b1))

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(m_b1), 8):
    tmp = m_b1[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_quant.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
