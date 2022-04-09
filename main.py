import sys
from PyQt5.QtWidgets import *
import numpy as np
import re
import string


class App(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Analiza'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.fileName = ''
        self.tabela_slow = []

        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

        # pola
        self.pole_tekstowe = QTextEdit(self)
        self.litera = QLineEdit(self)
        self.napis = QLabel(self)
        self.pole_wyniku = QLabel(self)
        self.przycisk = QPushButton('sortuj', self)
        self.przycisk.clicked.connect(self.how_many_starts_with)

        # text
        self.pole_tekstowe.setReadOnly(True)

        # menu
        menu = self.menuBar()
        file_menu = menu.addMenu("Plik")
        search_menu = menu.addMenu("Wyszukaj")
        policz_slowa = QAction('policz', self)
        policz_slowa.triggered.connect(self.word_lenght)
        start_with = QAction('zaczyna', self)
        start_with.triggered.connect(self.word_starts_at)
        ends_with = QAction('kończy', self)
        ends_with.triggered.connect(self.words_ends_with)
        value_starts_with = QAction('liczba', self)
        value_starts_with.triggered.connect(self.how_many_starts_with)
        search_menu.addAction(policz_slowa)
        search_menu.addAction(start_with)
        search_menu.addAction(ends_with)
        search_menu.addAction(value_starts_with)
        open_file = QAction('otwórz', self)
        open_file.triggered.connect(self.open)
        file_menu.addAction(open_file)

        # Qlabel
        self.napis.setText('litera do sorowania:')

        # laoyout
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()

        layout2.addWidget(self.napis)
        layout2.addWidget(self.litera)
        layout2.addWidget(self.przycisk)
        layout1.addLayout(layout2)
        layout1.addWidget(self.pole_wyniku)
        layout1.addWidget(self.pole_tekstowe)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout1)
        self.show()

    def open(self):
        option = QFileDialog.Options()
        self.fileName = QFileDialog.getOpenFileName(self, filter='*.txt', options=option)
        file_text = open(self.fileName[0])
        self.pole_tekstowe.setText(file_text.read())

    def word_lenght(self):
        if self.fileName == "":
            self.pole_wyniku.setText('Otwórz najpierw plik na którym amm pracować!')
            return
        self.strip_words()
        ilosc_liter = np.zeros(15)
        for i in range(0, len(self.tabela_slow), 1):
            for j in range(1, 15):
                if len(self.tabela_slow[i]) == j:
                    ilosc_liter[j] = ilosc_liter[j] + 1
        nieposortowana_liczba = []
        for i in range(0, 15, 1):
            nieposortowana_liczba.append(ilosc_liter[i])
        ilosc_liter.sort()
        for i in range(0, 15, 1):
            if nieposortowana_liczba[i] == ilosc_liter[-1]:
                self.pole_wyniku.setText("Najwięcej słów w tym tekście ma rozmiar: " + str(i + 1))

    def word_starts_at(self):
        if self.fileName == "":
            self.pole_wyniku.setText('Otwórz najpierw plik na którym amm pracować!')
            return
        self.strip_words()
        alfabet = string.ascii_lowercase
        tab_value = []
        alf = []
        for a in alfabet:
            tab = 0
            for b in self.tabela_slow:
                if b.startswith(a) or b.startswith(a.capitalize()):
                    tab = tab + 1
            tab_value.append(tab)
            alf.append(a)
        diction = zip(tab_value, alf)
        dictionary = dict(diction)
        dictionary = dict(sorted(dictionary.items(), key=lambda item: item[0], reverse=True))
        tab_value = list(dictionary.values())
        self.pole_wyniku.setText("najwęcej słów rozpoczyna się na literę: " + tab_value[0])

    def words_ends_with(self):
        if self.fileName == "":
            self.pole_wyniku.setText('Otwórz najpierw plik na którym amm pracować!')
            return
        self.strip_words()
        alfabet = string.ascii_lowercase
        tab_value = []
        alf = []
        for a in alfabet:
            tab = 0
            for b in self.tabela_slow:
                if b.endswith(a) or b.endswith(a.capitalize()):
                    tab = tab + 1
            tab_value.append(tab)
            alf.append(a)
        diction = zip(tab_value, alf)
        dictionary = dict(diction)
        dictionary = dict(sorted(dictionary.items(), key=lambda item: item[0], reverse=True))
        tab_value = list(dictionary.values())
        self.pole_wyniku.setText("najwęcej słów kończy się na literę: " + tab_value[0])

    def how_many_starts_with(self):
        if self.fileName == "":
            self.pole_wyniku.setText('Otwórz najpierw plik na którym amm pracować!')
            return
        if(self.litera.text()):
            self.pole_wyniku.setText("Podaj jedną literę")
        self.strip_words()
        letter = self.litera.text()
        value = 0
        tab = map(lambda word: word.startswith(letter), self.tabela_slow)
        for a in tab:
            if a == True:
                value = value + 1
        self.pole_wyniku.setText("na podaną frazę zaczyna się " + str(value) + " słów")

    def strip_words(self):
        file_text = open(self.fileName[0])
        self.tabela_slow = re.findall("[a-zA-Z]+", file_text.read())


app = QApplication(sys.argv)
ex = App()
app.exec_()
