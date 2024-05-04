import numpy as np
from PIL import Image

array_image = np.asarray(Image.open('images/50.jpeg').convert('RGB'))
print(array_image.shape)
print(array_image[0].shape)
print(array_image)