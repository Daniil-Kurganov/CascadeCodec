import numpy as np

def create_inreleaver_table_from_code_words(string_item: str, array_input: np.array) -> None:
    '''Функция создания блочного перемежителя для массива строк кодовых подслов. Адаптирована под numpy.vectorize()'''
    global string_current_result, string_current_check_bits, int_index_of_current_column, int_index_of_current_row, int_index_of_current_item,\
        list_of_correction_bit_positions, string_current_main_bits, array_workspace
    if int_index_of_current_item == -1:
        int_index_of_current_item += 1
        return
    list_workspace = list(string_item)
    string_current_check_bits += ''.join([list_workspace.pop(int_index_of_current_correction_bit) for int_index_of_current_correction_bit
                                             in list_of_correction_bit_positions])
    string_current_main_bits += ''.join(list_workspace)
    if int_index_of_current_item < (array_input.shape[2] - 1): int_index_of_current_item += 1
    else:
        array_workspace[int_index_of_current_row, int_index_of_current_column] = string_current_main_bits + string_current_check_bits
        string_current_main_bits, string_current_check_bits = '', ''
        int_index_of_current_item = 0
        if int_index_of_current_column < (array_input.shape[1] - 1): int_index_of_current_column += 1
        else:
            int_index_of_current_column = 0
            int_index_of_current_row += 1
    return
def create_interleaver_out_string(string_code_word: str, int_index_of_current_interleaver_column: int) -> None:
    global string_current_result
    string_current_result += string_code_word[int_index_of_current_interleaver_column]
    return
# def create_inreleaver_table(string_item: str, array_input: np.array, bool_encode: bool) -> None:
#     '''Функция создания блочного перемежителя для массива строк кодовых подслов. Адаптирована под numpy.vectorize()'''
#     global string_current_result, string_current_check_bits, int_index_of_current_column, int_index_of_current_row, int_index_of_current_item,\
#         list_of_correction_bit_positions, string_current_main_bits, array_workspace
#     if int_index_of_current_item == -1:
#         int_index_of_current_item += 1
#         return
#     if bool_encode: list_workspace = list(string_item)
#     string_current_check_bits += ''.join([list_workspace.pop(int_index_of_current_correction_bit) for int_index_of_current_correction_bit
#                                              in list_of_correction_bit_positions])
#     string_current_main_bits += ''.join(list_workspace)
#     if int_index_of_current_item < (array_input.shape[2] - 1): int_index_of_current_item += 1
#     else:
#         array_workspace[int_index_of_current_row, int_index_of_current_column] = string_current_main_bits + string_current_check_bits
#         string_current_main_bits, string_current_check_bits = '', ''
#         int_index_of_current_item = 0
#         if int_index_of_current_column < (array_input.shape[1] - 1): int_index_of_current_column += 1
#         else:
#             int_index_of_current_column = 0
#             int_index_of_current_row += 1
#     return
def interleaver_codec_encode(array_input: np.array) -> np.array:
    '''Процесс перемежения'''
    global array_workspace, string_current_result, int_index_of_current_row, int_index_of_current_column, int_index_of_current_item
    int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
    array_workspace = np.full(array_input.shape[:2], fill_value = ('-' * 9))
    np.vectorize(lambda string_current_item: create_inreleaver_table_from_code_words(string_current_item, array_input))(array_input)
    for array_current_row in array_workspace:
        list_workspace = []
        for int_index_of_current_interleaver_column in range(9):
            string_current_result = ''
            np.vectorize(lambda string_current_code_word: create_interleaver_out_string(string_current_code_word,
                                                                                        int_index_of_current_interleaver_column))(array_current_row)
            list_workspace.append(string_current_result[1:])
        list_result.append(list_workspace)
    return np.array(list_result)
def interleaver_codec_decode(array_input:np.array) -> np.array:
    '''Процесс деперемежения'''
    global array_workspace, int_index_of_current_row, int_index_of_current_column, int_index_of_current_item
    int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
    array_workspace = np.full((array_input.shape[0], len(array_input[0][0])), fill_value = ('-' * array_input.shape[1]))
    np.vectorize(lambda string_current_submessage: filling_interleaver_array(string_current_submessage, array_input))(array_input)
    print(array_workspace)
def filling_interleaver_array(string_item: str, array_input: np.array) -> None:
    '''Подготовка массива перемежителя. Преобразование стлобцов в строки'''
    global array_workspace, int_index_of_current_row, int_index_of_current_column, int_index_of_current_item
    if int_index_of_current_item == -1:
        int_index_of_current_item += 1
        return
    string_current_line_1 = array_workspace[int_index_of_current_row][int_index_of_current_column]
    string_current_line_2 = array_workspace[int_index_of_current_row][int_index_of_current_column + 1]
    array_workspace[int_index_of_current_row, int_index_of_current_column] = (string_current_line_1[:int_index_of_current_item] + string_item[0] +
                                                                              string_current_line_1[:int_index_of_current_item + 1])
    array_workspace[int_index_of_current_row, int_index_of_current_column + 1] = (string_current_line_2[:int_index_of_current_item] + string_item[0] +
                                                                                  string_current_line_2[:int_index_of_current_item + 1])
    print(array_workspace)
    if int_index_of_current_item < (array_input.shape[1] - 1): int_index_of_current_item += 1
    else:
        int_index_of_current_item = 0
        int_index_of_current_row += 1
    return

list_of_correction_bit_positions, list_result = [1], []
int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
string_current_main_bits, string_current_check_bits = '', ''