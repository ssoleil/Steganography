from PIL import Image
import numpy as np
from lib import D_B, B_D, DCT

# number of blocks
block = 8
# certain positive value - threshold - for encoding and decoding
pr = 5

# save the secret message container in the jpg format
Image.open("secret_img_KZ.bmp").save("secret_img_KZ_attack.jpg", quality=75)
secret_img = Image.open("secret_img_KZ_attack.jpg")
secret_img = np.array(secret_img)
width, height = len(secret_img[0]), len(secret_img)
sliced = []

m = open('secret_message.txt', 'r').read()
m_ascii = [ord(i) for i in m]
m_b = ''
for i in m_ascii:
    m_b += D_B(i)
print("Encoded message is: " + m_b[:100] + '...')

# divide an image into blocks
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
stego = open('stego_KZ_attack.txt', 'w', encoding="utf-8")
stego.write(res_str)
stego.close()
