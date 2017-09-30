#! python3

### This utility will copy a folder and its contents into a different folder
###
import Tkinter
from Tkinter import *

import ttk
from ttk import *

from tkFileDialog import askdirectory

import os
import shutil

from time import time
import subprocess as sp

class Application(Frame):

    def __init__(self, master):
        
        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables
        
        self.origin = os.getcwd()
        self.copied = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.script = ""
        self.allSet = True
        self.initialize = IntVar()
        self.build = IntVar()
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", background="white", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="40")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TCheckButton", font="Verdana 8")

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        
        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="SCRIPT DEPLOY UTILITY", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Copies python files from a source folder to a target folder. The target folder may ", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="be initialized, which is recommended. If not, all data in target folder that ", style="S.TLabel" )
        self.subLabelC = Label(self.main_container, text="exists in the source folder will be overwritten.", style="S.TLabel" )

        self.sourceTarget = LabelFrame(self.main_container, text=' Source - Target Options ', style="O.TLabelframe")
        self.selectSource = Button(self.sourceTarget, text="SOURCE FOLDER", style="B.TButton", command=self.setSource)
        self.sourceLabel = Label(self.sourceTarget, text="None", style="B.TLabel" )
        self.selectTarget = Button(self.sourceTarget, text="TARGET FOLDER", style="B.TButton", command=self.setTarget)
        self.targetLabel = Label(self.sourceTarget, text="None", style="B.TLabel" )
        self.selectScript = Button(self.sourceTarget, text="SCRIPT LOCATION", style="B.TButton", command=self.setScript)
        self.scriptLabel = Label(self.sourceTarget, text="None", style="B.TLabel" )

        self.initTarget = Checkbutton(self.sourceTarget, text="Initialize Target Folder", style="B.TCheckbutton", variable=self.initialize)
        self.createScript = Checkbutton(self.sourceTarget, text="Build Script", style="B.TCheckbutton", variable=self.build)
        self.sep_s = Separator(self.sourceTarget, orient=HORIZONTAL)
        self.sep_t = Separator(self.sourceTarget, orient=HORIZONTAL)
        
        self.statusLabel = Label(self.main_container, text="Select source and target folders", style="G.TLabel")
        self.submit = Button(self.main_container, text="START", style="B.TButton", command=self.startProcess)
        self.restart = Button(self.main_container, text="RESTART", style="B.TButton", command=self.restartProcess)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)
        
        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_a.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.selectSource.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.sourceLabel.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.sep_s.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.selectTarget.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')
        self.targetLabel.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.sep_t.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.selectScript.grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')
        self.scriptLabel.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.initTarget.grid(row=5, column=0, padx=5, pady=5, sticky='W')
        self.createScript.grid(row=5, column=2, padx=5, pady=5, sticky='W')
        self.sourceTarget.grid(row=5, column=0, columnspan=3, rowspan=6, padx=5, pady=0, sticky='NSEW')
        
        self.sep_b.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.submit.grid(row=12, column=0, columnspan=1, padx=5, pady=0, sticky='NSEW')
        self.restart.grid(row=12, column=1, padx=5, pady=0, sticky='NSEW')
        self.exit.grid(row=12, column=2, padx=5, pady=0, sticky='NSEW')
        self.sep_d.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.statusLabel.grid(row=14, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.sep_e.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.progress_bar.grid(row=16, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.initialize.set(0)
        self.build.set(0)

    def setSource(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.sourceLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.source = pathname

            
    def setTarget(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.targetLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.target = pathname


    def setScript(self):
        
        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.scriptLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.script = pathname


    def startProcess(self):

        if self.submit["text"] == "START":
            self.checkFolders()
            
            if self.allSet:
                self.submit["text"] = "PROCESS"
                self.restart["state"] = "DISABLED"
                self.statusLabel["text"] = "Click PROCESS to start or RESTART to change settings"

        else:
            self.checkFolders()
            
            if self.allSet:
                self.processRequest()


    def checkFolders(self):

        self.allSet = True
        
        if self.source == "":
            self.showMessage("Source folder not yet selected.")
            self.allSet = False
            return

        if self.target == "":
            self.showMessage("Target folder not yet selected.")
            self.allSet = False
            return

        if len(os.listdir(self.source)) == 0:
            self.showMessage("Source folder is empty.")
            self.allSet = False
            return

        if self.initialize.get() == 1 and self.submit["text"] == "START":
            self.showMessage("You have chosen to initialize target folder.")
            

    def showMessage(self, message):

        self.popConfirm = Toplevel(self.main_container)
        self.popConfirm.title("MESSAGE")
        self.popConfirm.maxsize(300, 80)
        self.popConfirm.minsize(300, 80)

        self.messageText = Label(self.popConfirm, text=message, style="MS.TLabel" )
        self.close = Button(self.popConfirm, text="CLOSE", style="B.TButton", command=self.popConfirm.destroy)
        self.messageSep = Separator(self.popConfirm, orient=HORIZONTAL)

        self.messageText.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.messageSep.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.close.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')


    def processRequest(self):

        import threading

        t = threading.Thread(None, self.copyFiles, ())
        t.start()


    def copyFiles(self):

        self.progress_bar.start()
        self.copying = 0

        # get start time

        t0 = time()
        
        # disable all buttons

        self.selectSource["state"] = DISABLED
        self.selectTarget["state"] = DISABLED
        self.initTarget["state"] = DISABLED
        self.restart["state"] = DISABLED
        self.submit["state"] = DISABLED
        self.exit["state"] = DISABLED

        self.statusLabel["text"] = "Processing..."
        
        if self.initialize.get() == 1:

            # Target folder will be initialized to ensure that it has same structure as source
            for folderName, subFolders, fileNames in os.walk(self.target):

                # Delete all files first
                for file in fileNames:
                    os.remove(os.path.join(folderName, file))

            for folderName, subFolders, fileNames in os.walk(self.target, topdown=False):

                # Delete all folders in target folder next
                for folder in subFolders:
                    os.rmdir(os.path.join(folderName, folder))
                    

        if self.build.get() == 1:

            self.buildScript()


        # Walk thru the source folder, creating subfolders and copying files into the target folder
        
        for folderName, subFolders, fileNames in os.walk(self.source):

            for files in fileNames:

                if files[-3:] == '.py':

                    sub = os.path.relpath(folderName, self.source)
                
                    # Check if the subfolder already exists in the target folder and create it if it is not
                
                    if sub != ".":
                        if os.path.exists(os.path.join(self.target, sub)):
                            pass
                        else:
                            os.chdir(self.target)
                            os.makedirs(sub)

                    shutil.copy(os.path.join(folderName, files), os.path.join(self.target, sub))
                    self.copying += 1

        self.selectSource["state"] = NORMAL
        self.selectTarget["state"] = NORMAL
        self.initTarget["state"] = NORMAL
        self.restart["state"] = NORMAL
        self.submit["state"] = NORMAL
        self.exit["state"] = NORMAL

        self.progress_bar.stop()            
        self.statusLabel["text"] = str(self.copying) + " file(s) copied successfully in %0.1fs." % (time() - t0)
        

    def buildScript(self):

        scriptFile = open("script.bat", "w")

        script_line = 'Attention! Delete this line and others that are not needed for the script to run'
        scriptFile.write(script_line)
        scriptFile.write("\n")
        
        for folderName, subFolders, fileNames in os.walk(self.source):

            for files in fileNames:

                if files[-3:] == '.py':

                    script_line = '@pyw ' + self.target.lower() + '/' + files + ' %*'
                    scriptFile.write(script_line)
                    scriptFile.write("\n")

        scriptFile.close()

        sp.Popen(["notepad.exe", "script.bat"])


    def restartProcess(self):
        # Launch notepad to show status of last copy request

        os.chdir(self.origin)
        self.statusLabel["text"] = "Select source and target folders"
        self.sourceLabel["text"] = "None"
        self.targetLabel["text"] = "None"
        self.submit["text"] = "START"
        self.initialize.set(0)
        self.source = ""
        self.target = ""
        self.copying = 0

root = Tk()
root.title("FOLDER COPY UTILITY")
#root.minsize(480, 380)
#root.maxsize(480, 380)

# Set size

wh = 380
ww = 480

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
