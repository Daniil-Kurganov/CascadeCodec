import numpy as np
from InterleaverCodec import interleaver_codec_encode, interleaver_codec_decode
from HammingCodec import hamming_codec_encode, hamming_codec_decode

a = np.asarray([[[10, 100, 255], [54, 31, 91]],
                [[192, 62, 109], [203, 188, 215]]])
array_encode_hamming_image = np.vectorize(lambda uint8_item: hamming_codec_encode(int(uint8_item)))(a)
print(array_encode_hamming_image)
array_encode_interleaver_image = interleaver_codec_encode(array_encode_hamming_image)
print(array_encode_interleaver_image)
array_decode_interleaver_image = interleaver_codec_decode(array_encode_interleaver_image)
print(array_decode_interleaver_image)
# array_decode_hamming_image = np.vectorize(lambda string_item: hamming_codec_decode(string_item))(array_decode_interleaver_image)
# if np.array_equal(array_encode_interleaver_image, array_decode_interleaver_image): print('Oh, yeah!')
# else: print("oh no")