import sys
from PyQt5.QtWidgets import QApplication, QDialog
import mainwindow


if __name__=='__main__':
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    ui = mainwindow.Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())