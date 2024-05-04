import numpy as np
from PIL import Image
from HammingCodec import hamming_codec_get_result

array_image = np.asarray(Image.open('C:/Users/User/PythonProjects/CascadeCodec/images/50.jpeg').convert('RGB'))
array_encode_image = np.vectorize(lambda uint8_item: hamming_codec_get_result(True, int(uint8_item)))(array_image)
print(array_encode_image)