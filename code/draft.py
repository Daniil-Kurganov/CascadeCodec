import numpy as np
from InterleaverCodec import interleaver_codec_encode, interleaver_codec_decode
from HammingCodec import hamming_codec_encode, hamming_codec_decode

def fill_matr(string_code_subword: str) -> None:
    '''Заполнение блочного перемежителя'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows
    if int_counter_done_items == -1:
        int_counter_done_items = 0
        return
    string_current_interleaver_table_item = array_interleaver_table[int_counter_done_rows, int_counter_done_columns]
    list_main_bits, list_checking_bits = list(string_code_subword), []
    for int_current_position_of_correction_bit in [0, 1, 3, 7]:
        list_checking_bits.append(list_main_bits.pop(int_current_position_of_correction_bit))
    int_point_of_main_bits_insert_start, int_point_of_main_bits_insert_end = int_counter_done_items * 11, (int_counter_done_items + 1) * 11
    int_point_of_correction_bits_insert_start = (int_counter_done_items * 4) + 33
    int_point_of_correction_bits_insert_end = (int_counter_done_items * 4) + 37
    string_current_interleaver_table_item
    # Вставить в строку ^


    string_current_interleaver_table_item = string_current_interleaver_table_item[:int_inserting_point - 1] +
    array_workspace[int_counter_done_rows][int_counter_done_columns].insert(int_counter_done_items, list_main_bits)
    list_workspace[int_counter_done_rows][int_counter_done_columns].append(list_checking_bits)
    if int_counter_done_items < 2: int_counter_done_items += 1
    else:
        list_current_row = []
        for list_current_bits in list_workspace[int_counter_done_rows][int_counter_done_columns]:
            list_current_row += list_current_bits
        list_workspace[int_counter_done_rows][int_counter_done_columns] =list_current_row

def encode(array_input: np.array) -> None:
    '''Процесс перемежения'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows
    array_interleaver_table = np.full(array_input[:2], fill_value = ('-' * 45))
    int_counter_done_items, int_counter_done_columns, int_counter_done_rows = -1, 0, 0



a = np.asarray([[[10, 100, 255], [54, 31, 91]],
                [[192, 62, 109], [203, 188, 215]]])
array_encode_hamming_image = np.vectorize(lambda uint8_item: hamming_codec_encode(int(uint8_item)))(a)
print(array_encode_hamming_image)
print(array_encode_hamming_image.shape)
array_encode_interleaver_image = interleaver_codec_encode(array_encode_hamming_image)
# print(array_encode_interleaver_image)
# print(array_encode_interleaver_image.shape)
# array_decode_interleaver_image = interleaver_codec_decode(array_encode_interleaver_image)
# array_decode_hamming_image = np.vectorize(lambda string_item: hamming_codec_decode(string_item))(array_decode_interleaver_image)
# if np.array_equal(array_encode_interleaver_image, array_decode_interleaver_image): print('Oh, yeah!')
# else: print("oh no")