"""
PythonPolonatorversion5.py
Adaptation of Polonator User interface originally written in java by Greg Porreca
Created by Roger Conturie
"""

import os, sys, math, ui_polonatorV5
#import change, re and time modules imported but not used
#PyQt4 imports could probably be condensed
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtSvg import *
from PolAnimation import Wheel as wheel
from PolAnimation import Light as light
from PolAnimation import FilterCube as filterCube

import acquireTab
import acquisitionUtilitiesTab
import fluidicsUtilitiesTab
import polonatorTab
import sbsTab
import stageAlignmentTab


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

class ConfigWarning(QDialog):
	def __init__(self, parent = None):
		super(ConfigWarning, self).__init__(parent)
		message = QLabel("Filter Position Conflict")
		FixButton = QPushButton("&AutoFix")
		IgnoreButton = QPushButton("&Ignore")
		
		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(FixButton)
		buttonLayout.addWidget(IgnoreButton)
		layout = QGridLayout() 
		layout.addWidget(message, 0, 0)
		
		layout.addLayout(buttonLayout, 1,0)
		self.setLayout(layout)
				
		self.setWindowTitle("Alert!")
		self.connect(IgnoreButton, SIGNAL("clicked()"),
					 self, SLOT("reject()"))
		self.connect(FixButton, SIGNAL("clicked()"), self.autofix)
		
	def autofix(self):
		print "Fixing"
		global poloninstance
		poloninstance.filterconfig(None)
		self.close()
		
class Polonator(QMainWindow, ui_polonatorV5.Ui_MainWindow):
	"""
		This function initializes polonator class as mainwindow and as 
		parent class.
		setupUi creates and positiosn all widgets from the UI file
		List boxes are initialized to begin at their first row (row 0)
	"""        
	def __init__(self, parent=None):
		super(Polonator, self).__init__(parent)
		self.setupUi(self)
		global poloninstance
		poloninstance = self
		self.utilsLiveFilterList.setCurrentRow(0)
		self.utilsSnapFilterList.setCurrentRow(0)
		self.wheelview.setScene
		self.scene = QGraphicsScene(self)
		self.scene.setSceneRect(0, 0, 10, 10)
		self.view = self.wheelview
		self.view2 = self.svgview
		self.scene2 = QGraphicsScene(self)
		self.scene2.setSceneRect(300, 150, 100, 455)
		self.view2.setScene(self.scene2)
		self.view.setRenderHint(QPainter.Antialiasing)
		self.view.setScene(self.scene)
		self.view.setFocusPolicy(Qt.NoFocus)
		height = self.svgview.size().height()
		width = self.svgview.size().width()

		acquireTab.establishConnections(self)
		acquisitionUtilitiesTab.establishConnections(self)
		fluidicsUtilitiesTab.establishConnections(self)
		polonatorTab.establishConnections(self)
		sbsTab.establishConnections(self)
		stageAlignmentTab.establishConnections(self)
		"""
		base_dir = os.environ['POLONATOR_PATH']
		home_dir = os.environ['HOME']
		project_dir = home_dir + "/polonator/G.007/acquisition"
		acqbase_dir = base_dir + "/bin"
		fluidicsbase_dir = base_dir + "/polonator/fluidics/src"
		sequencing_home_dir = project_dir + "/sequencing_run"
		stagealign_dir = project_dir + "/stagealign"		
		"""
		filename = "polonatormaster.svg"
		file = open(filename, 'r')
		fileList = file.readlines()
		file.close()
		filename2 = "io.svg"       
		file = open(filename2, 'w')
		for i in range(len(fileList)):
			if i == 6 or i == 21 or i == 36 or i == 67:
				file.write('') 
			else:
				file.write(fileList[i])
		file.close()
		self.board = QGraphicsSvgItem("io.svg", QGraphicsPixmapItem(None, self.scene2))
		
		
		self.processlist = []
		self.timer = QTimer()
		QObject.connect(self.timer, SIGNAL("timeout()"), self.rotate)
		#global main
		mainWindow = self
		red, green, blue = 15, 5, 15
		color = QColor(red, green, blue)
		x = 100
		y = 0
		self.filterWheel = wheel(color, 1, QPointF(x1,y1))
		InstrumentLight = light(Qt.black, QPointF(-210,-22.5))
		self.scene.addItem(self.filterWheel)
		self.scene.addItem(InstrumentLight)
#COLORS
		self.color_cy5 = Qt.red
		self.color_cy3 = Qt.green
		self.color_fam = Qt.yellow
		self.color_txred = Qt.blue
		self.color_cust1 = Qt.white
		self.color_cust2 = Qt.white
		self.colorlist = [self.color_cy5, self.color_cy3, self.color_fam, self.color_txred, self.color_cust1, self.color_cust2]
		
		self.filterconfig(self.colorlist)

		




	def filterconfig(self, colorlist):
		for item in self.scene.items():
			if item.__class__.__name__ == "FilterCube":
				self.scene.removeItem(item)
		r = -math.sqrt(x1**2 + y1**2)/2
		self.filterlist = []
		colorlist = colorlist
		if colorlist == None:
			colorlist = self.colorlist
		
		for position in range(6):
			x = math.cos(position*pi/3)*r - rad/2
			y = math.sin(position*pi/3)*r - rad/2
			filter = filterCube(colorlist[position], position*pi/3, QPointF(x, y), position, colorlist, self)
			self.scene.addItem(filter)
			self.filterlist.append(filter)
		print "wheel", self.filterWheel
		self.filterWheel.update()

	def rotate(self):

		self.filterWheel.update()
		r = -math.sqrt(x1**2 + y1**2)/2
		rotateangle = pi/16

		for filter in self.filterlist:
			x = math.cos(filter.angle)*r - rad/2
			y = math.sin(filter.angle)*r - rad/2
			filter.setPos(QPointF(x, y))
			filter.angle += rotateangle
			if filter.clickedfilter != None:
				clickedfilter = filter.clickedfilter
				filterindex = clickedfilter.filter_num
		
				
		if -0.1 < math.sin(clickedfilter.angle) < 0.1 and math.cos(clickedfilter.angle) > 0:
			self.timer.stop()
			color = clickedfilter.color
			emptyposlist = []
			for position in range(len(self.filterlist)):
				self.filterlist[position].clickedfilter = None
				clickedfilter = None
				if self.filterlist[position].color == 3:
					print "NO FILTER HERE!"
					if (position - filterindex) >= 0:
						emptypos = position - filterindex
					else:
						emptypos = position + (6 - filterindex)
					emptyposlist.append(emptypos)
				x = math.cos((position-filterindex)*pi/3)*r - rad/2
				y = math.sin((position-filterindex)*pi/3)*r - rad/2
				self.filterlist[position].setPos(QPointF(x, y))
			
			print emptyposlist
			filename = "polonatormaster.svg"
			file = open(filename, 'r')
			fileList = file.readlines()
			file.close()
			filename2 = "io.svg"       
			file = open(filename2, 'w')
			for i in range(len(fileList)):
				if i == 5:
					if color == 12:
						#Yellow
						file.write('<rect x="288.739" y="515.667" fill="#F2EC63" width="9.688" height="92.529"/> \n' )
					if color == 9:
						#Blue
						file.write('<rect x="288.739" y="515.667" fill="#206AB4" width="9.688" height="92.529"/> \n' )
					if color == 7:
						#Red
						file.write('<rect x="288.739" y="515.667" fill="#9E1C20" width="9.688" height="92.529"/> \n' )
					if color == 8:
						#Green
						file.write('<rect x="288.739" y="515.667" fill="#19803F" width="9.688" height="92.529"/> \n' )
				elif i == 6 and emptyposlist.count(2) == 0:
					file.write('')
				elif i == 21 and emptyposlist.count(1) == 0:
					file.write('')
				elif i == 36 and emptyposlist.count(0) == 0:
					file.write('')
				elif i == 67 and emptyposlist.count(3) == 0:
					file.write('')
				elif i == 82 and emptyposlist.count(5) == 0:
					file.write('')
				elif i == 99 and emptyposlist.count(4) == 0:
					file.write('')
				
				else:
					file.write(fileList[i])
			file.close()
			self.scene2.removeItem(self.board)
			self.board = QGraphicsSvgItem("io.svg", QGraphicsPixmapItem(None, self.scene2))

		
	def on_SetConfigButton_released(self):
		self.comboboxlist = [self.filtcom1.currentIndex(), self.filtcom2.currentIndex(), self.filtcom3.currentIndex(), self.filtcom4.currentIndex(), self.filtcom5.currentIndex(), self.filtcom6.currentIndex()]
#ConfigWarning().show()

		colorlist = []
		for i in range(6):
			if self.comboboxlist[i] == 1:
				colorlist.append(self.color_cy5)
			if self.comboboxlist[i] == 2:
				colorlist.append(self.color_cy3)
			if self.comboboxlist[i] == 3:
				colorlist.append(self.color_fam)
			if self.comboboxlist[i] == 4:
				colorlist.append(self.color_txred)
			if self.comboboxlist[i] == 5:
				colorlist.append(self.color_cust1)
			if self.comboboxlist[i] == 6:
				colorlist.append(self.color_cust2)
			if self.comboboxlist[i] == 0:
				colorlist.append(self.color_cust2)
		
#			if self.comboboxlist.count(i + 1) > 1:		
#				form = ConfigWarning(self)
#				form.show()	
		
		self.filterconfig(colorlist)
		
		













































	def processkill(self):
	    for process in self.processlist:
			if process.pid() > 0:
			    process.kill()
	    
	    self.processlist = []

    
	def process_readyRead(self):
	    self.outWin.append(str(self.process.readLine()).strip('\n'))
	
	def process_finished(self):
	    self.outWin.append(QString(self.process.readAllStandardError()))
	    self.outWin.append("++++++++++++++++++++++++++++++++++++++")
	    self.process.close()
	    """
	If there is are additional functions to be executed after the first 
	one is finished, eval(self.nextFunc) will take care of it.
	for arg in self.args:exec(arg)
	    """
	    for arg in self.args:
	    	exec(arg)
	    #	exec arg in globals()
	    	# function unnecessary and untested
	    if self.nextFunc == "self.process_pass()":
	    	pass
	    else:
		    eval(self.nextFunc)


	
	def ButtonPermission(self, buttontype, bool):
		"""
		This function is called by many of the buttons in the GUI to disable or enable the other buttons in the GUI
		"newtablist" is used to keep track of widgets that are not push buttons, but may have push button children
		"pushbuttonlist" is a list that keeps track of all pushbuttons that are to be enabled/disabled
		
		The first if statement takes care of the condition that the buttontype argument is "All".  In this case, all
		widgets must be accounted for.  The for loop embedded in the "All" conditional statement is necessary to catch
		any pushbuttons that are immediate children of the tab widgets.
		
		Tabcount is initialized at 1 and becomes zero once the while loop has cycled through all widgets in the GUI and
		reached all of the lowest level children widgets.
		
		The final for loop will go through the eligable pushbutton list and enable or disable the buttons based on the 
		"bool" argument.  If bool is true then the buttons will be enabled, if it is false, the buttons will be disabled
		
		
		9/29/10
		ButtonPermission function has been commented out because although it disables the items specified in the original java 
		code, the suppression of these buttons makes the file difficult to test
		- Roger Conturie
		
		"""
		print "button permission function has been temporarily disabled"
		"""
		newtablist = []
		
		pushbuttonlist = []
		if buttontype == "All":
			tab = self.PolonatorTab.children() \
				+ self.AcquireTab.children() \
				+ self.FluidicsUtilitiesTab.children() \
				+ self.SBSTab.children() \
				+ self.AcquisitionUtilitiesTab.children() \
				+ self.StageAlignmentTab.children()
		else:
			tab = buttontype.children()
	            #end if

		for i in range(len(tab)):
			if str(tab[i].__class__.__name__) == "QPushButton":
				pushbuttonlist.append(tab[i])
			else:
				pass
	    # end else
		tabcount = 1
		while tabcount > 0:
			for i in range(len(tab)):
				tabwatch = tab[i].children()
				for i in range(len(tab[i].children())):
					if str(tabwatch[i].__class__.__name__) != "QPushButton":
						newtablist.append(tabwatch[i])
					else:
						pushbuttonlist.append(tabwatch[i])
# end for
	# end for
	        if newtablist == []:
	            tabcount = 0
	# end if
	        tab = newtablist
	        newtablist = []
	# end while
		for i in range(len(pushbuttonlist)):
			pushbuttonlist[i].setEnabled(bool)
	# end for
	 # end def   

	    """
	def process_start(self, cmd, args, nextFunc):
	    """
			This function begins the process of executing a command by creating
			a QProcess instance and feeding it a command line
			The input variables are cmd (the command), outWin (the specific text
			window in the GUI that the output is displayed on), args (not sure 
			what they're for), and nextFunc (the next funciton that should be
			run once the first process has completed)
	    """
	    
	    self.process = QProcess()
	    self.process.start(cmd)
	    try:
	    	processlist.append(self.process)
	    except:
	    	print "no process to add"
	    self.outWin = self.polonatorTextArea
	    self.args = args
	    self.nextFunc = nextFunc
	    """
			The first signal/slot method triggers the program to display a line 
			of text from the output into the appropriate output window.
	    
			The second signal/slot method triggers the program to terminate the
			process when the code is done executing
	    """
	    self.connect(self.process, SIGNAL("readyRead()"), self.process_readyRead)
	    self.connect(self.process, SIGNAL("finished(int)"), self.process_finished)

	"""
	########################################
	####BEGIN POLONATOR TAB FUNCTIONS ######
	########################################


	def on_stopButton_released(self):
	   
#	        For all buttons, a command is specified near the beginning of the function definition, and
#	        self.process_start is implemented to run the command.
	        

	    self.processkill()
	#     cmd = "/home/polonator/G.007/G.007_acquisition/process_kill.pl acq" 
	    
	    self.ButtonPermission(self.AcquireTab, True)
	    self.ButtonPermission(self.FluidicsUtilitiesTab, True)
	    self.ButtonPermission(self.AcquireTab, True)
	  
	    if not self.polonatorCycleEntryValidate.isEnabled():
	        for i in range(len(polonatorCycleListVector)):
	            polonatorCycleListVector.pop()
	
	    self.polonatorCycleEntry.setEnabled(True);
	    self.polonatorCycleEntryValidate.setEnabled(True);
	    self.polonatorStart.setEnabled(False);
	#     self.process_start(cmd, self.polonatorTextArea, ['pass'], "self.process_pass()")   
	    
	  
	def on_polonatorStart_released(self):
	
	    entry = str(self.polonatorCycleEntry.toPlainText()).split("\n")
	    CycleEntryRows = len(entry)
	    touchFlag = "0"
	    
	    self.polonatorStart.setEnabled(False)
	    self.polonatorCycleEntry.setEnabled(False)
	    self.polonatorCycleEntryValidate.setEnabled(False)
	# polonatorTouch.setEnabled(false);   This function cannot be used anymore because the button has been changed to a combobox
	    self.ButtonPermission("All", False)    
	    self.polonatorCycleList.clear()
	    
	    for i in range(len(entry)):
	        polonatorCycleListVector.append(entry[i])
	    
	    polonatorCycleListVector.pop()
	# print polonatorCycleListVector
	
	# polonatorCycleList.setListData(polonatorCycleListVector);
	
	#     write cycle names to cycle_list file
	    try:
	        outfile = open("/home/polonator/G.007/G.007_fluidics/src/cycle_list", "w")
	
	        for i in range(len(entry)):
	            outfile.write(str(polonatorCycleListVector[i]))
	            outfile.write('\n')
	        outfile.close()
	    except IOError: #as (errno, strerror):
	        print "Error writing to cycle_list file, I/O error" #: ({0}): {1}".format(errno, strerror)
	
	#    Version 2.6 option:
	#           try:
	#               outfile = io.BufferedWriter(io.open("/home/polonator/G.007/G.007_fluidics/src/cycle_list", "w"));
	#               for i in range(len(entry)):
	#                   outfile.write(str(polonatorCycleListVector[i]);
	#                   outfile.write('\n')
	#                   outfile.close();
	#           except IOError as (errno, strerror):
	#               print "Error writing to cycle_list file, I/O error : ({0}): {1}".format(errno, strerror)   
	#               out = io.BufferedWriter(FileWriter("/home/polonator/G.007/G.007_fluidics/src/cycle_list"));
	
	#   should we run w/ the touch sensor (forever) or w/ the GUI (just once)?
	    if self.comboBox.currentIndex() == 1:
	        touchFlag = "1"
	
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/polonator_main.py "+ touchFlag 
	    self.process_start(cmd, ['pass'], "self.process_pass()")   
	    
	
	def on_polonatorCycleEntryValidate_released(self):
	    changed = False
	# parse full document into lines
	    
	    entry = str(self.polonatorCycleEntry.toPlainText()).split("\n")
	    newEntry = len(entry)
	    L = []
	# validate each line; keep track if we need to change something
	    for i in range(newEntry):
	        if len(entry[i]) > 4:
	            entry[i] = entry[i][:4]
	            changed = True
	        if len(entry[i]) >= 3:
	            L.append(entry[i])
	        else:
	            changed = True
	    
	    self.polonatorCycleEntry.clear()
	    for i in range(len(L)):
	        self.polonatorCycleEntry.insertPlainText(str(L[i])+"\n") 
	    
	    if changed:
	        pass
	    else:
	        self.polonatorStart.setEnabled(True)
	        #polonatorCycleEntry.setBackground(Color.pink)
	# else:
	      #  polonatorCycleEntry.setBackground(Color.white)
	########################################
	####BEGIN ACQUIRE TAB FUNCTIONS ######
	########################################     
	        
	def on_acqDarkfieldScan_released(self):
	    self.ButtonPermission("All", False)
	
	    if self.acqSingle.isChecked():
	        cyclename = "WL1"
	        flowcell = "0"
	
	    elif self.acqDual.isChecked():
	        cyclename = "WL2"
	        flowcell = "2"
	        
	    else:
	        cyclename = "WL2"
	        flowcell = "3"
	 
	    cmd = "python /home/polonator/G.007/G.007_acquisition/src/test-img.py " + cyclename + " " + flowcell 
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	    
	
	def on_acqCycleUseSnap_released(self):
	    self.updateCycleScanParams()
	
	def on_acqCycleScan_released(self):
	    fcnum = "0";
	
	    self.ButtonPermission("All", False)    
	    if not self.acqFC0.isChecked():
	        fcnum = "1"
	
	    cmd = "python /home/polonator/G.007/G.007_acquisition/src/test-img.py " \
			+ str(self.acqCycleName.displayText()) + " " \
			+ fcnum + " "+ str(self.acqCycleIntFAM.value()) \
			+ " " + str(self.acqCycleGainFAM.value()) \
			+ " " + str(self.acqCycleIntCy5.value()) \
			+ " " + str(self.acqCycleGainCy5.value()) \
			+ " " + str(self.acqCycleIntCy3.value()) + " " \
			+ str(self.acqCycleGainCy3.value()) + " " \
			+ str(self.acqCycleGainTxRed.value()) \
			+ " " + str(self.acqCycleIntTxR.value())
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()") 
	    
	# ##########################################################
	#  The following functions all make use of biochem_utils.pl
	# ##########################################################
	########################################
	####BEGIN FLUID UTILS TAB FUNCTIONS ######
	########################################  
	def on_flUtilStartStrip_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
		#  cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
		cmd = fluidicsbase_dir + "/biochem_utils.pl " \
		+ str(flUtilsFCNum) \
		+ " strip_chem " \
		+ str(self.flUtilStripValve.currentText())
		self.process_start(cmd,  ['pass'], "self.process_pass()")         
	
	def on_flUtilStartHyb_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " hyb " \
	+ str(self.flUtilHybValve.currentText()) \
	+ str(self.flUtilHybPort.currentText()) 
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	
	def on_flUtilStartLig_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " lig_stepup_peg " \
	+ str(self.flUtilLigValve.currentText()) \
	+ " " + str(self.flUtilLigPort.currentText()) 
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	
	def on_flUtilStartReact_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	        
	    temp_min = 15;
	    temp_max = 70;
	    time_min = 1;
	    time_max = 240;
	
	# set flag and buffer defaults
	    bufferBefore = "0"
	    bufferAfter = "0"
	    bufferArgs = ""   
	     
	# set flags for buffer before and after reagent
	    if self.flUtilUseBufferBeforeRadioButton.isChecked():
	        bufferBefore = "1"
	
	    if self.flUtilUseBufferAfterRadioButton.isChecked():
	        bufferAfter = "1";
	    
	    if self.flUtilUseBufferBeforeRadioButton.isChecked() | self.flUtilUseBufferAfterRadioButton.isChecked():
	        flUtilUseBuffer = True
	    else:
	        flUtilUseBuffer = False
	
	#  specify buffer port/volume if we're using a buffer
	    if(flUtilUseBuffer):
	        bufferArgs = " " \
	+ str(self.flUtilReactBufferPort.currentText()) \
	+ " " \
	+ str(self.flUtilReactBufferVolume.displayText())
	
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " react " + str(self.flUtilReactValve.currentText()) \
	+ " " + str(self.flUtilReactPort.currentText()) \
	+ " " + str(self.flUtilReactTemp.displayText()) \
	+ " " + str(self.flUtilReactTime.displayText()) \
	+ " " + bufferBefore + " " + bufferAfter + bufferArgs 
	    
	    if int(str(self.flUtilReactTemp.displayText())) >= temp_min \
	and int(str(self.flUtilReactTemp.displayText())) <= temp_max \
	and int(str(self.flUtilReactTime.displayText())) >= time_min \
	and int(str(self.flUtilReactTime.displayText())) <= time_max:
	
	        self.process_start(cmd,  ['pass'], "self.process_pass()")      
	
	def on_flUtilStartCycle_released(self):                                                 
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " cycle_ligation " + str(flUtilCycleName.displayText()) 
	   
	    self.process_start(cmd,  ['pass'], "self.process_pass()")   
	
	def updateCycleScanParams(self):
	    self.acqCycleGainFAM.setProperty("value", self.acqCycleGainFAM.value())
	    self.acqCycleGainCy5.setProperty("value", self.acqCycleGainCy5.value())
	    self.acqCycleGainCy3.setProperty("value", self.acqCycleGainCy3.value())
	    self.acqCycleGainTxRed.setProperty("value", self.acqCycleGainTxRed.value())
	
	    self.acqCycleIntFAM.setProperty("value", self.utilsSnapExp.value())
	    self.acqCycleIntCy5.setProperty("value", self.utilsSnapExp.value())
	    self.acqCycleIntCy3.setProperty("value", self.utilsSnapExp.value())
	    self.acqCycleIntTxR.setProperty("value", self.utilsSnapExp.value())
	    
	def on_flUtilPrimeReagentBlock_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	    
	    if self.Includev4radioButton.ischecked():
	        primeV4 = "1"
	    else:
	        primeV4 = "0"
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(self.flUtilsFCNum.toPlainText()) + " prime_reagent_block " + primeV4
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")       
	    
	def on_flUtilPrimeFlowcell_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	        
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " flush_flowcell"
	    
	    self.process_start(cmd,  ['pass'], "self.process_pass()")   
	            
	def on_flUtilInitializeSyringe_released(self):
	    if self.flUtilFlowcell0.isChecked():
	        flUtilsFCNum = 0
	    
	    if self.flUtilFlowcell1.isChecked():
	        flUtilsFCNum = 1
	        
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(flUtilsFCNum) + " syringe_pump_init"
	    
	    self.process_start(cmd,  ['pass'], "self.process_pass()")      

	########################################
	####BEGIN SBS TAB FUNCTIONS ######
	########################################   
	def on_SBSHybRun_released(self):                                          
	    if SBSFlowcell0.isChecked():
	        SBSFCNum = 0                             
	    if SBSFlowcell1.isChecked:
	        SBSFCNum = 1
	    
	    self.ButtonPermission(self.SBSTab, False)
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(SBSFCNum) + " ilmnHyb " + str(SBSHybValve.currentText())
	    self.process_start(cmd,  ['pass'], "self.process_pass()")      
	               
	def on_SBSDeblockRun_released(self):                                              
	    if SBSFlowcell0.isChecked():
	        SBSFCNum = 0
	          
	    if SBSFlowcell1.isChecked:
	        SBSFCNum = 1
	    
	    self.ButtonPermission(self.SBSTab, False)
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(SBSFCNum) \
	+ " ilmnDeblock " \
	+ str(SBSDeblockValve.currentText())
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")          
	       
	def on_SBSIncorpRun_released(self):                                             
	    if SBSFlowcell0.isChecked():
	        SBSFCNum = 0
	                                     
	    if SBSFlowcell1.isChecked:
	        SBSFCNum = 1
	        
	    self.ButtonPermission(self.SBSTab, False)
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(SBSFCNum) + " ilmnCycle " + str(SBSIncorpValve.currentText())
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	    
	def on_SBSCycleRun_released(self):                   
	    
	    self.ButtonPermission(self.SBSTab, False)
	    
	    if SBSFlowcell0.isChecked():
	        SBSFCNum = 0
	                                     
	    if SBSFlowcell1.isChecked:
	        SBSFCNum = 1
	    
	    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	+ str(SBSFCNum) \
	+ " illumina " \
	+ str(SBSCycleDeblockValve.currentText()) \
	+ " " + str(SBSCycleIncorpValve.currentText())
	
	    self.process_start(cmd,  ['pass'], "self.process_pass()")   
	
	########################################
	####BEGIN ACQUISITION UTILS TAB FUNCTIONS ######
	########################################  
	def on_utilsHomeButton_released(self):                                                
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	
	 #   cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils reset"    
	    cmd = acqbase_dir+"/PolonatorUtils reset"   
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	
	def on_utilsStatusButton_released(self):
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils status"
	    cmd = acqbase_dir+"/PolonatorUtils status"   
	    self.process_start(cmd,  ['pass'], "self.process_pass()")       
	    
	def on_utilsUnlockButton_released(self):                                                  
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils unlock"
	    cmd = acqbase_dir + "/PolonatorUtils unlock"   
	    self.process_start(cmd,  ['pass'], "self.process_pass()")                              
	
	def on_utilsLockButton_released(self):                                                
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	 #   cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils lock"
	    cmd = acqbase_dir + "/PolonatorUtils lock"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")     
	                   
	def on_utilsThetahomeButton_released(self):                                                    
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils hometheta"
	    cmd = acqbase_dir + "/PolonatorUtils hometheta"
	    self.process_start(cmd, ['pass'], "self.process_pass()")      
	
	def on_utilsPoweronButton_released(self):
	#	cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils power-on" #, utilsTextArea, "acqUtils"
		cmd = acqbase_dir + "/PolonatorUtils power-on"
		self.process_start(cmd, ['pass'], "self.process_pass()")
		
	def on_utilsPoweroffButton_released(self):
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils power-off" #, utils, "acqUtils"
	    cmd = acqbase_dir+"/PolonatorUtils power-off"
	    self.process_start(cmd, ['pass'], "self.process_pass()")      
	
	def on_utilsDarkfieldonButton_released(self):                                                      
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils darkfield-on"
	    cmd = acqbase_dir+"/PolonatorUtils darkfield-on"
	    self.process_start(cmd, ['pass'], "self.process_pass()")         
	       
	def on_utilsDarkfieldoffButton_released(self):                                                        
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils darkfield-off"
	    cmd = acqbase_dir+"/PolonatorUtils darkfield-off"
	    self.process_start(cmd, ['pass'], "self.process_pass()")         
	
	def on_utilsCompletescanButton_released(self):                                                       
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils complete-scan"
	    cmd = acqbase_dir+"/PolonatorUtils complete-scan"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")           
	  
	def on_utilsLiveButton_released(self):                                                
	    # disableAllAcqUtilsCameraButtons();
	    commandArgs = ""+ str(float(int(self.utilsLiveExp.value())) / 1000) \
	+ " " + str(int(self.utilsLiveGain.value()))+" "+ str(self.utilsLiveFilterList.currentItem().text())
	    cmd = acqbase_dir+"/PolonatorUtils live_new " + commandArgs 
	    self.utilFocusBar.setEnabled(True);
	    self.utilSetFocus.setEnabled(True);  
	    self.process_start(cmd,  ['pass'], "self.process_pass()")          
	  
	def on_utilsViewButton_released(self):                                               
	
	    cmd = "/home/polonator/G.007/G.007_acquisition/run_load_raw.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ snap-image.raw"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")        
	 
	def on_utilsSnapButton_released(self):                                                
	    commandArgs = "" + str(self.utilsSnapFilterList.currentItem().text()) \
	+ " " + str((float(self.utilsSnapExp.value())) / 1000) + " " + str(int(self.utilsSnapGain.value()))
	    cmd = acqbase_dir + "/PolonatorUtils snap " + commandArgs 
	    self.process_start(cmd,  ['pass'], "self.process_pass()")                        
	
	def on_utilsThetaunlockButton_released(self):                                                       
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	    cmd = acqbase_dir + "/PolonatorUtils unlocktheta"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")    
	                                                                  
	def on_utilsThetahomeButton_released(self):                                                     
	    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
	    cmd = acqbase_dir + "/PolonatorUtils hometheta"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")       
	
	def on_shutLightButton_released(self):                                                
	    #TODO add your handling code here:
	    cmd = acqbase_dir + "/PolonatorUtils darkfield-off "
	
	    self.process_start(cmd, ['pass'], "self.shutLightButton2()")    
	
	
	#         cmd1 = 'python initialize_processor.py'
	#         self.process_start(cmd1, self.polonator_textarea, ['pass'], "self.shutLightButton2()")    
	
	def shutLightButton2(self):
	    cmd2 = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils shutter_close "
	    self.process_start(cmd2, ['pass'], "self.process_oa()")    
	
	def on_utilSetFocus_released(self):                                             
	    cmd = acqbase_dir + "/PolonatorUtils writefocus"
	    self.process_start(cmd,  ['pass'], "self.process_pass()")        
	            
	def on_utilFocusBar_valueChanged(self):
	    cmd = acqbase_dir + "/PolonatorUtils setfocus " + str(self.utilFocusBar.value())    
	# utilFocusLabel.setText(Integer.toString(utilFocusBar.getValue()));
	    self.process_start(cmd,  ['pass'], "self.process_pass()")              
	    
	def on_utilsColorSnapButton_released(self):                                          
	    commandArgs = "" + str(float(int(self.utilsSnapExp.value())) / 1000) \
	+ " " + str(int(self.utilsColorFAMgain.value())) \
	+ " " + str(int(self.utilsColorCy5gain.value())) \
	+ " " + str(float(int(self.utilsColorCy3gain.value()))) \
	+ " " + str(float(int(self.utilsColorTxRgain.value())))
	    cmd = acqbase_dir + "/PolonatorUtils colorsnap " + commandArgs 
	    self.process_start(cmd,  ['pass'], "self.process_pass()")               
	      
	def on_utilsColorViewButton_released(self):                                                     
	    filename1 = "none"
	    filename2 = "none"
	    filename3 = "none"
	    red = str(self.utilsColorRed.currentText())
	    green = str(self.utilsColorGreen.currentText())
	    blue = str(self.utilsColorBlue.currentText())
	    if not red == "none" or not green == "none" or not blue == "none":
	        pass
	    if not red == "none":
	        filename1 = "/home/polonator/G.007/G.007_acquisition/colorsnap-" + red + ".raw"
	    if not green == "none":
	        filename2 = "/home/polonator/G.007/G.007_acquisition/colorsnap-" + green + ".raw"
	    if not blue == "none":
	        filename3 = "/home/polonator/G.007/G.007_acquisition/colorsnap-" + blue + ".raw"
	    cmd = "/home/polonator/G.007/G.007_acquisition/run_display_color_raw.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ " \
	+ filename1 +" " + filename2 +" " + filename3 
	    self.process_start(cmd,  ['pass'], "self.process_pass()")          
	########################################
	####BEGIN STAGE ALIGNMENT TAB FUNCTIONS ######
	########################################  
	def on_stagealign_gotoposition_released(self):                                                        
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1    
	    cmd = acqbase_dir + "/PolonatorUtils gotostagealignpos " \
	+ str(stagealign_fcnum) + " " + str(int(self.stagealign_lane.value())) 
	    self.process_start(cmd, ['pass'], "self.process_pass()")                        
	    
	def on_stagealign_dostagealign_released(self):                               
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1       
	    cmd = "/home/polonator/G.007/G.007_acquisition/Polonator-stagealign " + stagealign_fcnum 
	    self.process_start(cmd, ['pass'], "self.process_pass()")      
	            
	def on_stagealign_viewlog_released(self):
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1      
	    stagealign_dir = "/home/polonator/G.007/G.007_acquisition/stagealign/"                                      
	    stagealign_textwindow.setText("");
	    try:
	        Input = open("/home/polonator/G.007/G.007_acquisition/logs/polonator-stagealign" + stagealign_fcnum + ".offsetlog" )
	        br = Input.read()
	        while Input == br.readLine():
	            stagealign_textwindow.append(input + "\n");
	        Input.close()
	    except IOError: #as (errno, strerror):
	        print "Error writing to cycle_list file, I/O error" #: ({0}): {1}".format(errno, strerror)
	
	def on_stagealign_viewbase_released(self):                                                    
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1    
	    stagealign_dir = "/home/polonator/G.007/G.007_acquisition/stagealign/"
	    cmd = "/home/polonator/G.007/G.007_acquisition/run_load_raw.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ " \
	+ str(stagealign_dir) + "ALIGN_BASE" + str(stagealign_fcnum) + "_" + str(int(self.stagealign_lane.value())) + ".raw" 
	    title = "STAGEALIGN-BASE-IMAGE-FLOWCELL-" + str(stagealign_fcnum) + "-LANE-" + str(int(self.stagealign_lane.value()))
	    cmd = cmd + " " + title
	    self.process_start(cmd,  ['pass'], "self.process_pass()")   
	                
	def on_stagealign_viewcurrent_released(self):                                                      
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1    
	    stagealign_dir = "/home/polonator/G.007/G.007_acquisition/stagealign/"
	    cmd = "/home/polonator/G.007/G.007_acquisition/run_load_raw.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ " \
	+ str(stagealign_dir) + "stagealign-image" \
	+ str(stagealign_fcnum) + "_" +str(int(self.stagealign_lane.value())) + ".raw" 
	    title = "STAGEALIGN-CURRENT-IMAGE-FLOWCELL-" \
	+ str(stagealign_fcnum) + "-LANE-" \
	+ str(int(self.stagealign_lane.value()))
	    cmd = cmd + " " + title
	    self.process_start(cmd,  ['pass'], "self.process_pass()")         
	              
	def on_stagealign_viewscore_released(self):                                                     
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1    
	    stagealign_dir = "/home/polonator/G.007/G.007_acquisition/stagealign/"
	    cmd = "/home/polonator/G.007/G.007_acquisition/run_load_stagealign_score.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ " \
	+ stagealign_dir + "stagealign-scorematrix" \
	+ str(stagealign_fcnum) + "_" \
	+ str(int(self.stagealign_lane.value())) 
	    title = "STAGEALIGN-CURRENT-SCOREMATRIX-FLOWCELL-" \
	+ str(stagealign_fcnum) + "-LANE-" \
	+ str(int(self.stagealign_lane.value()))
	    cmd = cmd + " " + title 
	    self.process_start(cmd,  ['pass'], "self.process_pass()")             
	
	def on_stagealign_dostagealign_released(self):     
	    if self.stagealign_fc0.isChecked():
	        stagealign_fcnum = 0                                 
	    if self.stagealign_fc1.isChecked():
	        stagealign_fcnum = 1                                         
	    cmd = "/home/polonator/G.007/G.007_acquisition/Polonator-stagealign " + str(stagealign_fcnum) 
	    self.process_start(cmd,  ['pass'], "self.process_pass()")         
              

	########END FUNCTIONS
	"""
if __name__ == "__main__":
    import sys

# add comments as to what this specifically does
app = QApplication(sys.argv)
form = Polonator()
form.show()
app.exec_()
