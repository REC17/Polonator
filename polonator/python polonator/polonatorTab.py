
def establishConnections(mainWin):
    mainWin.stopButton.released.connect(polonatorStop)
    mainWin.polonatorStart.released.connect(polonatorStart)
    mainWin.polonatorCycleEntryValidate.released.connect(polonatorCycleEntryValidate)
    mainWin.acqDarkfieldScan.released.connect(acqDarkfieldScan)
    
def polonatorStop():
    print "Stop"

def polonatorStart():

    entry = str(mainWin.polonatorCycleEntry.toPlainText()).split("\n")
    CycleEntryRows = len(entry)
    touchFlag = "0"
    
    mainWin.polonatorStart.setEnabled(False)
    mainWin.polonatorCycleEntry.setEnabled(False)
    mainWin.polonatorCycleEntryValidate.setEnabled(False)
# polonatorTouch.setEnabled(false);   This function cannot be used anymore because the button has been changed to a combobox
    mainWin.ButtonPermission("All", False)    
    mainWin.polonatorCycleList.clear()
    
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
    if mainWin.comboBox.currentIndex() == 1:
        touchFlag = "1"

    cmd = "python /home/polonator/G.007/G.007_fluidics/src/polonator_main.py "+ touchFlag 
    mainWin.process_start(cmd, ['pass'], "mainWin.process_pass()")   
    

def polonatorCycleEntryValidate():
    changed = False
# parse full document into lines
    
    entry = str(mainWin.polonatorCycleEntry.toPlainText()).split("\n")
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
    
    mainWin.polonatorCycleEntry.clear()
    for i in range(len(L)):
        mainWin.polonatorCycleEntry.insertPlainText(str(L[i])+"\n") 
    
    if changed:
        pass
    else:
        mainWin.polonatorStart.setEnabled(True)
        #polonatorCycleEntry.setBackground(Color.pink)
# else:
      #  polonatorCycleEntry.setBackground(Color.white)
#           
        
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


