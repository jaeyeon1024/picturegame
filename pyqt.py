import sys
import cv2
import Main
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

first_path = r"C:\Labs\picture_game\pyqt_img\first.jpg"
second_path = r"C:\Labs\picture_game\pyqt_img\second.jpg"

class DragandDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop')
        self.setGeometry(1000,250,300,300)
        self.setFixedSize(300,300)
        self.setAcceptDrops(True)

        self.setup()
        self.show()
    def setup(self):
        self.target_label = QLabel(self)
        self.target_label.setText('Drag Image Here')
        main_box = QVBoxLayout()
        main_box.addWidget(self.target_label)
        
        self.setLayout(main_box)

    def dragEnterEvent(self, e):
        if e.mimeData().hasImage:
            e.setAccepted(True)
        else:
            e.setAccepted(False)
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            image_path = event.mimeData().urls()[0].toLocalFile()
            
            self.setImage(image_path)
            event.setAccepted(True)
        else:
            event.setAccepted(False)
    

    def setImage(self, image_path):
        self.target_label.setPixmap(QPixmap(image_path))
        self.target_label.setScaledContents(True)
        self.show_second_window(image_path)
    
    def show_second_window(self,image_path):
        self.second = secondwindow(image_path)
        self.second.show()
        
class secondwindow(QMainWindow):
    def __init__(self,image_path):
        super().__init__()
        self.image_path = image_path
        self.initUI()
    def initUI(self):
        self.setWindowTitle('find Picture')
        self.setGeometry(700,250,300,300)
        self.setFixedSize(300,550)
        self.setup()
        self.show()

        
    def setup(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        

        self.img, self.background = Main.create(self.image_path)

        cv2.imwrite(first_path, self.img)
        cv2.imwrite(second_path, self.img)

        self.show_image_before()

    def show_image_before(self):
        pixmap = QPixmap(first_path)
        self.label1.setPixmap(pixmap)
        self.label1.setScaledContents(True)
        self.label1.resize(pixmap.width()+10,pixmap.height()+10)
        self.label1.show()
        self.rgb_changer()
    
    def show_image_after(self):
        Main.print_pexels(self.img,self.background,self.rgb,second_path)
        pixmap = QPixmap(second_path)
        self.label2.setPixmap(pixmap)
        self.label2.setScaledContents(True)
        self.label2.resize(pixmap.width()+10,pixmap.height()+10)
        self.label2.move(0,pixmap.height()+10)
        self.label2.show()

    def rgb_changer(self):
        self.changer = changer_rgb()
        self.changer.show()
        self.changer.commit_box.clicked.connect(self.commit)
    def commit(self):
        self.rgb = self.changer.rgb
        self.show_image_after()


class changer_rgb(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('RGB Changer')
        self.setGeometry(1000,580,300,300)
        self.setFixedSize(300,220)
        self.setup()
        self.show()
    def setup(self):
        self.slider_setup()
        self.set_label()
        self.rgb = [0,0,0]
        main_layout = QVBoxLayout()
        self.color_border = QLabel(self)
        self.color_border.setFixedSize(280,50)
        self.color_border.setStyleSheet("background-color:rgb({red},{green},{blue});".format(red = self.rgb[0],green = self.rgb[1],blue = self.rgb[2]))
        main_layout.addWidget(self.color_border)

        layout = QGridLayout()

        layout.addWidget(self.label1,0,0)
        layout.addWidget(self.slider_red,0,1)
        layout.addWidget(self.label2,1,0)
        layout.addWidget(self.slider_green,1,1)
        layout.addWidget(self.label3,2,0)
        layout.addWidget(self.slider_blue,2,1)

        main_layout.addLayout(layout)

        self.color_border.setStyleSheet("background-color:rgb({red},{green},{blue});".format(red = self.rgb[0],green = self.rgb[1],blue = self.rgb[2]))

        self.commit_box = QPushButton('Commit',self)
        
        main_layout.addWidget(self.commit_box)
        self.setLayout(main_layout)
    
    def set_label(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        
        self.label1.setText('Red')
        self.label2.setText('Green')
        self.label3.setText('Blue')
        
    def slider_setup(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.slider_red = QSlider(Qt.Horizontal,self)
        self.slider_red.setRange(0,255)
        self.slider_red.setSingleStep(1)
        self.slider_red.setValue(0)
        
        self.slider_green = QSlider(Qt.Horizontal,self)
        self.slider_green.setRange(0,255)
        self.slider_green.setSingleStep(1)
        self.slider_green.setValue(0)

        self.slider_blue = QSlider(Qt.Horizontal,self)
        self.slider_blue.setRange(0,255)
        self.slider_blue.setSingleStep(1)
        self.slider_blue.setValue(0)

        self.slider_red.valueChanged.connect(self.slider_changed_red)
        self.slider_green.valueChanged.connect(self.slider_changed_green)
        self.slider_blue.valueChanged.connect(self.slider_changed_blue)

    def slider_changed_red(self):
        self.red = self.slider_red.value()
        self.rgb = [self.red,self.green,self.blue]
        self.color_border.setStyleSheet("background-color:rgb({red},{green},{blue});".format(red = self.rgb[0],green = self.rgb[1],blue = self.rgb[2]))
    def slider_changed_green(self):
        self.green = self.slider_green.value()
        self.rgb = [self.red,self.green,self.blue]        
        self.color_border.setStyleSheet("background-color:rgb({red},{green},{blue});".format(red = self.rgb[0],green = self.rgb[1],blue = self.rgb[2]))
    def slider_changed_blue(self):
        self.blue = self.slider_blue.value()
        self.rgb = [self.red,self.green,self.blue]
        self.color_border.setStyleSheet("background-color:rgb({red},{green},{blue});".format(red = self.rgb[0],green = self.rgb[1],blue = self.rgb[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragandDrop()
    sys.exit(app.exec_())