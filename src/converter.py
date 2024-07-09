import sys
import os
from PIL import Image
import pillow_heif
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QProgressBar,
    QListWidget,
    QMessageBox,
    QComboBox,
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon


class ConversionThread(QThread):
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    def __init__(self, input_path, output_path, output_format):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    def run(self):
        try:
            files = [
                f
                for f in os.listdir(self.input_path)
                if f.lower().endswith((".heic", ".heif"))
            ]
            total_files = len(files)

            for i, filename in enumerate(files, 1):
                filepath = os.path.join(self.input_path, filename)
                heif_file = pillow_heif.read_heif(filepath)
                image = Image.frombytes(
                    heif_file.mode, heif_file.size, heif_file.data, "raw"
                )
                output_filename = (
                    os.path.splitext(filename)[0] + f".{self.output_format.lower()}"
                )
                output_path_new = os.path.join(self.output_path, output_filename)
                if self.output_format.upper() == "JPG":
                    image.save(output_path_new, format="JPEG")
                else:
                    image.save(output_path_new, format=self.output_format.upper())
                self.progress.emit(int((i / total_files) * 100))

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapShift")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("src/assets/icon.ico"))
        main_layout = QVBoxLayout()

        # Input folder selection
        input_layout = QHBoxLayout()
        self.input_label = QLabel("Input Folder:")
        self.input_path = QLabel("Not selected")
        self.input_button = QPushButton("Browse")
        self.input_button.clicked.connect(self.choose_input_folder)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.input_button)

        # Output folder selection
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output Folder:")
        self.output_path = QLabel("Not selected")
        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.choose_output_folder)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.output_button)

        # Output format selection
        format_layout = QHBoxLayout()
        self.format_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPG", "PNG", "WebP", "BMP", "TIFF"])
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)

        # File list
        self.file_list = QListWidget()

        # Progress bar
        self.progress_bar = QProgressBar()

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setEnabled(False)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(format_layout)
        main_layout.addWidget(self.file_list)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.convert_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def choose_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Input Folder")
        if folder:
            self.input_path.setText(folder)
            self.update_file_list()
            self.check_convert_button()

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Output Folder")
        if folder:
            self.output_path.setText(folder)
            self.check_convert_button()

    def update_file_list(self):
        self.file_list.clear()
        input_folder = self.input_path.text()
        if os.path.isdir(input_folder):
            files = [
                f
                for f in os.listdir(input_folder)
                if f.lower().endswith((".heic", ".heif"))
            ]
            self.file_list.addItems(files)

    def check_convert_button(self):
        self.convert_button.setEnabled(
            os.path.isdir(self.input_path.text())
            and os.path.isdir(self.output_path.text())
            and self.file_list.count() > 0
        )

    def start_conversion(self):
        output_format = self.format_combo.currentText()
        self.conversion_thread = ConversionThread(
            self.input_path.text(), self.output_path.text(), output_format
        )
        self.conversion_thread.progress.connect(self.update_progress)
        self.conversion_thread.finished.connect(self.conversion_finished)
        self.conversion_thread.error.connect(self.conversion_error)

        self.convert_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.conversion_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        QMessageBox.information(self, "Success", "Conversion completed successfully!")
        self.convert_button.setEnabled(True)

    def conversion_error(self, error_message):
        QMessageBox.warning(self, "Error", f"An error occurred: {error_message}")
        self.convert_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
