import numpy as np
import math
from skimage.filters import sobel

def mirror_pad_image(image, pad_row, pad_col):
	"""
	Fungsi untuk menambah array/pad pada tepi citra
	Penambahan pad menggunakan mirroring
	"""
	row = np.size(image, 0)
	col = np.size(image, 1)

	paddedYX = np.zeros((row+2*pad_row, col+2*pad_col))

	for i in range(pad_row, row+pad_row):
		for j in range(pad_col, col+pad_col):
			paddedYX[i, j] = image[i-pad_row, j-pad_col]

	#Mirror X

	padded_img = np.copy(paddedYX)

	for i in range(pad_row):
		for j in range(np.size(padYX, 1)):
			padded_img[i, j] = padded_img[2*pad_row-i, j]
			padded_img[np.size(paddedYX, 0)-i-1, j] = padded_img[np.size(paddedYX, 0)-2*pad_row+i-1, j]


	#Mirror Y

	for j in range(pad_col):
		for i in range(np.size(paddedYX, 0)):
			padded_img[i, j] = padded_img[i, 2*pad_col-j]
			padded_img[i, np.size(paddedYX, 1)-j-1] = padded_img[i, np.size(paddedYX, 1)-2*pad_col+j-1]
	
	return padded_img