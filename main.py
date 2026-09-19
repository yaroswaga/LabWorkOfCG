import numpy as np
from PIL import Image
from src.model import Model


width = 10000
height = 10000
zoom = 50000

img_mat = np.zeros((height, width, 3), dtype=np.uint8)

model = Model(img_mat, zoom)
model.print_model()

img = Image.fromarray(img_mat)
img.save("images/img.png")