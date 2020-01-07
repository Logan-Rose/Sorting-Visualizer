import gc
import sys
import time
from datetime import datetime
from random import shuffle

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui

size = 5

class MainWindow:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.givenImage = QPixmap('./Untitled2.png')
        self.givenImage = self.givenImage.scaled(640, 640, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.image_label.setPixmap(self.givenImage)
        self.split()

        self.mainGrid = QGridLayout()
        self.mainGrid.setSpacing(0)
        self.show()

        self.layout.addWidget(self.image_label)
        self.layout.addLayout(self.mainGrid)
        select = QPushButton("Select Image")
        self.choice = 0
        self.cb = QComboBox()
        self.options = ["Bubble Sort - O(n^2)", "Selection Sort - O(n^2)", "Insertion Sort - O(n^2) ", "Heap Sort - O(n*log(n))", "Merge Sort - O(n^2)"]
        self.cb.addItems(self.options)
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.layout.addWidget(self.cb)

        shufflebutton = QPushButton("Shuffle")
        shufflebutton.clicked.connect(self.randomize)
        sortbutton = QPushButton("Sort")
        sortbutton.clicked.connect(self.callsort)
        self.layout.addWidget(select)
        self.layout.addWidget(shufflebutton)
        self.layout.addWidget(sortbutton)
        self.window.setLayout(self.layout)

        self.window.show()
        self.app.exec_()

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    def selectionchange(self, i):
        print("Items in the list are :")
        self.choice = i
        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        print("Current index", i, "selection changed ", self.cb.currentText())

    def randomize(self):
        shuffle(self.chunktuples)
        self.show()

    def show(self):
        for i in range(len(self.chunktuples)):
            image_current = QLabel()
            currentImage = QPixmap(self.chunktuples[i][0])
            image_current.setPixmap(currentImage)
            self.mainGrid.addWidget(image_current, int(i/size), i%size)
        self.mainGrid.update()

    def split(self):
        width = self.givenImage.width()
        height = self.givenImage.height()
        stepX = width / size
        stepY = height / size
        xPos = stepX
        yPos = stepY
        self.chunktuples = []
        xIndex = 0
        yIndex = 0
        for i in range(size * size):
            cropped = self.givenImage.copy(QRect(int(xPos - stepX), int(yPos - stepY), int(stepX), int(stepY)))
            self.chunktuples.append((cropped, i))
            xIndex = xIndex + 1
            if xPos == width:
                xPos = 0
                xIndex = 0
                yPos = yPos + stepY
                yIndex = yIndex + 1
            xPos = xPos + stepX

    def callsort(self):
        if(self.choice ==0):
            self.bubblesort()
        elif(self.choice == 1):
            self.selectionsort()
        elif(self.choice == 2):
            self.insertionsort()
        elif(self.choice == 3):
            self.heapsort()
      #  elif(self.choise == 4):
      #      self.callmergesort()
      #  self.sort()

    def issorted(self):
        for i in range(len(self.chunktuples) - 1):
            if self.chunktuples[i][1] != i:
                return False
        return True

    def bubblesort(self):
        while self.issorted() is False:
            for i in range(len(self.chunktuples) - 1):
                if self.chunktuples[i][1] > self.chunktuples[i+1][1]:
                    temp = self.chunktuples[i]
                    self.chunktuples[i] = self.chunktuples[i + 1]
                    self.chunktuples[i + 1] = temp
                    self.app.processEvents()
            self.show()

    def selectionsort(self):
        for i in range(len(self.chunktuples) -1):
            k = i
            x = self.chunktuples[i]
            for j in range(i+1, len(self.chunktuples)):
                if self.chunktuples[j][1]< x[1]:
                    k = j
                    x = self.chunktuples[j]
            self.chunktuples[k] = self.chunktuples[i]
            self.chunktuples[i] = x
            self.app.processEvents()
            self.show()

    def insertionsort(self):
        for i in range(1, len(self.chunktuples)):
            x = self.chunktuples[i]
            j = i-1
            while x[1] < self.chunktuples[j][1] and j >=0:
                self.chunktuples[j+1] = self.chunktuples[j]
                j = j-1
            self.chunktuples[j + 1] = x
            self.app.processEvents()
            self.show()

    def heapsort(self):
        length = len(self.chunktuples)
        for i in range(length, -1, -1):
            self.heapify(length, i)
        for i in range(length -1, 0, -1):
            temp = self.chunktuples[0]
            self.chunktuples[0] = self.chunktuples[i]
            self.chunktuples[i] = temp
            self.heapify(i, 0)
            self.app.processEvents()
            self.show()

    def heapify(self, length, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < length and self.chunktuples[i][1] < self.chunktuples[left][1]:
            largest = left

        if right < length and self.chunktuples[largest][1] < self.chunktuples[right][1]:
            largest = right

        if largest != i:
            temp = self.chunktuples[i]
            self.chunktuples[i] = self.chunktuples[largest]
            self.chunktuples[largest] = temp
            self.heapify(length, largest)

x = MainWindow()
