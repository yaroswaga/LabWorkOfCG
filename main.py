import numpy as np
from PIL import Image
from src.model import Model
from cfg import height, width, zoom, IMAGES


img_mat = np.zeros((height, width, 3), dtype=np.uint8)
z_buffer = np.full((height, width, 1), np.inf)

model = Model(img_mat, zoom, z_buffer)

model.print_model()

img = Image.fromarray(img_mat)
img.save(IMAGES + "/img1.png")