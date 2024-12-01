import sys
from PyQt6 import uic
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Эспрессо')
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute("""SELECT roasting_degree FROM coffee""")
        mn = set()
        self.choose_st_ob.addItem('Любая')
        self.choose_type.addItem('Любой')
        self.choose_type.addItem('Молотый')
        self.choose_type.addItem('Зерновой')
        for elem in data:
            mn.add(elem[0])
        con.close()
        for elem in mn:
            self.choose_st_ob.addItem(elem)
        self.pushButton.clicked.connect(self.run)
    
    def run(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        sp_cond = []
        zapros = "SELECT * FROM coffee"
        if self.name_input.text() != '':
            sp_cond.append(f"name LIKE '%{self.name_input.text()}%'")
        if self.choose_st_ob.currentText() != 'Любая':
            sp_cond.append(f'roasting_degree = "{self.choose_st_ob.currentText()}"')
        if self.choose_type.currentText() != 'Любой':
            sp_cond.append(f'ground_or_grain = "{self.choose_type.currentText()}"')
        if len(sp_cond) > 0:
            zapros += ' WHERE '
            out = ' AND '.join(sp_cond)
            zapros += out
        print(zapros)
        res = cur.execute(zapros)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки',
                                                    'Молотый / в зёрнах', 'Описание вкуса',
                                                    'Цена, руб', 'Объём упаковки'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())