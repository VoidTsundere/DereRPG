from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from sys import argv, exit

app = QApplication(argv)

class game:
	class mainWindow(QMainWindow):
		
		def __init__(self):
			QMainWindow.__init__(self)

			screen = app.primaryScreen()
			self.dlg = uic.loadUi('data/ui/main.ui')
			self.consoleFont = QFontDatabase.addApplicationFont('./data/ui/Modeseven.ttf')
			self.fontConsole = QFont('Modeseven',12)
			self.dlg.textBox.setFont(self.fontConsole)

			self.dlg.console.move(0,screen.size().height()-70)
			self.dlg.console.setFixedSize(screen.size().width(),31)
			self.dlg.console.setFont(self.fontConsole)
			self.dlg.console.installEventFilter(self)

			self.dlg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
			self.dlg.showMaximized()

			self.dlg.show()
			print(screen.size().width())

		def keyEvent(self, event):
			print('defff')


window = game.mainWindow()
exit(app.exec_())