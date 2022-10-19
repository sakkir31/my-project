import sys
import random
import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPlainTextEdit,
    QFileDialog,
    QStackedWidget,
    
)

from vigenere import *
from playfair import *
from fullvigenere import *
from hill import *
from affine import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MUSAKKIR NOMPO")

        hbox = QHBoxLayout()
        layout = QVBoxLayout()
        
        self.label1 = QLabel("Jenis Cipher:")
        self.jeniscipher = QComboBox()
        self.jeniscipher.addItems(["Vigénere", "Full Vigénere", "Auto-key Vigénere", "Extended Vigénere", "Playfair", "Affine", "Hill"])


        self.spasi = QCheckBox("Tambahkan spasi di cipherteks")

        
        self.label2 = QLabel("Input:")
        self.inputfield = QPlainTextEdit()

        self.label3 = QLabel("Output:")
        self.outputfield = QPlainTextEdit()
        self.outputfield.setReadOnly(True)


        self.bukafile = QPushButton("Berkas...")
        self.labelpath = QLabel("")
        self.bukafile.clicked.connect(self.open)
        self.bukafile2 = QPushButton("Simpan...")
        self.bukafile2.clicked.connect(self.simpanhasil)
        
        self.label4 = QLabel()
        self.enkripsi = QPushButton("Enkripsi")
        self.enkripsi.clicked.connect(self.fungsi_enkripsi)
        self.dekripsi = QPushButton("Dekripsi")
        self.dekripsi.clicked.connect(self.fungsi_dekripsi)

        self.enkripsi.setStyleSheet("background-color : #98d6ed")
        self.dekripsi.setStyleSheet("background-color : #98d6ed")

        # Extra fields
        self.vigenere_kunci = QLineEdit()
        self.shiftnum = QLineEdit()
        self.onlyInt = QIntValidator()
        self.shiftnum.setValidator(self.onlyInt)
        self.tabel = QPlainTextEdit()
        self.matriks = QPlainTextEdit()
        self.full_kunci = QLineEdit()
        self.relatifprima = QComboBox()
        self.binaryfile = ''
        self.relatifprima.addItems(["1","3","5","7","9","11","15","17","19","21","23","25"])

        # Buttons
        self.generate = QPushButton("Buat tabel acak")
        self.generate.clicked.connect(self.shuffleAZ)
        self.importabel = QPushButton("Impor tabel...")
        self.importabel.clicked.connect(self.loadtabel)
        self.eksportabel = QPushButton("Ekspor tabel...")
        self.eksportabel.clicked.connect(self.savetabel)

        
        # Buat menu beda sesuai jenis cipher
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.layout1()
        self.layout2()
        self.layout3()
        self.layout4()
        self.stack = QStackedWidget (self)
        self.stack.addWidget (self.stack1)
        self.stack.addWidget (self.stack2)
        self.stack.addWidget (self.stack3)
        self.stack.addWidget (self.stack4)

        

        self.jeniscipher.currentIndexChanged.connect(self.changemenus)

        

        # Masukkan menu ganti cipher
        #layout.addWidget(self.label1)
        #layout.addWidget(self.jeniscipher)
        #layout.addWidget(self.stack)
        layout.addWidget(self.spasi)
        layout.addWidget(self.label2)
        layout.addWidget(self.inputfield)
        layout.addWidget(self.bukafile)
        layout.addWidget(self.labelpath)
        layout.addWidget(self.label3)
        layout.addWidget(self.outputfield)
        layout.addWidget(self.bukafile2)
        layout.addWidget(self.label4)
        #layout.addWidget(self.enkripsi)
        #layout.addWidget(self.dekripsi)

        widget = QWidget()
        hbox.addLayout(layout)
        hbox.addWidget(self.stack)
        layoutall = QVBoxLayout()
        layoutall.addWidget(self.label1)
        layoutall.addWidget(self.jeniscipher)
        layoutall.addLayout(hbox)
        layoutall.addWidget(self.enkripsi)
        layoutall.addWidget(self.dekripsi)
        widget.setLayout(layoutall)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def layout1(self):
        # Layout 1. Vignere Cipher
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 23, 0, 0)

        
        labelkey = QLabel("Kunci:")
        
        layout.addWidget(labelkey)
        layout.addWidget(self.vigenere_kunci)
        layout.setAlignment(Qt.AlignTop)
        
        
        self.stack1.setLayout(layout)


    def layout2(self):
        # Layout 2. Full Vignere Cipher
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 23, 0, 19)

        labelkey = QLabel("Kunci:")
        

        tabel = QLabel("Tabel Huruf:")
        hbox = QHBoxLayout()
        hbox.addWidget(self.importabel)
        hbox.addWidget(self.eksportabel)
        

        layout.addWidget(labelkey)
        layout.addWidget(self.full_kunci)
        layout.addWidget(tabel)
        layout.addWidget(self.tabel)
        layout.addLayout(hbox)
        layout.addWidget(self.generate)
        layout.setAlignment(Qt.AlignTop)
        

        self.stack2.setLayout(layout)

    def layout3(self):
        # Layout 3. Affine Cipher
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 23, 0, 0)

        labelkey = QLabel("Shift:")
        

        prima = QLabel("Angka relatif prima:")
        

        layout.addWidget(labelkey)
        layout.addWidget(self.shiftnum)
        layout.addWidget(prima)
        layout.addWidget(self.relatifprima)
        layout.setAlignment(Qt.AlignTop)
        

        self.stack3.setLayout(layout)

    def layout4(self):
        # Layout 4. Hill Cipher
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 23, 0, 19)

        labelkey = QLabel("Matriks Kunci:")

        layout.addWidget(labelkey)
        layout.addWidget(self.matriks)
        layout.setAlignment(Qt.AlignTop)
        

        self.stack4.setLayout(layout)


    def changemenus(self, s):
        # Untuk ganti menu saat mengubah jenis cipher
        index = self.jeniscipher.currentIndex()
        #print("Current index:", index)
        if index == 1:
            self.stack.setCurrentIndex(1)
        elif index == 5:
            self.stack.setCurrentIndex(2)
        elif index == 6:
            self.stack.setCurrentIndex(3)
        else:
            self.stack.setCurrentIndex(0)

        if index == 3:
            self.inputfield.setDisabled(True)
        else:
            self.inputfield.setDisabled(False)


    def fungsi_enkripsi(self):
        index = self.jeniscipher.currentIndex()
        teksinput = self.inputfield.toPlainText()
        output = ''
        content = ''
        isbinary = False
        
        if index == 0:
            tekskunci = self.vigenere_kunci.text()
            output = vigenere(tekskunci, teksinput, True, False)

        elif index == 1:
            tekskunci = self.full_kunci.text()
            tabel = self.tabel.toPlainText()
            output = fullvigenere(tekskunci, teksinput, tabel, True)

        elif index == 2:
            tekskunci = self.vigenere_kunci.text()
            output = vigenere(tekskunci, teksinput, True, True)

        elif index == 3:
            tekskunci = self.vigenere_kunci.text()
            instring = []
            
            if os.path.exists(teksinput):
                isbinary = True
                with open(teksinput, 'rb') as f:
                    #byte = f.read(1)
                    #while byte:
                        #instring += chr(ord(byte))
                        #byte = f.read(1)
                    #encrypted = vigenere(tekskunci, instring, True, False, True)
                    #self.binaryfile = encrypted
                    byte = f.read(1)
                    while byte:
                        instring.append(int.from_bytes(byte, "big"))   
                        byte = f.read(1)
                    encrypted = bytearray(vigenerebin(tekskunci, instring, True))
                    self.binaryfile = encrypted

            else:
                output = vigenere(tekskunci, teksinput, True, False)
            

        elif index == 4:
            tekskunci = self.vigenere_kunci.text()
            output = playfair_cipher(teksinput, tekskunci).upper()
        
        elif index == 5:
            shift = int(self.shiftnum.text())
            relprime = int(self.relatifprima.currentText())
            output = affine_cipher(teksinput, relprime, shift).upper()

        elif index == 6:
            teksmatriks = self.matriks.toPlainText()
            output = hill(teksinput, teksmatriks, True)
            
        # Tambah spasi jika opsi dipilih
        if self.spasi.isChecked():
            output = ' '.join(output[i:i+5] for i in range(0,len(output),5))
            
        if index == 3 and isbinary:
            output = 'Berkas telah dienkripsi. Silakan unduh dengan tombol "Simpan..."'

        self.outputfield.setPlainText(output)

    def fungsi_dekripsi(self):
        index = self.jeniscipher.currentIndex()
        teksinput = self.inputfield.toPlainText()
        output = ''
        isbinary = False
        
        
        if index == 0:
            tekskunci = self.vigenere_kunci.text()
            output = vigenere(tekskunci, teksinput, False, False)

        elif index == 1:
            tekskunci = self.full_kunci.text()
            tabel = self.tabel.toPlainText()
            output = fullvigenere(tekskunci, teksinput, tabel, False)

        elif index == 2:
            tekskunci = self.vigenere_kunci.text()
            output = vigenere(tekskunci, teksinput, False, True)

        elif index == 3:
            tekskunci = self.vigenere_kunci.text()
            instring = []
            
            if os.path.exists(teksinput):
                with open(teksinput, 'rb') as f:
                    isbinary = True
                    #byte = f.read(1)
                    #while byte:
                        #instring += chr(ord(byte))
                        #byte = f.read(1)
                    #encrypted = vigenere(tekskunci, instring, True, False, True)
                    #self.binaryfile = encrypted
                    byte = f.read(1)
                    while byte:
                        instring.append(int.from_bytes(byte, "big"))   
                        byte = f.read(1)
                    encrypted = bytearray(vigenerebin(tekskunci, instring, False))
                    self.binaryfile = encrypted

            else:
                output = vigenere(tekskunci, teksinput, False, False)
            
        elif index == 4:
            tekskunci = self.vigenere_kunci.text()
            output = playfair_decipher(teksinput, tekskunci).upper()
        
        elif index == 5:
            shift = int(self.shiftnum.text())
            relprime = int(self.relatifprima.currentText())
            output = affine_decipher(teksinput, relprime, shift).upper()
            
        elif index == 6:
            teksmatriks = self.matriks.toPlainText()
            output = hill(teksinput, teksmatriks, False)

        if index == 3 and isbinary:
            output = 'Berkas telah didekripsi. Silakan unduh dengan tombol "Simpan..."'

        self.outputfield.setPlainText(output)

    def open(self):
        fileName = ''
        index = self.jeniscipher.currentIndex()
        if index != 3:
            fileName, _ = QFileDialog.getOpenFileName(self, 'File Input','.', "Text Files (*.txt)")
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, 'File Input')
        content = ''
        if fileName:
            if fileName.endswith('.txt'):
               # File txt
               with open(fileName, 'r', encoding='ISO-8859-1') as f:
                   content = f.read()
                   self.inputfield.setPlainText(content)
            else:
                # File biner
                #with open(fileName, 'rb') as f:
                   #bytecontent = f.read()
                self.inputfield.setPlainText(fileName)

    def shuffleAZ(self):
        # Buat tabel huruf random untuk cipher Full Vigenere
        alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shuffled = ''.join(random.sample(alfabet,len(alfabet)))
        content = shuffled
        for i in range(26):
            shuffled = ''.join(random.sample(alfabet,len(alfabet)))
            content += '\n'
            content += shuffled
        
        self.tabel.setPlainText(content)

    def loadtabel(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Load Tabel','.', "Text Files (*.txt)")
        content = ''
        # File txt
        if fileName:
            with open(fileName, 'r') as f:
                content = f.read()
                self.tabel.setPlainText(content)

    def savetabel(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save Tabel', 'tabel.txt')
        if fileName:
            tabel = self.tabel.toPlainText()
            fname = open(fileName, 'w')
            fname.write(tabel)
            fname.close()

    def simpanhasil(self):
        index = self.jeniscipher.currentIndex()
        if index == 3 and os.path.exists(self.inputfield.toPlainText()):
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save Output', 'output')
            if(fileName):
                output = self.binaryfile
                fname = open(fileName, 'wb')
                fname.write(output)
                fname.close()
        else:
            fileName, _ = QFileDialog.getSaveFileName(self, 'Save Output', 'output.txt')
            if(fileName):
                output = self.outputfield.toPlainText()
                fname = open(fileName, 'w')
                fname.write(output)
                fname.close()

    


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
