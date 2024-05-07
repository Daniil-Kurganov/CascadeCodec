import sys
import numpy as np
import qimage2ndarray
from PIL import Image
from HammingCodec import hamming_codec_encode, hamming_codec_decode
from InterleaverCodec import interleaver_codec_encode, interleaver_codec_decode
from ConvolutionalCodec import convolutional_codec_encode, convolutional_codec_decode
from GUI import *

def select_image_file() -> None:
    '''Вызово диалогового окна для выбора изображения'''
    global list_arrays_logs, bool_processing_is_done
    try:
        tuple_file_path_type_information = QtWidgets.QFileDialog.getOpenFileName(caption = 'Выберите изображение',
                                                                   directory = 'C:/Users/User/PythonProjects/CascadeCodec/images',
                                                                   filter = 'Изображения в формате JPEG (*.jpeg)')
        array_input_image = np.asarray(Image.open(tuple_file_path_type_information[0]).convert('RGB'))
        array_input_image_show = np.asarray(Image.fromarray(array_input_image.astype('uint8'), 'RGB').resize((300, 300)))
        qimage_input = qimage2ndarray.array2qimage(array_input_image_show)
        ui.LabelImage.setPixmap(QtGui.QPixmap.fromImage(qimage_input))
    except: return
    array_encode_hamming_image = np.vectorize(lambda uint8_item: hamming_codec_encode(int(uint8_item)))(array_input_image)
    list_arrays_logs = [array_encode_hamming_image]
    ui.ProgressBar.setProperty('value', 16)
    array_encode_interleaver_image = interleaver_codec_encode(array_encode_hamming_image)
    list_arrays_logs.append(array_encode_interleaver_image)
    ui.ProgressBar.setProperty('value', 32)
    array_encode_convolutional_image = np.vectorize(lambda string_current_submessage: convolutional_codec_encode(string_current_submessage))(
        array_encode_interleaver_image)
    list_arrays_logs.append(array_encode_convolutional_image)
    ui.ProgressBar.setProperty('value', 46)
    array_decode_convolutional_image = np.vectorize(lambda string_current_submessage: convolutional_codec_decode(string_current_submessage))(
        array_encode_convolutional_image)
    list_arrays_logs.append(array_decode_convolutional_image)
    ui.ProgressBar.setProperty('value', 64)
    array_decode_interleaver_image = interleaver_codec_decode(array_decode_convolutional_image)
    list_arrays_logs.append(array_decode_interleaver_image)
    ui.ProgressBar.setProperty('value', 80)
    array_result_image = np.vectorize(lambda string_item: hamming_codec_decode(string_item))(array_decode_interleaver_image)
    list_arrays_logs.append(array_result_image)
    ui.ProgressBar.setProperty('value', 100)
    array_result_image_show = np.asarray(Image.fromarray(array_result_image.astype('uint8'), 'RGB').resize((300, 300)))
    qimage_result = qimage2ndarray.array2qimage(array_result_image_show)
    ui.LabelImage.setPixmap(QtGui.QPixmap.fromImage(qimage_result))
    bool_processing_is_done = True
    return
def filling_the_table() -> None:
    '''Заполнение таблицы, в соответствии с выбранным пунктом'''
    global list_arrays_logs, ui, bool_processing_is_done
    if not bool_processing_is_done: return
    int_index_of_array = ui.ComboBoxSelectTable.currentIndex()
    ui.TableWidget.setRowCount(list_arrays_logs[int_index_of_array].shape[0])
    ui.TableWidget.setColumnCount(list_arrays_logs[int_index_of_array].shape[1])
    ui.TableWidget.horizontalHeader().setVisible(False)
    ui.TableWidget.verticalHeader().setVisible(False)
    for int_current_row_index in range(list_arrays_logs[int_index_of_array].shape[0]):
        for int_current_column_index in range(list_arrays_logs[int_index_of_array].shape[1]):
            ui.TableWidget.setItem(int_current_row_index, int_current_column_index, QtWidgets.QTableWidgetItem(str(
                list_arrays_logs[int_index_of_array][int_current_row_index][int_current_column_index])))
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    bool_processing_is_done = False
    ui.PushButtonSelectImage.clicked.connect(select_image_file)
    ui.ComboBoxSelectTable.currentIndexChanged.connect(filling_the_table)
    sys.exit(app.exec_())