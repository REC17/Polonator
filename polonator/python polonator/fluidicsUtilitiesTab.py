def establishConnections(mainWin):
    mainWin.flUtilStartStrip.released.connect(flUtilStartStrip)
    mainWin.flUtilStartHyb.released.connect(flUtilStartHyb)
    mainWin.flUtilStartLig.released.connect(flUtilStartLig)
    mainWin.flUtilStartReact.released.connect(flUtilStartReact)
    mainWin.flUtilStartCycle.released.connect(flUtilStartCycle)
    mainWin.flUtilPrimeFlowcell.released.connect(flUtilPrimeFlowcell)
    mainWin.flUtilInitializeSyringe.released.connect(flUtilInitializeSyringe)

def flUtilStartStrip():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
	#  cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
	cmd = fluidicsbase_dir + "/biochem_utils.pl " \
	+ str(flUtilsFCNum) \
	+ " strip_chem " \
	+ str(mainWin.flUtilStripValve.currentText())
	mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")         

def flUtilStartHyb():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " hyb " \
+ str(mainWin.flUtilHybValve.currentText()) \
+ str(mainWin.flUtilHybPort.currentText()) 

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")    

def flUtilStartLig():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " lig_stepup_peg " \
+ str(mainWin.flUtilLigValve.currentText()) \
+ " " + str(mainWin.flUtilLigPort.currentText()) 

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")    

def flUtilStartReact():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
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
    if mainWin.flUtilUseBufferBeforeRadioButton.isChecked():
        bufferBefore = "1"

    if mainWin.flUtilUseBufferAfterRadioButton.isChecked():
        bufferAfter = "1";
    
    if mainWin.flUtilUseBufferBeforeRadioButton.isChecked() | mainWin.flUtilUseBufferAfterRadioButton.isChecked():
        flUtilUseBuffer = True
    else:
        flUtilUseBuffer = False

#  specify buffer port/volume if we're using a buffer
    if(flUtilUseBuffer):
        bufferArgs = " " \
+ str(mainWin.flUtilReactBufferPort.currentText()) \
+ " " \
+ str(mainWin.flUtilReactBufferVolume.displayText())

    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " react " + str(mainWin.flUtilReactValve.currentText()) \
+ " " + str(mainWin.flUtilReactPort.currentText()) \
+ " " + str(mainWin.flUtilReactTemp.displayText()) \
+ " " + str(mainWin.flUtilReactTime.displayText()) \
+ " " + bufferBefore + " " + bufferAfter + bufferArgs 
    
    if int(str(mainWin.flUtilReactTemp.displayText())) >= temp_min \
and int(str(mainWin.flUtilReactTemp.displayText())) <= temp_max \
and int(str(mainWin.flUtilReactTime.displayText())) >= time_min \
and int(str(mainWin.flUtilReactTime.displayText())) <= time_max:

        mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")      

def flUtilStartCycle():                                                 
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " cycle_ligation " + str(flUtilCycleName.displayText()) 
   
    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")   

def updateCycleScanParams(mainWin):
    mainWin.acqCycleGainFAM.setProperty("value", mainWin.acqCycleGainFAM.value())
    mainWin.acqCycleGainCy5.setProperty("value", mainWin.acqCycleGainCy5.value())
    mainWin.acqCycleGainCy3.setProperty("value", mainWin.acqCycleGainCy3.value())
    mainWin.acqCycleGainTxRed.setProperty("value", mainWin.acqCycleGainTxRed.value())

    mainWin.acqCycleIntFAM.setProperty("value", mainWin.utilsSnapExp.value())
    mainWin.acqCycleIntCy5.setProperty("value", mainWin.utilsSnapExp.value())
    mainWin.acqCycleIntCy3.setProperty("value", mainWin.utilsSnapExp.value())
    mainWin.acqCycleIntTxR.setProperty("value", mainWin.utilsSnapExp.value())
    
def flUtilPrimeReagentBlock():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
    
    if mainWin.Includev4radioButton.ischecked():
        primeV4 = "1"
    else:
        primeV4 = "0"
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(mainWin.flUtilsFCNum.toPlainText()) + " prime_reagent_block " + primeV4

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")       
    
def flUtilPrimeFlowcell():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
        
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " flush_flowcell"
    
    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")   

def flUtilInitializeSyringe():
    if mainWin.flUtilFlowcell0.isChecked():
        flUtilsFCNum = 0
    
    if mainWin.flUtilFlowcell1.isChecked():
        flUtilsFCNum = 1
        
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(flUtilsFCNum) + " syringe_pump_init"
    
    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")      
