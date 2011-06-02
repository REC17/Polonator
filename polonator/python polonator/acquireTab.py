def establishConnections(mainWin):
    mainWin.acqDarkfieldScan.released.connect(acqDarkfieldScan)
    mainWin.acqCycleUseSnap.released.connect(acqCycleUseSnap)
    mainWin.acqCycleScan.released.connect(acqCycleScan)

def acqDarkfieldScan():
    mainWin.ButtonPermission("All", False)

    if mainWin.acqSingle.isChecked():
        cyclename = "WL1"
        flowcell = "0"

    elif mainWin.acqDual.isChecked():
        cyclename = "WL2"
        flowcell = "2"
        
    else:
        cyclename = "WL2"
        flowcell = "3"
 
    cmd = "python /home/polonator/G.007/G.007_acquisition/src/test-img.py " + cyclename + " " + flowcell 

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")    
    

def acqCycleUseSnap():
    mainWin.updateCycleScanParams()

def acqCycleScan():
    fcnum = "0";

    mainWin.ButtonPermission("All", False)    
    if not mainWin.acqFC0.isChecked():
        fcnum = "1"

    cmd = "python /home/polonator/G.007/G.007_acquisition/src/test-img.py " \
		+ str(mainWin.acqCycleName.displayText()) + " " \
		+ fcnum + " "+ str(mainWin.acqCycleIntFAM.value()) \
		+ " " + str(mainWin.acqCycleGainFAM.value()) \
		+ " " + str(mainWin.acqCycleIntCy5.value()) \
		+ " " + str(mainWin.acqCycleGainCy5.value()) \
		+ " " + str(mainWin.acqCycleIntCy3.value()) + " " \
		+ str(mainWin.acqCycleGainCy3.value()) + " " \
		+ str(mainWin.acqCycleGainTxRed.value()) \
		+ " " + str(mainWin.acqCycleIntTxR.value())

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()") 
