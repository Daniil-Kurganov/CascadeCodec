import sys
from GUI import *

def select_image_file() -> None:
    '''Вызово диалогового окна для выбора изображения'''
    global string_image_file_path
    tuple_file_path_type_information = QtWidgets.QFileDialog.getOpenFileName(caption = 'Выберите изображение',
                                                                   directory = 'C:/Users/User/PythonProjects/CascadeCodec/images',
                                                                   filter = 'Изображения в формате JPEG (*.jpeg)')
    string_image_file_path = tuple_file_path_type_information[0]
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    string_image_file_path = ''
    ui.PushButtonSelectImage.clicked.connect(select_image_file)
    sys.exit(app.exec_())