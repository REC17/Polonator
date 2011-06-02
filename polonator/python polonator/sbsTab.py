def establishConnections(mainWin):
    mainWin.SBSHybRun.released.connect(SBSHybRun)
    mainWin.SBSDeblockRun.released.connect(SBSDeblockRun)
    mainWin.SBSIncorpRun.released.connect(SBSIncorpRun)
    mainWin.SBSCycleRun.released.connect(SBSCycleRun) 

def SBSHybRun():                                          
    if SBSFlowcell0.isChecked():
        SBSFCNum = 0                             
    if SBSFlowcell1.isChecked:
        SBSFCNum = 1
    
    mainWin.ButtonPermission(mainWin.SBSTab, False)
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(SBSFCNum) + " ilmnHyb " + str(SBSHybValve.currentText())
    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")      
               
def SBSDeblockRun():                                              
    if SBSFlowcell0.isChecked():
        SBSFCNum = 0
          
    if SBSFlowcell1.isChecked:
        SBSFCNum = 1
    
    mainWin.ButtonPermission(mainWin.SBSTab, False)
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(SBSFCNum) \
+ " ilmnDeblock " \
+ str(SBSDeblockValve.currentText())

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")          
       
def SBSIncorpRun():                                             
    if SBSFlowcell0.isChecked():
        SBSFCNum = 0
                                     
    if SBSFlowcell1.isChecked:
        SBSFCNum = 1
        
    mainWin.ButtonPermission(mainWin.SBSTab, False)
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(SBSFCNum) + " ilmnCycle " + str(SBSIncorpValve.currentText())
    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")    
    
def SBSCycleRun():                   
    
    mainWin.ButtonPermission(mainWin.SBSTab, False)
    
    if SBSFlowcell0.isChecked():
        SBSFCNum = 0
                                     
    if SBSFlowcell1.isChecked:
        SBSFCNum = 1
    
    cmd = "python /home/polonator/G.007/G.007_fluidics/src/biochem_utils.py " \
+ str(SBSFCNum) \
+ " illumina " \
+ str(SBSCycleDeblockValve.currentText()) \
+ " " + str(SBSCycleIncorpValve.currentText())

    mainWin.process_start(cmd,  ['pass'], "mainWin.process_pass()")   
