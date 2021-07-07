import pymongo
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

app = QApplication([])

consoleFont = QFontDatabase.addApplicationFont('./data/resources/fonts/Modeseven.ttf')
fontConsole = QFont('Modeseven',12)

class Game:
	class login_window(QWidget):
		def __init__(self):
			super().__init__()

			self.dlg = uic.loadUi('data/ui/login_scr.ui', self)
			self.dlg.setWindowFlags(Qt.FramelessWindowHint)
			self.dlg.exit_button.clicked.connect(self.close)
			self.dlg.minus_button.clicked.connect(self.dlg.showMinimized)
			self.show()

win = Game.login_window()
app.exec_()