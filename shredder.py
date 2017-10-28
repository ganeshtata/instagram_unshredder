from PIL import Image
from random import shuffle

SHREDS = 20
image = Image.open('random13.jpg')
shredded = Image.new('RGBA', image.size)
width, height = image.size
shred_width = width/SHREDS
print shred_width
sequence = range(0, SHREDS)
shuffle(sequence)

for i, shred_index in enumerate(sequence):
    shred_x1, shred_y1 = shred_width * shred_index, 0
    shred_x2, shred_y2 = shred_x1 + shred_width, height
    region =image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
    shredded.paste(region, (shred_width * i, 0))

    shredded.save('sample_shredded.png')