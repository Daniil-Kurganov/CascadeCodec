import numpy as np
from InterleaverCodec import interleaver_codec_encode, interleaver_codec_decode

a = np.asarray([[['000', '001', '002'], ['010', '011', '012']],
                [['100', '101', '102'], ['110', '111', '112']]])
a_enc = interleaver_codec_encode(a)
a_dec = interleaver_codec_decode(a_enc)