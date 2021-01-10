import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel


class Logis(QWidget):
    def __init__(self, *args):
        super().__init__()
        for i , el in enumerate(args):
            if i == 1:
                self.b = el
            elif i == 2:
                self.name = el
        uic.loadUi('log.ui', self)
        self.OK.clicked.connect(self.check)

    def check(self):
        self.LorN.setText("Введите логин или почту")
        self.LorN_2.setText("Введите пароль")
        lo = self.Nick.text()
        pa = self.Pas.text()
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        try:
            if self.check_acc(lo , pa)[1] == True:
                self.b.setEnabled(True)
                self.name.setText(self.check_acc(lo , pa)[0])
                self.hide()

        except IndexError:
            self.LorN.setText("Неверный формат")
        except NameError:
            self.LorN.setText("Такой пользователь не найден")
        con.close()

    def check_acc(self , l , p):
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        for i in cur.execute("SELECT * FROM acc").fetchall():
            if (l == i[1] or l == i[3]) and p == i[2]:
                return [i[3], True]
            elif (l == i[1] or l == i[3]) and p != i[2]:
                raise IndexError
        raise NameError






