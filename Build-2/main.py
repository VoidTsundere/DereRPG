from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QFont, QFontDatabase, QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from sys import argv, exit
import sqlite3

conn = sqlite3.connect('data/data.dere')

app = QApplication(argv)

class game:
	class mainWindow(QWidget):
		
		def __init__(self):
			super().__init__()

			def runConsole():
				command = self.dlg.console.text()

				if 'exit' in command:
					self.dlg.close()

				if 'clear' in command:
					self.dlg.textBox.clear()

				if 'run' in command:
					commandZone = command.split(' ')
					if commandZone[1] == 'new':
						if commandZone[2] == 'save':
							try:
								playerName = commandZone[3]
							except:
								self.dlg.textBox.append("Use 'run new save (player name)'")

				self.dlg.console.clear()

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
			self.dlg.console.returnPressed.connect(runConsole)
			self.dlg.showMaximized()

			self.dlg.exit_button.clicked.connect(self.dlg.close)
			self.dlg.exit_button.setFont(self.fontConsole)
			self.dlg.exit_button.move(screen.size().width()-50,0)

			self.dlg.show()
		

		def keyPressEvent(self, event):
			if event.key() == QtCore.Qt.Key_Space:
				printt()

window = game.mainWindow()
exit(app.exec_())