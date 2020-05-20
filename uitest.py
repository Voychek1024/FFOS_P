import sys

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidget, QTableWidgetItem
from uidesign import *
from pop import *
x = 0


class MyDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.submit)
        self.pushButton_2.clicked.connect(self.reject)
        self.spinBox.setValue(0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Set Value')

    def submit(self):
        # value = self.spinBox.value()
        # print('submit item', value)
        QDialog.close(self)


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.store1)
        self.pushButton_2.clicked.connect(self.store2)
        self.pushButton_3.clicked.connect(self.store3)
        self.pushButton_4.clicked.connect(self.order)
        self.treeWidget.itemDoubleClicked.connect(self.onclick)
        self.tableWidget.removeRow(0)
        self.total = 0
        self.dialogwindow = MyDialog(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Message box')
        self.show()

    def store1(self):
        image = QtGui.QImage(QtGui.QImageReader("./picture/mc.png").read())
        self.label_2.setPixmap(QtGui.QPixmap(image))
        self.initree(1)

    def store2(self):
        image = QtGui.QImage(QtGui.QImageReader("./picture/kfc.png").read())
        self.label_2.setPixmap(QtGui.QPixmap(image))
        self.initree(2)

    def store3(self):
        image = QtGui.QImage(QtGui.QImageReader("./picture/bk.png").read())
        self.label_2.setPixmap(QtGui.QPixmap(image))
        self.initree(3)

    def initree(self, index):
        self.treeWidget.clear()
        # '''
        for i in range(index-1, index+1):
            parent_it = QtWidgets.QTreeWidgetItem(["Group {}".format(i)])
            self.treeWidget.addTopLevelItem(parent_it)
            for j in range(index-1, index+2):
                it = QtWidgets.QTreeWidgetItem(["{}{}".format(i, j), "{}".format(index)])
                parent_it.addChild(it)
        self.treeWidget.expandAll()

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onclick(self, item, col):
        # print('You Clicked', item.text(col), col)
        self.dialogwindow.exec_()
        global x
        value = self.dialogwindow.spinBox.value()
        if value > 0:
            # print(value)
            self.dialogwindow.spinBox.setValue(0)

            self.tableWidget.insertRow(x)
            self.tableWidget.setItem(x, 0, QTableWidgetItem("{}".format(item.text(col))))
            self.tableWidget.setItem(x, 1, QTableWidgetItem("{}".format(item.text(col+1))))
            self.tableWidget.setItem(x, 2, QTableWidgetItem("{}".format(value)))
            x += 1
        self.total += (int(item.text(col+1))*value)
        self.lcdNumber.display(self.total)

    def order(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Please Confirm Your Order.\n"
                                     "Are you sure to order?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # print('Ordering...')
            with open("tip.txt", "w") as f:
                f.write("----Order List----")
                f.write("\nItem\tPrice\tNumber\n")
                for row_index in range(self.tableWidget.rowCount()):
                    for column_index in range(self.tableWidget.columnCount()):
                        f.write(self.tableWidget.item(row_index, column_index).text() + "\t")
                    f.write("\n")
                f.write("\nTotal：" + "￥" + str(self.total) )
            f.close()
        else:
            QMessageBox.close


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.setWindowTitle('Customer Order')
    myWin.setWindowIcon(QtGui.QIcon('./picture/Order.png'))
    myWin.show()
    sys.exit(app.exec_())