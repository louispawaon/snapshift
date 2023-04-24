import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

def convert_to_jpg(input_path, output_path):
    register_heif_opener()
    for filename in os.listdir(input_path):
        print(filename)
        if filename.endswith('.HEIC') or filename.endswith('.heic'):
            filepath = os.path.join(input_path, filename)
            image = Image.open(filepath)

            #lacking code for heif conversion

def choose_folder():
    input_path = QFileDialog.getExistingDirectory(None,'Choose a Folder')
    return input_path


def main():
    input_path = choose_folder()
    if input_path:
        output_path = os.path.join(os.path.dirname(input_path), 'converted_jpgs')
        os.makedirs(output_path, exist_ok=True)
        try:
            convert_to_jpg(input_path, output_path)
            message_box = QMessageBox()
            message_box.setWindowTitle('Success')
            message_box.setText('Conversion complete.')
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        except Exception as e:
            message_box = QMessageBox()
            message_box.setWindowTitle('Error')
            message_box.setText(f'An error occurred: {e}')
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle('Error')
        message_box.setText('No folder selected.')
        message_box.setIcon(QMessageBox.Warning)
        message_box.exec_()


if __name__ == '__main__':
    app = QApplication([])
    main()