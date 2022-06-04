from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Game import Timer
class Act_Painter(QMainWindow):
    def __init__(self, _c, words):

        super().__init__()

        self._c = _c

        # setting title
        self.setWindowTitle("Paint with PyQt5")

        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)

        # creating image object
        self.image = QImage(self.size(), QImage.Format_RGB32)

        # making image color to white
        self.image.fill(Qt.white)

        # variables
        # drawing flag
        self.drawing = False
        self.start = False
        # default brush size
        self.brushSize = 5
        # default color
        self.brushColor = Qt.black

        # QPoint object to tract the point
        self.lastPoint = QPoint()
        # creating menu bar
        mainMenu = self.menuBar()

        # adding brush size to main menu
        b_size = mainMenu.addMenu("Brush Size")

        # adding brush color to ain menu
        b_color = mainMenu.addMenu("Brush Color")

        # creating file menu for save and clear action
        fileMenu = mainMenu.addMenu("clear")
        # creating clear action

        clearAction = QAction("Clear", self)
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(self.clear)
        # similarly repeating above steps for different color
        eraser = QAction("eraser", self)
        fileMenu.addAction(eraser)
        eraser.triggered.connect(self.whiteColor)

        # creating options for brush sizes
        # creating action for selecting pixel of 4px
        pix_4 = QAction("4px", self)
        # adding this action to the brush size
        b_size.addAction(pix_4)
        # adding method to this
        pix_4.triggered.connect(self.Pixel_4)

        # similarly repeating above steps for different sizes
        pix_7 = QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        # creating options for brush color
        # creating action for black color
        black = QAction("Black", self)
        # adding this action to the brush colors
        b_color.addAction(black)
        # adding methods to the black
        black.triggered.connect(self.blackColor)

        green = QAction("Green", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QAction("Yellow", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        blue = QAction("Blue", self)
        b_color.addAction(blue)
        blue.triggered.connect(self.blueColor)

        red = QAction("Red", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)
        self.menuBar().setDisabled(True)
        self.timer = None
        QMessageBox.information(self, "choose!!!",
                                "In the next window two words will be showed\nChoose the word you would like to paint")
        self.opOne = QPushButton(words[0], self)
        self.opTwo = QPushButton(words[1], self)

        self.UiComponents()

    def UiComponents(self):
        # creating a push button
        # setting geometry of button
        self.opOne.setGeometry(200, 150, 200, 60)
        self.opTwo.setGeometry(500, 150, 200, 60)

        # adding action to a button

        self.opOne.clicked.connect(self.click1)
        self.opTwo.clicked.connect(self.click2)

        # action method

    def click1(self):
        self.guessWord = self.opOne.text()
        self.startPaint()

    def click2(self):
        self.guessWord = self.opTwo.text()
        self.startPaint()

    def startPaint(self):

        self._c.send_request_to_server('w' + self.guessWord)
        self.timer = Timer.Timer()
        self.timer.show()
        self.start = True
        self.menuBar().setDisabled(False)
        self.opOne.hide()
        self.opTwo.hide()

    # method for checking mouse cicks
    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == Qt.LeftButton and self.start:
            # make drawing flag truipconfigipe
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # creating painter object
            painter = QPainter(self.image)

            # set the pen of the painter
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            # draw line from the last point of cursor to the current point
            # this will draw only one step

            painter.drawLine(self.lastPoint, event.pos())

            lst = [str(self.lastPoint.x()), str(self.lastPoint.y()), str(event.pos().x()), str(event.pos().y()),
                   str(self.brushColor), str(self.brushSize)]
            self.splitList(lst)

            # change the last point
            self.lastPoint = event.pos()
            # update

            self.update()

    def splitList(self, lst):
        str = ''
        for i in lst:
            str += i + ' '
        self._c.send_request_to_server(str)

        # method for mouse left button release

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # make drawing flag false

            self.drawing = False

    # paint event
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)

        # draw rectangle  on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for clearing every thing on canvas
    def clear(self):
        print(55)
        self._c.send_request_to_server("clear")
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()

    # methods for changing pixel sizes
    def Pixel_4(self):
        self.brushSize = 5

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    # methods for changing brush color
    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def redColor(self):
        self.brushColor = Qt.red

    def blueColor(self):
        self.brushColor = Qt.blue
