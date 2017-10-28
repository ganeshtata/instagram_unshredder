import cv2
import numpy as np
from collections import deque


def sum_of_differences(col1, col2):
	differences_array = np.absolute(np.subtract(col1, col2, dtype=np.dtype(int)))
	return differences_array.sum()


def minimum_differences(image_shreds, current_shred, seen_indices, direction, omit_indices =[]):
	difference = -1
	pos = -1
	for index, shred in enumerate(image_shreds):
		if index in seen_indices or index in omit_indices:
			continue
		if direction == "right":
			pixel_difference_sum = sum_of_differences(current_shred, shred[:,0])
		else:
			pixel_difference_sum = sum_of_differences(current_shred, shred[:, -1])

		if difference == -1 or pixel_difference_sum < difference:
			difference = pixel_difference_sum
			pos = index
	return difference, pos


def combine_shreds(shreds):
	combined_image = shreds[0]
	for shred in shreds[1:]:
		combined_image = np.column_stack((combined_image, shred))
	return combined_image

rgb_image = cv2.imread('sample_shredded.png')
image_shreds = list()
for i in range(0, rgb_image.shape[1], 40):
	image_shreds.append(rgb_image[:, i:i + 40])
for i, shred_candidate in enumerate(image_shreds):
	ordered_shreds = deque()
	seen_indices = list()
	image_indices = deque()
	image_indices.append(i)
	ordered_shreds.append(shred_candidate)
	while len(ordered_shreds) < len(image_shreds):
		difference, pos = minimum_differences(image_shreds, ordered_shreds[0][:, 0], seen_indices, 'left')
		difference_omitting, _ = minimum_differences(image_shreds, image_shreds[pos][:, -1], seen_indices, 'right', [pos, image_indices[0]])
		difference1 = difference
		if difference < difference_omitting or difference_omitting == -1:
			flag = True
			ordered_shreds.appendleft(image_shreds[pos])
			image_indices.appendleft(pos)
			seen_indices.append(pos)
		else:
			break
	print len(ordered_shreds)
	if len(ordered_shreds) == len(image_shreds):
		break
unshredded_image = combine_shreds(list(ordered_shreds))
cv2.imwrite("unshredded.jpg", unshredded_image)
