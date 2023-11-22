import os
from PIL import Image
import pillow_heif
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox


def convert_to_jpg(input_path, output_path):
    for filename in os.listdir(input_path):
        if filename.lower().endswith((".heic", ".heif")):
            filepath = os.path.join(input_path, filename)
            heif_file = pillow_heif.read_heif(filepath)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
            output_path_new = os.path.join(
                output_path, os.path.splitext(filename)[0] + ".jpg"
            )
            image.save(output_path_new)


def choose_folder():
    input_path = QFileDialog.getExistingDirectory(None, "Choose a Folder")
    return input_path


def main():
    input_path = choose_folder()
    if input_path:
        output_path = os.path.join(os.path.dirname(input_path), "converted_jpgs")
        os.makedirs(output_path, exist_ok=True)
        try:
            convert_to_jpg(input_path, output_path)
            message_box = QMessageBox()
            message_box.setWindowTitle("Success")
            message_box.setText("Conversion complete.")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()
        except Exception as e:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText(f"An error occurred: {e}")
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec_()
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("Error")
        message_box.setText("No folder selected.")
        message_box.setIcon(QMessageBox.Warning)
        message_box.exec_()


if __name__ == "__main__":
    app = QApplication([])
    main()
