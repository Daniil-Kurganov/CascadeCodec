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
def filling_interleaver_array(string_item: str, array_input: np.array) -> None:
    '''Подготовка массива перемежителя. Преобразование стлобцов в строки. Адаптирована под np.vectorize()'''
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
def decode_from_interleaver_table(string_item: str) -> None:
    '''Декодирование кодовых подслов из массива перемежителя. Адаптирована под numpy.vectorize()'''
    global int_index_of_current_column, int_index_of_current_row, int_index_of_current_item, list_correction_bit_positions, array_result
    if int_index_of_current_item == -1:
        int_index_of_current_item += 1
        return
    list_code_word, list_code_subwords, list_result = list(string_item), [], []
    int_point_of_trimm = len(list_code_word) - (len(list_correction_bit_positions) * 3)
    list_main_bits, list_correction_bits  = list_code_word[:int_point_of_trimm], list_code_word[int_point_of_trimm:]
    int_index_of_last_insert = 0
    for int_index_of_current_insert in range(len(list_main_bits) // 3, len(list_main_bits) + 1, len(list_main_bits) // 3):
        list_code_subwords.append(''.join(list_main_bits[int_index_of_last_insert : int_index_of_current_insert]))
        int_index_of_last_insert = int_index_of_current_insert
    for string_current_code_subword in list_code_subwords:
        for int_index_of_current_currection_bit_position in list_correction_bit_positions:
            list_result.append(string_current_code_subword[:int_index_of_current_currection_bit_position] + list_correction_bits.pop(0) +
                                           string_current_code_subword[int_index_of_current_currection_bit_position:])
    array_result[int_index_of_current_row, int_index_of_current_column, 0] = list_result[0]
    array_result[int_index_of_current_row, int_index_of_current_column, 1] = list_result[1]
    array_result[int_index_of_current_row, int_index_of_current_column, 2] = list_result[2]
    if int_index_of_current_column < (array_result.shape[1] - 1): int_index_of_current_column += 1
    else:
        int_index_of_current_column = 0
        int_index_of_current_row += 1
    return
def interleaver_codec_encode(array_input: np.array) -> None:
    '''Процесс перемежения'''
    global array_interleaver_table, int_counter_done_items, int_counter_done_columns, int_counter_done_rows, string_current_result
    array_interleaver_table = np.full(array_input.shape[:2], fill_value = ('-' * 45))
    int_counter_done_items, int_counter_done_columns, int_counter_done_rows = -1, 0, 0
    np.vectorize(lambda string_current_code_subword: create_interleaver_matrix(
        string_current_code_subword))(array_input)
    print(array_interleaver_table)
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
def interleaver_codec_decode(array_input:np.array) -> np.array:
    '''Процесс деперемежения'''
    global array_workspace, int_index_of_current_row, int_index_of_current_column, int_index_of_current_item, array_result
    int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
    array_workspace = np.full((array_input.shape[0], len(array_input[0][0])), fill_value = ('-' * array_input.shape[1]))
    np.vectorize(lambda string_current_submessage: filling_interleaver_array(string_current_submessage, array_input))(array_input)
    # print()
    # print()
    # print(array_workspace)
    # print(array_workspace.shape)
    int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
    array_result = np.full((array_workspace.shape[0], array_workspace.shape[1], 3), fill_value = ('-' * 3))
    np.vectorize(lambda string_current_code_word: decode_from_interleaver_table(string_current_code_word))(array_workspace)
    return array_result

list_correction_bit_positions = [0, 1, 3, 7]
int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
string_current_main_bits, string_current_check_bits = '', ''