import numpy as np
from PIL import Image
from HammingCodec import hamming_codec_encode, hamming_codec_decode
from InterleaverCodec import interleaver_codec_encode

array_input_image = np.asarray(Image.open('C:/Users/User/PythonProjects/CascadeCodec/images/50.jpeg').convert('RGB'))
array_encode_hamming_image = np.vectorize(lambda uint8_item: hamming_codec_encode(int(uint8_item)))(array_input_image)
array_encode_interleaver_image = interleaver_codec_encode(array_encode_hamming_image)
# array_decode_hamming_image = np.vectorize(lambda string_item: hamming_codec_decode(string_item))(array_encode_hamming_image)
# if np.array_equal(array_input_image, array_decode_hamming_image): print('Oh, yeah!')
print(array_encode_interleaver_image.shape)
