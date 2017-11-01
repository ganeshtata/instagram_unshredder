import numpy as np
from collections import deque
from PIL import Image
from random import shuffle


def sum_of_differences(col1, col2):
    differences_array = np.absolute(np.subtract(col1, col2, dtype=np.dtype(int)))
    return differences_array.sum()


def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if not prev or abs(item - prev) <= 0.02:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group


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


def unshred_image(shred_width):
    rgb_image = np.asarray(Image.open('sample_shredded.png'))
    image_shreds = list()
    for i in range(0, rgb_image.shape[1], shred_width):
        image_shreds.append(rgb_image[:, i:i + shred_width])
    for i, shred_candidate in enumerate(image_shreds):
        differences = list()
        ordered_shreds = deque()
        seen_indices = list()
        image_indices = deque()
        image_indices.append(i)
        ordered_shreds.append(shred_candidate)
        while len(ordered_shreds) < len(image_shreds):
            difference, pos = minimum_differences(image_shreds, ordered_shreds[0][:, 0], seen_indices, 'left')
            difference_omitting, _ = minimum_differences(image_shreds, image_shreds[pos][:, -1], seen_indices, 'right', [pos, image_indices[0]])
            if difference < difference_omitting or difference_omitting == -1:
                differences.append(difference / (((255)*3)*rgb_image.shape[0]*2.0))
                ordered_shreds.appendleft(image_shreds[pos])
                image_indices.appendleft(pos)
                seen_indices.append(pos)
            else:
                break
        if len(ordered_shreds) == len(image_shreds) and len(list(grouper(sorted(differences)))) == 1:
            break
    unshredded_image = combine_shreds(list(ordered_shreds))
    im = Image.fromarray(np.uint8(unshredded_image))
    #cv2.imwrite(, unshredded_image)
    im.save('unshredded.jpg')


def shred_image(file_name):
    SHREDS = 20
    image = Image.open(file_name)
    shredded = Image.new('RGBA', image.size)
    width, height = image.size
    shred_width = width/SHREDS
    sequence = range(0, SHREDS)
    shuffle(sequence)

    for i, shred_index in enumerate(sequence):
        shred_x1, shred_y1 = shred_width * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + shred_width, height
        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        shredded.paste(region, (shred_width * i, 0))
    shredded.save('sample_shredded.png')
    return shred_width

shred_width = shred_image('/home/tata/Projects/Computer Vision/Instagram_unshredder/random6.jpg')
unshred_image(shred_width)