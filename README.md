# Steganography

> This repository is dedicated to the different steganography methods that were learned on the course at the V. N. Karazin Kharkiv National University. All methods are implemented as independent and can be used separately from each other.

## Install required modules
For most programs, the following modules were used. To install, use the following commands:
```pip install numpy```
```pip install Pillow```
```pip install opencv-python```
```pip install matplotlib```


## Least Significant Bit

This method uses weak human sensitivity to slight changes in image brightness.

- The **least significant bit** (LSB) carries the least information when encoding the brightness of a pixel. Hence, human vision is not able to distinguish between changes in the picture when this bit is changed. Therefore, we can use LSB as a place to store secret information.

- To increase the cryptographic strength of the LSB, the embedding of secret bits does not occur sequentially. The **random interval method** consists in randomly distributing the bits of the secret message across the container. Each bit of the message is sequentially inserted into a column from 0 to (width - 1) and into that row, the index of which is determined by the pseudo-random secret key.

- The essence of the **pseudo-random permutation method** is to use a permutation cipher (given by a matrix P) for pre-processing informational data bits. In a permutation cipher, the order of the bits of the secret message is changed. Thus, the probability of detecting the presence of a hidden message is reduced. 

## Hiding data in the spatial domain of images

- To implement the **method of hiding data in blocks** on the image, the container image is divided into N non-intersecting secret blocks. Only one bit will be hidden in each block.

- **Image quantization method**. To hide the i-th bit of the message, the *difference* between pixels i and i+1 is calculated. If at the same time i-th bit does not correspond to the secret bit that needs to be hidden, then the value of the *difference i* is replaced by the closest *difference i* for which this condition is fulfilled. At the same time, the pixel intensity values between which the difference was calculated are adjusted accordingly.

- **Kutter–Jordan–Bossen method**. The secret bit is embedded in the blue channel by modifying the brightness. When extracting an embedded bit, the difference between the current (x, y * B) and predicted (x, y * B') pixel intensity values is calculated.

## Spread Spectrum Image Steganography
 
##### Hiding with orthogonal discrete signals
 
1. Formation of **Walsh–Hadamard orthogonal discrete signals** using recursive matrix. The Hadamard matrix is characterized by the mutual orthogonality of all rows and columns.
2. Coding of secret data bits by **complex discrete signals**. The procedure consists in multiplying the modulated message by discrete Walsh–Hadamard signals.
3. **The embedding (encoding) algorithm** consists in summing the data of the container (a digital image) with modulated complex discrete signals of the secret message.
4. **Decoding:** k message elements are embedded in each row of the container, i.e. for each row we calculate the correlation coefficient k times. If the sign of the coefficient is negative, this is equal to signal -1, if it is positive, this is equal to signal 1.
5. **Evaluation** of the probability of correctly extracting the message and the amount of image distortion. 

    > Increasing the number of embedded data bits leads to an increase in the probability of a data extraction error, as well as an increase in the introduced distortions in the image container. 

    > An increase in the signal energy g leads to a decrease in the probability of errors in extracting information bits and immediately to an increase in image distortion.
 
##### Hiding with quasi-orthogonal discrete signals  

The values of the correlation coefficient of quasi-orthogonal discrete signals do not differ significantly from zero (due to the pseudo-randomness of their formation).  Quasi-orthogonal signals make it possible to significantly increase the bandwidth of steganochannels with a smaller amount of picture distortion.

The process is the same with the exception of modifying the decryption algorithm. We need to determine with which of the quasi-orthogonal signals the row has the highest correlation. 

> Note that quasi-orthogonal discrete signals can have a strong correlation with individual fragments of the image container, so the extraction error is significant. Moreover, embedding a message with such a high value of signal energy (g = 40) leads to a rapid distortion of the image.

##  Hiding data in the frequency domain of images
Steganographic methods in the spatial image domain are vulnerable to most of the known image distortion attacks (e.g., JPED-compression). Therefore, there are methods of hiding data in the frequency space of the image.
- **Koch-Zhao method**. The input image is divided into blocks of size 8x8 pixels, for each of which the DCT (Discrete Cosine Transform) is applied. In this way, we obtained the matrix of DCT coefficients. Each block hides one data bit. It is necessary to agree in advance on two specific DCT coefficients from each block, which will be used for data hiding. To transmit bit "0", it is necessary that the difference in the absolute values of the selected DCT coefficients exceed a certain positive value (pr). To transmit a "1" bit, this difference is made smaller than some negative value (-pr). A similar procedure for selecting coefficients is performed to extract data.
An imitation of **a steganographic attack** showed that even with the jpg image format, the secret message can be decrypted without errors.
- **Benham-Memon-Yeo-Yeung method**. This is an optimized version of the method discussed above. It was proposed to use the most suitable blocks for embedding, as well as three DCT coefficients, which significantly reduces the visual distortion of the container. The following image blocks are considered suitable for embedding:
-- blocks should not have sharp brightness transitions,
-- blocks should not be too monochrome.

**The execution time comparison** of the own DCT implementation with the cv2 implementation on the same input data was carried out. To run the file ```time.py``` it's necessary to install the ```opencv``` library.

**2020. Kharkiv, Ukraine.**

