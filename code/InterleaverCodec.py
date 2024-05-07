import numpy as np

def create_interleaver_matrix(string_code_subword: str) -> None:
    '''Заполнение блочного перемежителя. Адаптирована под np.vectorize()'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows
    if int_counter_done_items == -1:
        int_counter_done_items = 0
        return
    string_current_interleaver_table_item = array_interleaver_table[int_counter_done_rows, int_counter_done_columns]
    list_main_bits, list_checking_bits = list(string_code_subword), []
    for int_current_position_of_correction_bit in [0, 0, 1, 4]:
        list_checking_bits.append(list_main_bits.pop(int_current_position_of_correction_bit))
    int_point_of_main_bits_insert_start, int_point_of_main_bits_insert_end = int_counter_done_items * 11, (int_counter_done_items + 1) * 11
    int_point_of_correction_bits_insert_start = (int_counter_done_items * 4) + 33
    int_point_of_correction_bits_insert_end = (int_counter_done_items * 4) + 37
    string_current_interleaver_table_item = (string_current_interleaver_table_item[0 : int_point_of_main_bits_insert_start] + ''.join(list_main_bits) +
                                             string_current_interleaver_table_item[int_point_of_main_bits_insert_end : int_point_of_correction_bits_insert_start] +
                                             ''.join(list_checking_bits) + string_current_interleaver_table_item[int_point_of_correction_bits_insert_end:])
    array_interleaver_table[int_counter_done_rows, int_counter_done_columns] = string_current_interleaver_table_item
    if int_counter_done_items < 2: int_counter_done_items += 1
    else:
        int_counter_done_items = 0
        if int_counter_done_columns < array_interleaver_table.shape[1] - 1: int_counter_done_columns += 1
        else:
            int_counter_done_columns = 0
            int_counter_done_rows += 1
    return
def create_current_string_interleaver_submessage(string_code_word: str, int_index_of_current_interleaver_column: int) -> None:
    '''Заполнение текущей строки подсообщения перемежителя. Адаптирована под np.vectorize()'''
    global string_current_result
    string_current_result += string_code_word[int_index_of_current_interleaver_column]
    return
def filling_interleaver_array_messages(string_item: str, array_input: np.array) -> None:
    '''Подготовка массива сообщений перемежителя. Преобразование стлобцов в строки. Адаптирована под np.vectorize()'''
    global array_workspace, int_index_of_current_row, int_index_of_current_column, int_index_of_current_item
    if int_index_of_current_item == -1:
        int_index_of_current_item += 1
        return
    for int_index_of_current_interleaver_column in range((len(array_input[0][0]) - 1)):
        array_workspace[int_index_of_current_row, int_index_of_current_column + int_index_of_current_interleaver_column] = (
            array_workspace[int_index_of_current_row, int_index_of_current_column + int_index_of_current_interleaver_column][:int_index_of_current_item] +
            string_item[int_index_of_current_interleaver_column] +
            array_workspace[int_index_of_current_row, int_index_of_current_column + int_index_of_current_interleaver_column][:int_index_of_current_item + 1])
    if int_index_of_current_item < (len(array_input[0][0]) - 1): int_index_of_current_item += 1
    else:
        if int_index_of_current_row < (array_input.shape[0] - 1):
            int_index_of_current_item = 0
            int_index_of_current_row += 1
    return
def interleaver_codec_encode(array_input: np.array) -> None:
    '''Процесс перемежения'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows, string_current_result
    array_interleaver_table = np.full(array_input.shape[:2], fill_value = ('-' * 45))
    int_counter_done_items, int_counter_done_columns, int_counter_done_rows = -1, 0, 0
    np.vectorize(lambda string_current_code_subword: create_interleaver_matrix(
        string_current_code_subword))(array_input)
    list_result = []
    for array_current_interleaver_table_row in array_interleaver_table:
        list_workspace = []
        for int_index_of_current_interleaver_column in range(45):
            string_current_result = ''
            np.vectorize(lambda string_current_code_word: create_current_string_interleaver_submessage(
                string_current_code_word, int_index_of_current_interleaver_column))(array_current_interleaver_table_row)
            list_workspace.append(string_current_result[1:])
        list_result.append(list_workspace)
    return np.array(list_result)
def decode_interleaver_message_subword(string_message_subword_bit: str) -> None:
    '''Распределение битов подсообщения на кодовый словаю . Адаптирована под np.vectorize()'''
    global array_message_subword, int_counter_done_bits, int_counter_done_rows, array_interleaver_table, int_counter_done_items
    if int_counter_done_bits == -1:
        int_counter_done_bits += 1
        return
    string_code_word = array_interleaver_table[int_counter_done_rows][int_counter_done_bits]
    string_code_word = string_code_word[:int_counter_done_items] + string_message_subword_bit + string_code_word[int_counter_done_items:]
    array_interleaver_table[int_counter_done_rows, int_counter_done_bits] = string_code_word
    int_counter_done_bits += 1
    return
def decode_code_words_from_interleaver_submessages(string_message_subword: str) -> None:
    '''Декодирование кодовых подслов из массива сообщения перемежителя. Адаптирована под numpy.vectorize()'''
    global int_counter_done_items, int_counter_done_columns, int_counter_done_rows, array_message_subword, int_counter_done_bits,\
        array_interleaver_table
    if int_counter_done_items == -1:
        int_counter_done_items += 1
        return
    array_message_subword = np.array(list(string_message_subword))
    int_counter_done_bits = -1
    np.vectorize(lambda string_current_message_subword: decode_interleaver_message_subword(string_current_message_subword))(array_message_subword)
    if int_counter_done_items < 44: int_counter_done_items += 1
    else:
        int_counter_done_rows += 1
        int_counter_done_items = 0
    return
def decode_pixel_code_subwords_from_code_subword(string_pixel_code_subwords) -> None:
    '''Декодирование кодового подслова в 3 кодовых подслова пикселя. Адаптирована под numpy.vectorize()'''
    global array_interleaver_table, int_counter_done_columns, int_counter_done_rows, array_result
    if int_counter_done_columns == -1:
        int_counter_done_columns += 1
        return
    string_code_subword = array_interleaver_table[int_counter_done_rows][int_counter_done_columns]
    for int_current_pixel_index in range(3):
        int_current_point_of_main_bits_pop_start = int_current_pixel_index * 11
        int_current_point_of_main_bits_pop_end = (int_current_pixel_index + 1) * 11
        int_current_point_of_correction_bits_pop_start = (int_current_pixel_index * 4) + 33
        int_current_point_of_correction_bits_pop_end = (int_current_pixel_index * 4) + 37
        list_current_pixel_code_subword = list(string_code_subword[int_current_point_of_main_bits_pop_start : int_current_point_of_main_bits_pop_end])
        list_current_correction_bits = list(string_code_subword[int_current_point_of_correction_bits_pop_start : int_current_point_of_correction_bits_pop_end])
        for int_list_index, int_current_index_of_correction_bit in enumerate([0, 1, 3, 7]):
            list_current_pixel_code_subword.insert(int_current_index_of_correction_bit, list_current_correction_bits[int_list_index])
        array_result[int_counter_done_rows, int_counter_done_columns, int_current_pixel_index] = ''.join(list_current_pixel_code_subword)
    if int_counter_done_columns < array_interleaver_table.shape[1] - 1: int_counter_done_columns += 1
    else:
        int_counter_done_columns = 0
        int_counter_done_rows += 1
    return
def interleaver_codec_decode(array_input: np.array) -> np.array:
    '''Процесс деперемежения'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows, array_result
    array_interleaver_table = np.full((array_input.shape[0], len(array_input[0][0])), fill_value=('-' * 45))
    int_counter_done_items, int_counter_done_rows = -1, 0
    np.vectorize(lambda string_current_submessage: decode_code_words_from_interleaver_submessages(string_current_submessage))(array_input)
    array_result = np.full((array_interleaver_table.shape[0], array_interleaver_table.shape[0], 3), fill_value = ('-' * 15))
    int_counter_done_columns, int_counter_done_rows = -1, 0
    np.vectorize(lambda string_current_code_subword: decode_pixel_code_subwords_from_code_subword(string_current_code_subword))(array_interleaver_table)
    return(array_result)
