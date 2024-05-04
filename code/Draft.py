import numpy as np
from PIL import Image

array_image = np.asarray(Image.open('C:/Users/User/PythonProjects/CascadeCodec/images/50.jpeg').convert('RGB'))
# Image.fromarray(array_image).save('result.jpeg')
print(array_image.dtype)