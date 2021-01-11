import sqlite3
import sys

import shutil
from random import random

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFileDialog, QInputDialog

from LOGIN import Logis
from REG import Regis


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.AP.hide()
        self.AB.hide()
        self.CB.hide()
        self.list_l = [self.L1, self.L2, self.L3, self.L4, self.L5, self.L6]
        self.REG.clicked.connect(self.runREG)
        self.LOG.clicked.connect(self.runLOG)
        self.AP.clicked.connect(self.addPict)
        self.BOR.clicked.connect(self.showBords)
        self.MAIN.clicked.connect(self.main)
        self.AB.clicked.connect(self.addBoard)
        self.CB.activated.connect(self.onChanged)


    def runREG(self):
        self.r = Regis(self, self.BOR, self.LOG)
        self.r.show()

    def runSHOW(self):
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        esult = cur.execute("SELECT p_adress FROM pict").fetchall()
        print(esult[0][0])


    def runLOG(self):
        self.l = Logis(self, self.BOR, self.LOG)
        self.l.show()

    def addPict(self):
        b = "/"
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]
        if fname != "":
            con = sqlite3.connect("pict.sqlite")
            cur = con.cursor()
            p_name = "C:\\Users\inok3\PycharmProjects\IndexProject-master\Pict" + "\\" + fname.split(b)[-1]
            cur.execute(f"""INSERT INTO pict(p_adress, name) VALUES('{p_name}','Избраное')""")
            con.commit()
            es = []
            con = sqlite3.connect("pict.sqlite")
            cur = con.cursor()
            for i in cur.execute(f"SELECT id_pict FROM pict WHERE p_adress = '{p_name}'").fetchall():
                es.append(i[0])
            print(es)
            t = []
            for i in cur.execute(f"SELECT id_board FROM board WHERE name = '{self.CB.currentText()}' AND autor = '{self.LOG.text()}'").fetchall():
                t.append(i[0])
            print(t)
            cur.execute(f"""INSERT INTO fromBortoPict(id_bord, id_pict) VALUES('{t[0]}','{es[0]}')""")
            shutil.copy(fname, "C:\\Users\inok3\PycharmProjects\IndexProject-master\Pict")
            con.commit()
            self.onChanged()

    def showBords(self):
        self.AP.show()
        self.AB.show()
        self.CB.show()
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        for i in cur.execute(f"""SELECT name FROM board WHERE autor = '{self.LOG.text()}'""").fetchall():
            self.CB.addItem(i[0])
        con.close()

    def addBoard(self):
        name , ok_pressed = QInputDialog.getText(
        self, "Добавить доску", "Введите название доски")
        if ok_pressed:
            con = sqlite3.connect("pict.sqlite")
            cur = con.cursor()
            cur.execute(f"""INSERT INTO board(autor, name) VALUES('{self.LOG.text()}','{name}')""")
            con.commit()
            self.CB.addItem(name)
            self.onChanged()

    def onChanged(self):
        for i in self.list_l:
            i.clear()
        print(self.CB.currentText())
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        self.list_p = []

        for n,i  in enumerate(cur.execute(f"""SELECT p_adress FROM pict 
        WHERE id_pict IN(SELECT id_pict FROM fromBortoPict
        WHERE id_bord IN(SELECT id_board FROM board WHERE autor = '{self.LOG.text()}'  AND name = '{self.CB.currentText()}' ))""").fetchall()):
            if n <= 5:
                 self.list_p.append(i[0])
        for i , QL in enumerate(self.list_p):
             self.pixmap = QPixmap(QL)
             self.smaller_pixmap = self.pixmap.scaled(341, 261, Qt.KeepAspectRatio, Qt.FastTransformation)
             self.list_l[i].setPixmap(self.smaller_pixmap)



    def main(self):
        print(self.CB.currentText())
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        self.list_p = []
        for i in cur.execute("SELECT p_adress FROM pict").fetchall():
            self.list_p.append(i[0])
        for i , QL in enumerate(self.list_l):
             self.pixmap = QPixmap(self.list_p[i])
             self.smaller_pixmap = self.pixmap.scaled(720, 480, Qt.KeepAspectRatio, Qt.FastTransformation)
             self.list_l[i].setPixmap(self.smaller_pixmap)

def except_hook(cls, exception, traceback):
        sys.excepthook(cls, exception, traceback)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = ex
    sys.exit(app.exec_())
