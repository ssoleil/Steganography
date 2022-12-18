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
print("encode message is: \n" + m_b)

# print each image pixel from top-right to bottom-left corner
# for x in range(width):
#    for y in range(height):
#        pixel = list(img.getpixel((x, y)))
#        print(pixel)

# ----------------------encoding----------------------

# count the parity bit by summing the values of the red 
# channel of each pixel in the block
i, b = 0, 0
for x in range(width):
    for y in range(height):
        b += img.getpixel((x, y))[0]
    if i < len(m_b) and m_b[i] != b % 2:
        pixel = list(img.getpixel((x, 0)))
        pixel[0] = pixel[0] & ~1 | int(m_b[i])
    i += 1
    img.putpixel((x, 0), tuple(pixel))
img.save("secret_img_block.bmp", "BMP")

# ----------------------decoding----------------------

# knowing the secret rule of partitioning into blocks (by columns),
# we can count NZB in the first pixel of each of them
secret_img = Image.open("secret_img_block.bmp")
width, height = secret_img.size
m_b1, b1 = '', 0
for x in range(width):
    m_b1 += str(secret_img.getpixel((x, 0))[0] & 1)

print("\ndecode message is: \n" + m_b1)
print("length of decode message is: ", len(m_b1))

# string parsing: from each 8 binary symbols make a ASCII letter
res_str = ''
for i in range(1, len(m_b1), 8):
    tmp = m_b1[i - 1:i + 7]
    m_bb1 = B_D(tmp)
    res_str += chr(m_bb1)

# write decrypted text file
stego = open('stego_block.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
