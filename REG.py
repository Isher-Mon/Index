import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel



class Regis(QWidget):
    def __init__(self, *args):
        for i , el in enumerate(args):
            if i == 1:
                self.b = el
            elif i == 2:
                self.name = el
        super().__init__()
        uic.loadUi('reg.ui', self)
        self.OK.clicked.connect(self.sd)

    def sd(self):

        lo = self.Nick.text()
        mail = self.Mail.text()
        con = sqlite3.connect("pict.sqlite")
        cur = con.cursor()
        esult = []
        login = []
        for i in cur.execute("SELECT mail FROM acc"):
            esult.append(i[0])
        for i in cur.execute("SELECT log FROM acc"):
            login.append(i[0])
        pas , rpas = self.Pas.text(), self.RePas.text()
        if ("@" in mail and mail.split("@")[1] == "yandex.ru") and mail not in esult:
            if(lo not in login):
                if pas != rpas:
                    try:
                        if check_pas:
                            cur.execute(f"""INSERT INTO acc(mail , pas , log) VALUES('{mail}','{pas}','{lo}')""")
                            cur.execute(f"""INSERT INTO board(autor , name) VALUES('{lo}','Избраное')""")
                            con.commit()
                            self.b.setEnabled(True)
                            self.name.setText(lo)
                            con.close()
                            self.hide()
                    except TypeError:
                        self.EPP.setText("Пароль слишком короткий")
                else:
                    self.EPP.setText("Пароли не совпадают")
            else:
                self.L1.setText("Такое имя уже занято")
        else:
            self.EM.setText("Неверный формат или такая почта уже зарегестрированна")




def check_pas(self , pas , rep_pas):
        lstr = ["qertyuiop", "asdfghjkl", "zxcvbnm",
            "йцукенгшщзхъ", "фывапролджэё", "ячсмитьбю"]
        if(len(pas) <= 8):
            raise TypeError
        t = [False, False, False]
        for i in pas:
            if i.islower() and not t[0]:
                t[0] = True
            if i.isupper() and not t[1]:
                t[1] = True
            if i.isdigit() and not t[2]:
                t[2] = True
        if all(t):
            raise TypeError
        g = False
        for o in lstr:
            for k, i in enumerate(o[2::1]):
                if o[k:k + 3] in pas.lower() and not g:
                    g = True
        if g:
            raise TypeError
        return True









