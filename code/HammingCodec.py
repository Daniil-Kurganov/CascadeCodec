import math
import random
import numpy as np


def calculation_of_correction_bits(int_n: int, list_code_underword: list, bool_check: bool) -> str:
    '''Вычисление корректирующих битов в кодовых подсловах'''
    if bool_check: int_position_of_error_bit = 0
    for int_position_of_correction_bit in [0, 1, 3, 7]:
        int_current_correction_bit = 0
        for int_position_of_tail_bit in range(int_position_of_correction_bit * 2, int_n, (int_position_of_correction_bit + 1) * 2):
            for int_bit_subblock_position in range (int_position_of_tail_bit - int_position_of_correction_bit, int_position_of_tail_bit + 1):
                if list_code_underword[int_bit_subblock_position][0] != 'b':
                    int_current_correction_bit = int(ord(str(int_current_correction_bit)) ^ ord(str(list_code_underword[int_bit_subblock_position])))
        if not bool_check: list_code_underword[int_position_of_correction_bit] = str(int_current_correction_bit)
        elif int_current_correction_bit: int_position_of_error_bit += int_position_of_correction_bit + 1
    # print(list_code_underword)
    if bool_check:string_output = str(int_position_of_error_bit - 1)
    else: string_output = ''.join(list_code_underword)
    return string_output
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    if int(string_bit): return '0'
    else: return '1'
def cutting_code_subword_to_information_word(string_code_underword: str) -> str:
    '''Выбивание корректирующих битов из кодовых подслов и преобразование их в информационные'''
    list_current_information_underword = []
    # print(string_code_underword)
    for int_position_of_bit in range(1, int_n + 1):
        if (int_position_of_bit & (int_position_of_bit - 1) == 0): pass
        else: list_current_information_underword.append(string_code_underword[int_position_of_bit - 1])
    return ''.join(list_current_information_underword)
def hamming_codec_get_result(bool_encode_operation: bool, int_item: int) -> str:
    '''Запуск работы кодека в зависимости от типа флага'''
    global int_r,int_n, int_k
    int_r, int_n, int_k = 4, 15, 11
    if bool_encode_operation:
        string_iformation_word = format(int_item, '011b')
        list_code_underword = []
        int_position_of_bits = 0
        for int_position_of_bit in range(1, int_n + 1):
            if (int_position_of_bit & (int_position_of_bit - 1) == 0): list_code_underword.append('b' + str(int_position_of_bit))
            else:
                list_code_underword.append(string_iformation_word[int_position_of_bits])
                int_position_of_bits += 1
        return calculation_of_correction_bits(int_n, list_code_underword, False)

print(hamming_codec_get_result(True, 255))
print(hamming_codec_get_result(True, 25))



#
# print('Кодовое слово: ' + ''.join(list_code_underwords))
# print('Кодовые подслова: ')
# print(list_code_underwords)
# list_informaion_underwords.clear()
# for string_code_underword in list_code_underwords:
#     int_position_of_error = random.randint(0, len(string_code_underword) - 1)
#     print('Ошибка реальная: ' + str(int_position_of_error))
#     string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
#                                                         string_code_underword[int_position_of_error + 1:])
#     int_position_of_error = int(calculation_of_correction_bits(int_n, list_positions_of_correction_bits, list(string_code_underword), True))
#     print('Ошибка вычисленная: ' + str(int_position_of_error))
#     string_code_underword = (string_code_underword[:int_position_of_error] + changing_the_bit(string_code_underword[int_position_of_error]) +
#                                          string_code_underword[int_position_of_error + 1:])
#     string_current_information_underword = cutting_code_subword_to_information_word(string_code_underword)
#     list_informaion_underwords.append(string_current_information_underword)
# if int_count_of_zeros > 0: list_informaion_underwords[-1] = list_informaion_underwords[-1][int_count_of_zeros:]
# print('Информационные подслова после декодирования:')
# print(list_informaion_underwords)
# string_output_text_binary = ''.join(list_informaion_underwords)
# if string_input_text_binary != string_output_text_binary: print('Допущена ошибка при работе кодека!')
# else: print('Строки идентичны.')
# print('Декодированное информационное слово: ' + string_output_text_binary)
# print('Декодированное сообщение: ' + int(string_output_text_binary, 2).to_bytes((int(string_output_text_binary, 2).bit_length() + 7) // 8, 'big').decode())