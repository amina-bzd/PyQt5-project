from ctypes import alignment
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from scipy.misc import central_diff_weights


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Image Filter")
        self.setMinimumSize(800, 400)
        
        self.menu = self.menuBar().addMenu("File")
        
        self.load_action = QAction("Open", self)
        self.load_action.triggered.connect(self.load_image)
        self.menu.addAction(self.load_action)
        
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_image)
        self.menu.addAction(self.save_action)
        
        self.original_label = QLabel()
        self.original_label.setFixedSize(400, 200)
        
        self.filtered_label = QLabel()
        self.filtered_label.setFixedSize(400, 200)
        
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.original_label)
        
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.load_image)
        left_vbox.addWidget(self.open_button)
        
        left_widget = QWidget()
        left_widget.setLayout(left_vbox)
        
        right_vbox = QVBoxLayout()
        right_vbox.addWidget(self.filtered_label)
        
        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_image)
        right_vbox.addWidget(self.filter_button)
        
        right_widget = QWidget()
        right_widget.setLayout(right_vbox)
        
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        
        hbox = QHBoxLayout()
        hbox.addWidget(left_widget)
        hbox.addWidget(line)
        hbox.addWidget(right_widget)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        
        
        widget = QWidget()
        widget.setLayout(vbox)
        
        self.setCentralWidget(widget)
    
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files (*.jpg *.jpeg *.png)")
        if file_name:
          self.image = cv2.imread(file_name, cv2.IMREAD_COLOR)
          self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
          self.original_label.setPixmap(self.get_pixmap(self.image))
          self.filtered_label.clear()
    ''' def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files (*.jpg *.jpeg *.png)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.original_label.setPixmap(self.get_pixmap(self.image))
            self.filtered_label.clear() '''
            
    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", ".", "Image Files (*.jpg *.jpeg *.png)")
        if file_name:
            pixmap = self.filtered_label.pixmap()
            pixmap.save(file_name)
            
    def filter_image(self):
        if hasattr(self, "image"):
            filtered_image = self.smoothing_filter(self.image)
            self.filtered_label.setPixmap(self.get_pixmap(filtered_image))
            
    def smoothing_filter(self, image):
        filtered_image = cv2.GaussianBlur(image, (5, 5), 0)
        return filtered_image
    
    ''' def get_pixmap(self, image):
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg) '''
    def get_pixmap(self, image):
        if len(image.shape) == 2:  # Grayscale image
           height, width = image.shape
           bytes_per_line = width
           q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:  # BGR image
           height, width, channels = image.shape
           bytes_per_line = channels * width
           q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        return QPixmap.fromImage(q_image)

    def resize_images(self):
        if hasattr(self, "image"):
            size = int(self.slider.value()) * 30
            original_image = cv2.resize(self.image, (size, size))
            filtered_image = cv2.resize(self.filtered_label.pixmap().toImage().bits().asstring(), (size, size))
            self.original_label.setPixmap(self.get_pixmap(original_image))
            self.filtered_label.setPixmap(self.get_pixmap(filtered_image))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
