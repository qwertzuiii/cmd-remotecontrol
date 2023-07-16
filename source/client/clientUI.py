import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
import shutil

import pydlli

script_path = os.path.abspath(__file__)
script_folder = os.path.dirname(script_path) + "\\"

corelib = pydlli.import_dll(script_folder + "core.dll")  # Loading core.dll
shutil.rmtree("temp/")  # Removing temp directory, that was created by pydlli

data = []

class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(script_folder + "resources/client.ui", self)  # ui file load

        self.ip = None
        self.port = None

        # Set last ip + ports
        if os.path.exists(script_folder + 'last.sav'):
            with open(script_folder + 'last.sav', 'r') as sav:
                save = sav.read()
                save = save.split('^')
            self.line_ip.setText(save[0])
            self.line_port.setText(save[1])

        self.button_connect.clicked.connect(self.connect)

    def connect(self):
        # Get vars
        self.ip = self.line_ip.text()

        if self.ip == "" or self.ip == " ":
            print('No IP set')
            return

        try:
            self.port = self.line_port.text()
            if self.port == '' or self.port == ' ' or self.port == None:
                # Empty, using default port
                self.port = corelib["default_port"]
            self.port = int(self.port)
        except ValueError as e:
            print('Port is no integer:', e)
            return

        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    app.exec_()
    #print('IP:', str(appMain.ip), "PORT:", str(appMain.port))

    # Check if not exited
    if appMain.ip is None or appMain.port is None:
        print('Just exited window')
        sys.exit()

    open(script_folder + 'last.sav', 'w').write(f"{appMain.ip}^{appMain.port}")

    os.system('cls')
    corelib["init"](str(appMain.ip), int(appMain.port))
