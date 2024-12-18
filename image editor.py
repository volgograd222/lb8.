import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget, QPushButton, QFileDialog, QComboBox
from PyQt6.QtGui import QPixmap, QImage, QColor, QTransform
from PyQt6.QtCore import Qt

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("чина")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.adjust_opacity)

        self.rotate_left_button = QPushButton("повернуть в лево", self)
        self.rotate_left_button.clicked.connect(self.rotate_left)

        self.rotate_right_button = QPushButton("повернуть в право", self)
        self.rotate_right_button.clicked.connect(self.rotate_right)

        self.channel_selector = QComboBox(self)
        self.channel_selector.addItems(["дефолт", "красный", "зеленый", "голубой"])
        self.channel_selector.currentIndexChanged.connect(self.change_channel)

        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.opacity_slider)
        layout.addWidget(self.rotate_left_button)
        layout.addWidget(self.rotate_right_button)
        layout.addWidget(self.channel_selector)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.original_image = None
        self.current_image = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "open images", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.original_image = QImage(file_path)
            self.current_image = self.original_image
            self.update_image_display()

    def update_image_display(self):
        if self.current_image:
            pixmap = QPixmap.fromImage(self.current_image)
            self.image_label.setPixmap(pixmap)

    def adjust_opacity(self, value):
        if self.original_image:
            image = self.original_image.convertToFormat(QImage.Format.Format_ARGB32)
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    color.setAlpha(int(value * 2.55))
                    image.setPixel(x, y, color.rgba())
            self.current_image = image
            self.update_image_display()

    def rotate_left(self):
        if self.current_image:
            transform = QTransform().rotate(-90)
            self.current_image = self.current_image.transformed(transform)
            self.update_image_display()

    def rotate_right(self):
        if self.current_image:
            transform = QTransform().rotate(90)
            self.current_image = self.current_image.transformed(transform)
            self.update_image_display()

    def change_channel(self, index):
        if self.original_image:
            image = self.original_image.convertToFormat(QImage.Format.Format_ARGB32)
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    if index == 1:  # Red
                        color.setGreen(0)
                        color.setBlue(0)
                    elif index == 2:  # Green
                        color.setRed(0)
                        color.setBlue(0)
                    elif index == 3:  # Blue
                        color.setRed(0)
                        color.setGreen(0)
                    image.setPixel(x, y, color.rgba())
            self.current_image = image
            self.update_image_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec())