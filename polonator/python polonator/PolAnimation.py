import os, sys, math, ui_polonatorV5
#import change, re and time modules imported but not used
#PyQt4 imports could probably be condensed
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyQt4 import QtCore, QtGui
MAC = "qt_mac_set_native_menubar" in dir()

#cir is the radius of the filterwheel
global cir
cir = 200
# rad is the radius of each circle
global rad
rad = 40
#x1 and y1 are the coordinates of the filter wheel
global x1
x1 = -100
global y1
y1 = -100
global pi
pi = 3.14159265358979
global filter
filter = 0
global polonatorCycleListVector
polonatorCycleListVector = []

"""
	Note: Version 4 is compatible with original UI.  Version 5 is designed for use with updated UI
	TODO: 
	convert the following Perl files to python modules
	Also adapt the following binaries (Work has been done on this already), to python modules
	as written by Nick Conway:  
		PolonatorUtils
		Polonator-stagealign
"""
class Light(QGraphicsItem):
	Rect = QRectF(0, 0, 400, 50)
	def __init__(self, color, position):
		super(Light, self).__init__()
		self.color = color
		self.setPos(position)
	
	def boundingRect(self):
		return Light.Rect
	
	def paint(self, painter, option, widget=None):
		painter.setBrush(QBrush(self.color))
		painter.drawRect(0,0,100,45)
		
class Wheel(QGraphicsItem):
    Rect = QRectF(0, 0, rad, rad)
    def __init__(self, color, angle, position):
        super(Wheel, self).__init__()
        self.color = color
        self.angle = angle
        self.setPos(position)
        self.angle = 0

    def mousePressEvent(self, event):
        factor = 10
        whee.color.setBlue(factor)
        whee.setPos(QPointF(100, 0))

    def boundingRect(self):
        return Wheel.Rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(0, 0, cir, cir)

class FilterCube(QGraphicsItem):

    Rect = QRectF(x1+(3*cir/4)-rad/2,y1+(3*cir/4)-rad/2, rad, rad)
    def __init__(self, color, angle, position, filtnum, colorlist, mainWindowInstance):
        super(FilterCube, self).__init__()
	self.mWI = mainWindowInstance
        self.color = color
        self.angle = angle
        self.setPos(position)
        self.clickedfilter = None
        self.filter_num = filtnum
        self.colorlist = colorlist
    
    def mousePressEvent(self, event):

		self.mWI.timer.start(50)
		speed = 0.5
		print self.colorlist
		self.clickedfilter = self
		filename = "polonatormaster.svg"
		file = open(filename, 'r')
		fileList = file.readlines()
		file.close()
		filename2 = "io.svg"       
		file = open(filename2, 'w')
		for i in range(len(fileList)):
			if (i == 6 and self.colorlist[0]!=3)\
				or (i == 21 and self.colorlist[1]!=3) \
				or (i == 36 and self.colorlist[2]!=3) \
				or (i == 67 and self.colorlist[3]!=3) \
				or (i == 82 and self.colorlist[4]!=3) \
				or (i == 99 and self.colorlist[5]!=3):
				
				file.write('<!--Erase!-->') 
			elif i == 18 or i == 33 or i == 48 or i == 79 or i == 94 or i == 111:
				if i == 18:
					file.write('<rect x="379.303" y="281.725" fill="url(#SVGID_1_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate" values="0,0; 56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     
				if i == 33:
					file.write('<rect x="322.859" y="281.725" fill="url(#SVGID_2_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate" values="0,0; 56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     
				if i == 48:
					file.write('<rect x="266.832" y="281.725" fill="url(#SVGID_3_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate" values="0,0; 56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     
				if i == 79:
					file.write('<rect x="435.748" y="281.725" fill="url(#SVGID_5_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate"\n values="0,0; -56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     
				if i == 94:
					file.write('<rect x="322.859" y="281.725" fill="url(#SVGID_6A_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate"\n values="0,0; -56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     
				if i == 111:
					file.write('<rect x="379.303" y="281.725" fill="url(#SVGID_7A_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate" values="0,0; -56.4443, 0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)     

	
					
			#	if i == 43:
		#			file.write('<rect x="435.748" y="281.725" fill="url(#SVGID_3_)" width="55.836" height="52.775">\n  <animateTransform attributeName="transform" type="translate"\n values="0,0; -169.333,0" begin="0s" dur="%ss" fill="freeze" /> \n /> \n</rect>' %speed)
	#		<rect x="438.488" y="281.725" fill="url(#SVGID_3_)" width="55.836" height="52.775"/>

			else:
				file.write(fileList[i])
		file.close()
		self.mWI.scene2.removeItem(self.mWI.board)
		self.mWI.board = QGraphicsSvgItem("io.svg", QGraphicsPixmapItem(None, self.mWI.scene2))

	
    def boundingRect(self):
        return Wheel.Rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(0, 0, rad, rad)
            
