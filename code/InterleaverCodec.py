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
def interleaver_codec_encode(array_input: np.array) -> np.array:
    '''Процесс обработки входящего массива перемежителем'''
    global array_workspace, string_current_result
    array_workspace = np.full(array_input.shape[:2], fill_value = ('-' * 45))
    np.vectorize(lambda string_current_item: create_inreleaver_table_from_code_words(string_current_item, array_input))(array_input)
    for array_current_row in array_workspace:
        list_workspace = []
        for int_index_of_current_interleaver_column in range(45):
            string_current_result = ''
            np.vectorize(lambda string_current_code_word: create_interleaver_out_string(string_current_code_word,
                                                                                        int_index_of_current_interleaver_column))(array_current_row)
            list_workspace.append(string_current_result[1:])
        list_result.append(list_workspace)
    return np.array(list_result)

list_of_correction_bit_positions, list_result = [0, 1, 3, 7], []
int_index_of_current_row, int_index_of_current_column, int_index_of_current_item = 0, 0, -1
string_current_main_bits, string_current_check_bits = '', ''