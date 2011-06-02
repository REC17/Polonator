
def establishConnections(mainWin):
    mainWin.stagealign_gotoposition.released.connect(stagealign_gotoposition)
    mainWin.stagealign_dostagealign.released.connect(stagealign_dostagealign)
    mainWin.stagealign_viewlog.released.connect(stagealign_viewlog)
    mainWin.stagealign_viewbase.released.connect(stagealign_viewbase)
    mainWin.stagealign_viewcurrent.released.connect(stagealign_viewcurrent)
    mainWin.stagealign_viewscore.released.connect(stagealign_viewscore)

def stagealign_gotoposition():                                                       
    if self.stagealign_fc0.isChecked():
        stagealign_fcnum = 0                                 
    if self.stagealign_fc1.isChecked():
        stagealign_fcnum = 1    
    cmd = acqbase_dir + "/PolonatorUtils gotostagealignpos " \
+ str(stagealign_fcnum) + " " + str(int(self.stagealign_lane.value())) 
    self.process_start(cmd, ['pass'], "self.process_pass()")                        

def stagealign_dostagealign():                               
    if self.stagealign_fc0.isChecked():
        stagealign_fcnum = 0                                 
    if self.stagealign_fc1.isChecked():
        stagealign_fcnum = 1       
    cmd = "/home/polonator/G.007/G.007_acquisition/Polonator-stagealign " + stagealign_fcnum 
    self.process_start(cmd, ['pass'], "self.process_pass()")      
            
def stagealign_viewlog():
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

def stagealign_viewbase():                                                    
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
                
def stagealign_viewcurrent():                                                      
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
              
def stagealign_viewscore():                                                     
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

      
