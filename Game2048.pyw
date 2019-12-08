import sys, random
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)

class MyButton(QPushButton):

	def __init__(self):
		super().__init__()

	def mousePressEvent(self, event):
		button = event.button()
		if button == Qt.RightButton:
			if self.text() != '' and int(self.text()) >= 4:
				#self.setText(str(int(int(self.text()) / 2)))
				self.setText(str(int(self.text()) // 2))
				Example.ChangeColor(self, self)
			elif self.text() == '2':
				self.setText('')
				Example.ChangeColor(self, self)
		elif button == Qt.LeftButton:
			if self.text() != '' and int(self.text()) <= 512:
				self.setText(str(int(self.text()) * 2))
				Example.ChangeColor(self, self)
			if self.text() == '':
				self.setText('2')
				Example.ChangeColor(self, self)
		return QPushButton.mousePressEvent(self, event)

class Example(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)

		positions = [(i,j) for i in range(4) for j in range(4)]
		self.elements_all = [[0 for j in range(4)] for i in range(4)]

		for position in positions:
		    globals()['button_%d_%d' % (position[0], position[1])] = MyButton()
		    grid.addWidget(globals()['button_%d_%d' % (position[0], position[1])], *position)
		    globals()['button_%d_%d' % (position[0], position[1])].setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font: 32pt serif;}')
		    globals()['button_%d_%d' % (position[0], position[1])].setMaximumSize(100, 100)
		    globals()['button_%d_%d' % (position[0], position[1])].setEnabled(False)
		    globals()['button_%d_%d' % (position[0], position[1])].setMinimumSize(100, 100)
		    self.elements_all[position[0]][position[1]] = globals()['button_%d_%d' % (position[0], position[1])]

		self.Create()
		self.Create()

		self.mass_remove_save = []
		self.mass_remove = []
		self.enabled_push = False
		self.cheat_enabled = False

		self.move(300, 150)
		self.setMaximumSize(435, 435)
		self.setStyleSheet('QWidget{background-color: #FFF8DC;}')
		self.setMinimumSize(435, 435)
		self.setWindowTitle('2048')
		self.show()

	def remove_loading(self, mass):
		mass.clear()
		for line in self.elements_all:
			prom = []
			for col in line:
				prom.append(col.text())
			mass.append(prom)

	def remove_uploading(self, mass):
		for line in range(4):
			for col in range(4):
				self.elements_all[line][col].setText(str(mass[line][col]))
				self.ChangeColor(self.elements_all[line][col])

	def reset(self):
		for ylist in self.elements_all:
			for element in ylist:
				element.setText('')
				self.ChangeColor(element)

		self.Create()
		self.Create()

	def isblock(self):
		for ylist in self.elements_all:
			for element in ylist:
				if self.enabled_push:
					element.setEnabled(False)
				else:
					element.setEnabled(True)
		if self.enabled_push: self.enabled_push = False
		else: self.enabled_push = True

	def Moves(self, ind_start_line, shift_for_for, shift_next_line, for_one_shift, for_two_shift, for_three_shift, koef_next_line, ind_start_el_line, shift_next_el_line, koef_next_el_line, change_low_per):
		move, summ = False, False
		self.remove_loading(self.mass_remove)
		for hz in range(4):
			for i in range(1, 4):
				koor_1 = ind_start_line + (i * koef_next_line)
				koor_2 = ind_start_el_line + (i * koef_next_el_line)
				if (self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text() == '') and (self.elements_all[koor_1][koor_2].text() != ''):
					if self.elements_all[for_one_shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][for_one_shift if change_low_per=='ind_start_line' else locals()[change_low_per]].text() == '': shift = for_one_shift
					elif self.elements_all[for_two_shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][for_two_shift if change_low_per=='ind_start_line' else locals()[change_low_per]].text() == '': shift = for_two_shift
					else: shift = for_three_shift
					self.elements_all[shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][shift if change_low_per=='ind_start_line' else locals()[change_low_per]].setText(self.elements_all[ind_start_line + (i * koef_next_line)][ind_start_el_line + (i * koef_next_el_line)].text())
					self.elements_all[koor_1][koor_2].setText('')
					self.ChangeColor(self.elements_all[shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][shift if change_low_per=='ind_start_line' else locals()[change_low_per]])
					self.ChangeColor(self.elements_all[koor_1][koor_2])
					move = True
			for i in range(1, 4):
				koor_1 = ind_start_line + (i * koef_next_line)
				koor_2 = ind_start_el_line + (i * koef_next_el_line)
				if (self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text() == self.elements_all[koor_1][koor_2].text()) and (self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text() != ''):
					self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].setText(str(int(self.elements_all[koor_1][koor_2].text()) + int(self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text())))
					self.elements_all[koor_1][koor_2].setText('')
					self.ChangeColor(self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2])
					self.ChangeColor(self.elements_all[koor_1][koor_2])
					if self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text() == '2048':
						self.reset()
						return
					move, summ = True, True
			if summ:
				for i in range(1, 4):
					koor_1 = ind_start_line + (i * koef_next_line)
					koor_2 = ind_start_el_line + (i * koef_next_el_line)
					if (self.elements_all[shift_next_line + koor_1][shift_next_el_line + koor_2].text() == '') and (self.elements_all[koor_1][koor_2].text() != ''):
						if self.elements_all[for_one_shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][for_one_shift if change_low_per=='ind_start_line' else locals()[change_low_per]].text() == '': shift = for_one_shift
						elif self.elements_all[for_two_shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][for_two_shift if change_low_per=='ind_start_line' else locals()[change_low_per]].text() == '': shift = for_two_shift
						else: shift = for_three_shift
						self.elements_all[shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][shift if change_low_per=='ind_start_line' else locals()[change_low_per]].setText(self.elements_all[ind_start_line + (i * koef_next_line)][ind_start_el_line + (i * koef_next_el_line)].text())
						self.elements_all[koor_1][koor_2].setText('')
						self.ChangeColor(self.elements_all[shift if change_low_per=='ind_start_el_line' else locals()[change_low_per]][shift if change_low_per=='ind_start_line' else locals()[change_low_per]])
						self.ChangeColor(self.elements_all[koor_1][koor_2])
			if change_low_per == 'ind_start_el_line': ind_start_el_line += shift_for_for
			else: ind_start_line += shift_for_for
		if move:
			self.Create()

	def Create(self):
		elements = []
		for line in range(4):
			for col in range(4):
				if self.elements_all[line][col].text() == '':
					elements.append(str(line) + ' ' + str(col))
		chance = random.randrange(100)
		element = elements[random.randrange(len(elements))].split(' ')
		if chance < 90:
			self.elements_all[int(element[0])][int(element[1])].setText('2')
			self.ChangeColor(self.elements_all[int(element[0])][int(element[1])])
		else:
			self.elements_all[int(element[0])][int(element[1])].setText('4')
			self.ChangeColor(self.elements_all[int(element[0])][int(element[1])])

	def ChangeColor(self, object):
		if object.text() == '':
			object.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font: 32pt serif;}')
		elif object.text() == '2':
			object.setStyleSheet('QPushButton {background-color: pink; color: black; font: 32pt serif;}')
		elif object.text() == '4':
			object.setStyleSheet('QPushButton {background-color: MediumVioletRed; color: black; font: 32pt serif;}')
		elif object.text() == '8':
			object.setStyleSheet('QPushButton {background-color: red; color: black; font: 32pt serif;}')
		elif object.text() == '16':
			object.setStyleSheet('QPushButton {background-color: green; color: black; font: 32pt serif;}')
		elif object.text() == '32':
			object.setStyleSheet('QPushButton {background-color: yellow; color: black; font: 32pt serif;}')
		elif object.text() == '64':
			object.setStyleSheet('QPushButton {background-color: Aqua; color: black; font: 32pt serif;}')
		elif object.text() == '128':
			object.setStyleSheet('QPushButton {background-color: RoyalBlue; color: black; font: 32pt serif;}')
		elif object.text() == '256':
			object.setStyleSheet('QPushButton {background-color: Honeydew; color: black; font: 32pt serif;}')
		elif object.text() == '512':
			object.setStyleSheet('QPushButton {background-color: Silver; color: black; font: 32pt serif;}')
		elif object.text() == '1024':
			object.setStyleSheet('QPushButton {background-color: Goldenrod; color: black; font: 32pt serif;}')
		elif object.text() == '2048':
			object.setStyleSheet('QPushButton {background-color: black; color: white; font: 32pt serif;}')

	def keyPressEvent(self, signal):
		if signal.key() == Qt.Key_Left:
			self.Moves(0, 1, 0, 0, 1, 2, 0, 0, -1, 1, 'ind_start_line')
		elif signal.key() == Qt.Key_Up:
			self.Moves(0, 1, -1, 0, 1, 2, 1, 0, 0, 0, 'ind_start_el_line')
		elif signal.key() == Qt.Key_Down:
			self.Moves(3, -1, 1, 3, 2, 1, -1, 0, 0, 0, 'ind_start_el_line')
		elif signal.key() == Qt.Key_Right:
			self.Moves(0, -1, 0, 3, 2, 1, 0, 3, 1, -1, 'ind_start_line')
		elif signal.key() == Qt.Key_R:
			self.reset()
		elif signal.key() == Qt.Key_N:
			if self.cheat_enabled: self.cheat_enabled = False
			else: self.cheat_enabled = True
		elif (signal.key() == Qt.Key_U) and self.cheat_enabled:
			self.remove_uploading(self.mass_remove)
		elif (signal.key() == Qt.Key_S) and self.cheat_enabled:
			self.remove_loading(self.mass_remove_save)
		elif (signal.key() == Qt.Key_L) and self.cheat_enabled:
			self.remove_uploading(self.mass_remove_save)
		elif (signal.key() == Qt.Key_E) and self.cheat_enabled:
			self.isblock()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
