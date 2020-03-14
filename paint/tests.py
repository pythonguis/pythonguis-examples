# import paint
from paint import Canvas
from paint import MODES
from paint import CANVAS_DIMENSIONS
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest
from PyQt5.QtCore import *

import os
import random
import types

import unittest

app = QApplication([])

GOOD_COLORS = [
	'#7f7f7f', '#333333', '#aaaaaa',
	'#010000', '#000100', '#000001',
	'#feffff', '#fffeff', '#fffffe'
]

def img_equals(img1, img2):
	if img1.width() != img2.width() or img1.height() != img2.height():
		return False
	for i in range(0, img1.width()):
		for j in range (0, img1.height()):
			pc1 = img1.pixelColor(i, j)
			pc2 = img2.pixelColor(i, j)
			# print(i,j,pc1.name(), pc2.name())
			if (pc2.name() != pc1.name() or pc2.alpha() != pc1.alpha()):
				# print(i, j, pc2.name(), pc1.name(), pc2.alpha(), pc1.alpha())
				return False
	# print('good!')
	return True

def img_not_fill(img):
	last_color = None
	for i in range(0, img.width()):
		for j in range(0,img.height()):
			pc = img.pixelColor(i, j)
			# print(i,'\t',j,'\t',pc.name())
			if last_color and last_color.name() != pc.name():
				return True
			else:
				last_color = pc
	return False

class fakeELeftClick():
	def __init__(self, x = 0, y = 0):
		self.intx = x
		self.inty = y
	def x(self):
		return self.intx
	def y(self):
		return self.inty
	def pos(self):
		p = QPoint()
		p.setX(0);
		p.setY(0);
		return p
	def button(self):
		return Qt.LeftButton

class fakeERightClick():
	def x(self):
		return 0
	def y(self):
		return 0
	def pos(self):
		p = QPoint()
		p.setX(0);
		p.setY(0);
		return p
	def button(self):
		return Qt.RightButton

class SetModeTest(unittest.TestCase):

	def setUp(self):
		self.canvas = Canvas()
		self.canvas.initialize()

	def test_switchValid(self):
		for m in MODES:
			self.canvas.reset()
			self.canvas.set_mode(m)
			self.assertEqual(self.canvas.mode, m)
			p = QPoint(1,1)
			# This test crashes the test program, as the stamp click function
			# breaks because the initial stamp is never set
			# QTest.mousePress(self.canvas, Qt.LeftButton, Qt.NoModifier, p)

	def test_switchInvalid(self):
		BAD_MODES = [
			'garbasdflkajdsf', 'FILL',
			'selectpol', 'eliipse',
			's', '', ' '
		]
		for b in BAD_MODES:
			self.canvas.set_mode(b)
			with self.assertRaises(Exception):
				p = QPoint(1,1)
				self.canvas.mousePressEvent(fakeELeftClick())
				# QTest.mousePress(self.canvas, Qt.LeftButton, Qt.NoModifier, p1)

class TestDropper(unittest.TestCase):

	def setUp(self):
		self.canvas = Canvas()
		self.canvas.initialize()

	def test_varyingColors(self):
		for c in GOOD_COLORS:
			self.canvas.initialize()
			self.canvas.pixmap().fill(QColor(c))

			self.canvas.dropper_mousePressEvent(fakeELeftClick())
			self.assertEqual(self.canvas.primary_color.name(), c)

			self.canvas.dropper_mousePressEvent(fakeERightClick())
			self.assertEqual(self.canvas.secondary_color.name(), c)

			self.canvas.initialize()

class TestFill(unittest.TestCase):

	def setUp(self):
		self.canvas = Canvas()
		self.canvas.initialize()

	def test_varyingColorsFillWhole(self):
		e = fakeELeftClick()
		
		for c in GOOD_COLORS:
			self.canvas.reset()
			self.canvas.primary_color = QColor(c)
			self.canvas.fill_mousePressEvent(fakeELeftClick())
			pix = self.canvas.pixmap().toImage().pixel(e.pos())
			self.assertEqual(QColor(pix).name(), c)

			self.canvas.reset()
			self.canvas.secondary_color = QColor(c)
			self.canvas.fill_mousePressEvent(fakeERightClick())
			pix = self.canvas.pixmap().toImage().pixel(e.pos())
			self.assertEqual(QColor(pix).name(), c)

	def test_varyingColorsFillPart(self):
		e = fakeELeftClick()
		p1 = QPoint(0,1)
		p2 = QPoint(1,1)
		p3 = QPoint(1,0)
		for c in GOOD_COLORS:
			self.canvas.initialize()

			p = QPainter(self.canvas.pixmap())
			p.setPen(QPen(QColor('#000000'), 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin))
			p.drawLine(p1, p2)
			p.drawLine(p2, p3)
			p.end()

			self.canvas.primary_color = QColor(c)
			self.canvas.fill_mousePressEvent(fakeELeftClick())

			pix = self.canvas.pixmap().toImage().pixel(e.pos())
			self.assertEqual(QColor(pix).name(), c)
			pix = self.canvas.pixmap().toImage().pixel(p1)
			self.assertEqual(QColor(pix).name(), '#000000')

	def test_varyingColorsFillMost(self):
		e = fakeELeftClick()
		p1 = QPoint(0,1)
		p2 = QPoint(1,1)
		p3 = QPoint(1,0)
		for c in GOOD_COLORS:
			self.canvas.initialize()

			p = QPainter(self.canvas.pixmap())
			p.setPen(QPen(QColor('#000000'), 1, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin))
			p.drawLine(p1, p2)
			p.drawLine(p2, p3)
			p.end()

			self.canvas.primary_color = QColor(c)
			self.canvas.fill_mousePressEvent(fakeELeftClick(90, 90))

			pix = self.canvas.pixmap().toImage().pixel(e.pos())
			self.assertNotEqual(QColor(pix).name(), c)
			pix = self.canvas.pixmap().toImage().pixel(p1)
			self.assertEqual(QColor(pix).name(), '#000000')

class TestCanvas(unittest.TestCase):

	def setUp(self):
		self.canvas = Canvas()

	def test_reset(self):
		self.canvas.background_color = QColor(Qt.white)
		self.canvas.reset()

		for x in range(0, CANVAS_DIMENSIONS[0]):
			for y in range(0, CANVAS_DIMENSIONS[1]):
				p = QPoint(x,y)
				c = self.canvas.pixmap().toImage().pixel(p)
				self.assertEqual(QColor(c).name(), QColor(Qt.white).name())

		self.canvas.background_color = QColor(Qt.black)
		self.canvas.reset()

		for x in range(0, CANVAS_DIMENSIONS[0]):
			for y in range(0, CANVAS_DIMENSIONS[1]):
				p = QPoint(x,y)
				c = self.canvas.pixmap().toImage().pixel(p)
				self.assertEqual(QColor(c).name(), QColor(Qt.black).name())


class TestRectangle(unittest.TestCase):

	def setUp(self):
		self.canvas = Canvas()
		self.canvas.initialize()
		self.canvas.setMouseTracking(True)
		# Initialize animation timer.
		# based on the paint.py code, this may be needed?
		timer = QTimer()
		timer.timeout.connect(self.canvas.on_timer)
		timer.setInterval(100)
		timer.start()

	def test_rectangle_drawing(self):
		points = [
			[1,1], [10, 10], [15, 15]
		]
		for i in points:
			for j in points:
				if (i[0] != j[0] or i[1] != j[1]):
					p1 = QPoint()
					p1.setX(i[0])
					p1.setY(i[1])
					p2 = QPoint()
					p2.setX(j[0])
					p2.setY(j[1])
					# print('point', i, j, p1.x(), p1.y(), p2.x(), p2.y())
					testCanv = Canvas()
					testCanv.initialize()
					p = QPainter(testCanv.pixmap())
					p.setPen(QPen(self.canvas.primary_color, self.canvas.config['size'], Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
					p.drawRect(QRect(p1, p2))
					p.end()
					self.canvas.reset()
					self.canvas.set_mode('rect')
					self.canvas.config['fill'] = False
					QTest.mousePress(self.canvas, Qt.LeftButton, Qt.NoModifier, p1)
					QTest.mouseMove(self.canvas, p2, 100)
					QTest.mouseRelease(self.canvas, Qt.LeftButton, Qt.NoModifier, p2, 100)
					print(img_not_fill(self.canvas.pixmap().toImage()))
					# print(img_not_fill(testCanv.pixmap().toImage()))
					self.assertEqual(True, img_equals(self.canvas.pixmap().toImage(), testCanv.pixmap().toImage()))


if __name__ == '__main__':
	unittest.main()