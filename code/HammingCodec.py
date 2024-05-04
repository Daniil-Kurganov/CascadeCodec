import math
import random
import numpy as np

int_r, int_n, int_k = 4, 15, 11

def calculation_of_correction_bits(list_code_word: list) -> str:
    '''Вычисление корректирующих битов в кодовом слове'''
    for int_position_of_correction_bit in [0, 1, 3, 7]:
        int_current_correction_bit = 0
        for int_position_of_tail_bit in range(int_position_of_correction_bit * 2, int_n, (int_position_of_correction_bit + 1) * 2):
            for int_bit_subblock_position in range (int_position_of_tail_bit - int_position_of_correction_bit, int_position_of_tail_bit + 1):
                if list_code_word[int_bit_subblock_position][0] != 'b':
                    int_current_correction_bit = int(ord(str(int_current_correction_bit)) ^ ord(str(list_code_word[int_bit_subblock_position])))
        list_code_word[int_position_of_correction_bit] = str(int_current_correction_bit)
    return ''.join(list_code_word)
def changing_the_bit(string_bit: str) -> str:
    '''Заменяет бит на противоположный'''
    return str((int(string_bit) + 1) % 2)
def hamming_codec_decode(string_item: str) -> int:
    '''Декодирование, выбиванием корректирующих битов из кодовых подслов и преобразование их в информационные'''
    list_information_word = []
    for int_position_of_bit in range(1, int_n + 1):
        if (int_position_of_bit & (int_position_of_bit - 1) == 0): pass
        else: list_information_word.append(string_item[int_position_of_bit - 1])
    return int(''.join(list_information_word), 2)
def hamming_codec_encode(int_item: int) -> str:
    '''Кодирование поступившего элемента'''
    string_iformation_word = format(int_item, '011b')
    list_code_word = []
    int_position_of_bits = 0
    for int_position_of_bit in range(1, int_n + 1):
        if (int_position_of_bit & (int_position_of_bit - 1) == 0): list_code_word.append('b' + str(int_position_of_bit))
        else:
            list_code_word.append(string_iformation_word[int_position_of_bits])
            int_position_of_bits += 1
    return calculation_of_correction_bits(list_code_word)
