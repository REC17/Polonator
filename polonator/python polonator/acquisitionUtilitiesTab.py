def establishConnections(mainWin):
    mainWin.utilsHomeButton.released.connect(utilsHome)
    mainWin.utilsStatusButton.released.connect(utilsStatus)
    mainWin.utilsUnlockButton.released.connect(utilsUnlock)
    mainWin.utilsLockButton.released.connect(utilsLock)
    mainWin.utilsThetahomeButton.released.connect(utilsThetahome)
    mainWin.utilsPoweronButton.released.connect(utilsPoweron)
    mainWin.utilsPoweroffButton.released.connect(utilsPoweroff)
    mainWin.utilsDarkfieldonButton.released.connect(utilsDarkfieldon)
    mainWin.utilsDarkfieldoffButton.released.connect(utilsDarkfieldoff)
    mainWin.utilsCompletescanButton_2.released.connect(utilsCompletescan)
    mainWin.utilsViewButton.released.connect(utilsView)
    mainWin.utilsLiveButton.released.connect(utilsLive)
    mainWin.utilsThetaunlockButton.released.connect(utilsThetaunlock)
    mainWin.utilsThetahomeButton.released.connect(utilsThetahome)
    mainWin.shutLightButton.released.connect(shutLight)
    mainWin.utilSetFocus.released.connect(utilSetFocus)
    mainWin.utilFocusBar.valueChanged.connect(utilsFocusBar)
    mainWin.utilsColorSnapButton.released.connect(utilsColorSnap)
    mainWin.utilsColorViewButton.released.connect(utilsColorView)

def utilsHome():                                                
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)

 #   cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils reset"    
    cmd = acqbase_dir+"/PolonatorUtils reset"   
    self.process_start(cmd,  ['pass'], "self.process_pass()")    

def utilsStatus():
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils status"
    cmd = acqbase_dir+"/PolonatorUtils status"   
    self.process_start(cmd,  ['pass'], "self.process_pass()")       
    
def utilsUnlock():                                                  
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils unlock"
    cmd = acqbase_dir + "/PolonatorUtils unlock"   
    self.process_start(cmd,  ['pass'], "self.process_pass()")                              

def utilsLock():                                                
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
 #   cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils lock"
    cmd = acqbase_dir + "/PolonatorUtils lock"
    self.process_start(cmd,  ['pass'], "self.process_pass()")     
                   
def utilsThetahome():                                                    
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils hometheta"
    cmd = acqbase_dir + "/PolonatorUtils hometheta"
    self.process_start(cmd, ['pass'], "self.process_pass()")      

def utilsPoweron():
#	cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils power-on" #, utilsTextArea, "acqUtils"
	cmd = acqbase_dir + "/PolonatorUtils power-on"
	self.process_start(cmd, ['pass'], "self.process_pass()")
	
def utilsPoweroff():
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils power-off" #, utils, "acqUtils"
    cmd = acqbase_dir+"/PolonatorUtils power-off"
    self.process_start(cmd, ['pass'], "self.process_pass()")      

def utilsDarkfieldon():                                                      
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils darkfield-on"
    cmd = acqbase_dir+"/PolonatorUtils darkfield-on"
    self.process_start(cmd, ['pass'], "self.process_pass()")         
       
def utilsDarkfieldoff():                                                        
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils darkfield-off"
    cmd = acqbase_dir+"/PolonatorUtils darkfield-off"
    self.process_start(cmd, ['pass'], "self.process_pass()")         

def utilsCompletescan():                                                       
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
#	    cmd = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils complete-scan"
    cmd = acqbase_dir+"/PolonatorUtils complete-scan"
    self.process_start(cmd,  ['pass'], "self.process_pass()")           
  
def utilsLive():                                                
    # disableAllAcqUtilsCameraButtons();
    commandArgs = ""+ str(float(int(self.utilsLiveExp.value())) / 1000) \
+ " " + str(int(self.utilsLiveGain.value()))+" "+ str(self.utilsLiveFilterList.currentItem().text())
    cmd = acqbase_dir+"/PolonatorUtils live_new " + commandArgs 
    self.utilFocusBar.setEnabled(True);
    self.utilSetFocus.setEnabled(True);  
    self.process_start(cmd,  ['pass'], "self.process_pass()")          
  
def utilsView():                                               

    cmd = "/home/polonator/G.007/G.007_acquisition/run_load_raw.sh /opt/MATLAB/MATLAB_Component_Runtime/v77/ snap-image.raw"
    self.process_start(cmd,  ['pass'], "self.process_pass()")        
 
def utilsSnap():                                                
    commandArgs = "" + str(self.utilsSnapFilterList.currentItem().text()) \
+ " " + str((float(self.utilsSnapExp.value())) / 1000) + " " + str(int(self.utilsSnapGain.value()))
    cmd = acqbase_dir + "/PolonatorUtils snap " + commandArgs 
    self.process_start(cmd,  ['pass'], "self.process_pass()")                        

def utilsThetaunlock():                                                       
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
    cmd = acqbase_dir + "/PolonatorUtils unlocktheta"
    self.process_start(cmd,  ['pass'], "self.process_pass()")    
                                                                  
def utilsThetahome():                                                     
    self.ButtonPermission(self.AcquisitionUtilitiesTab, False)
    cmd = acqbase_dir + "/PolonatorUtils hometheta"
    self.process_start(cmd,  ['pass'], "self.process_pass()")       

def shutLight():                                                
    #TODO add your handling code here:
    cmd = acqbase_dir + "/PolonatorUtils darkfield-off "

    self.process_start(cmd, ['pass'], "self.shutLightButton2()")    


#         cmd1 = 'python initialize_processor.py'
#         self.process_start(cmd1, self.polonator_textarea, ['pass'], "self.shutLightButton2()")    

def shutLightButton2(self):
    cmd2 = "/home/polonator/G.007/G.007_acquisition/PolonatorUtils shutter_close "
    self.process_start(cmd2, ['pass'], "self.process_oa()")    

def utilSetFocus(self):                                             
    cmd = acqbase_dir + "/PolonatorUtils writefocus"
    self.process_start(cmd,  ['pass'], "self.process_pass()")        
            
def utilsFocusBar(self):
    cmd = acqbase_dir + "/PolonatorUtils setfocus " + str(self.utilFocusBar.value())    
# utilFocusLabel.setText(Integer.toString(utilFocusBar.getValue()));
    self.process_start(cmd,  ['pass'], "self.process_pass()")              
    
def utilsColorSnap():                                          
    commandArgs = "" + str(float(int(self.utilsSnapExp.value())) / 1000) \
+ " " + str(int(self.utilsColorFAMgain.value())) \
+ " " + str(int(self.utilsColorCy5gain.value())) \
+ " " + str(float(int(self.utilsColorCy3gain.value()))) \
+ " " + str(float(int(self.utilsColorTxRgain.value())))
    cmd = acqbase_dir + "/PolonatorUtils colorsnap " + commandArgs 
    self.process_start(cmd,  ['pass'], "self.process_pass()")               
      
def utilsColorView():                                                     
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
