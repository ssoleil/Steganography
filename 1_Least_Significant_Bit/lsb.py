from PIL import Image
from math import floor

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

# print red
# for x in range(width):
#    for y in range(height):
#        pixel = list(img.getpixel((x, y)))
#        print(pixel)

# ----------------------LSB encoding----------------------
i = 0
for x in range(width):
    for y in range(height):
        pixel = list(img.getpixel((x, y)))  # parse 3 image channels: red, green, blue
        if i < len(m_b):
            pixel[0] = pixel[0] & ~1 | int(m_b[i])  # clean or set the least bit according to the secret message
            i += 1
        img.putpixel((x, y), tuple(pixel))
img.save("secret_img_lsb.bmp", "BMP")

# print red
# for x in range(width):
#     for y in range(height):
#         pixel = list(img.getpixel((x, y)))
#         print(pixel)

# ---------------------LSB decoding------------------------
secret_img = Image.open("secret_img_lsb.bmp")
width, height = secret_img.size
m_b1 = []
for x in range(width):
    for y in range(height):
        pixel = list(secret_img.getpixel((x, y)))
        m_b1.append(pixel[0] & 1)

# translate the list with decrypted secret message to the binary string
data, res_str = ''.join([str(i) for i in m_b1]), ''

# string parsing: from each 8 binary symbols make a ASCII letter
for i in range(1, len(data), 8):
    tmp = data[i - 1:i + 7]
    m_b1 = B_D(tmp)
    res_str += chr(m_b1)

# write decrypted text file
stego = open('stego_lsb.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
