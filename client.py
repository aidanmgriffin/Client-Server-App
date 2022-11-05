import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog
import clientApp
import threading

# Dynamically get IP address rather than manually inputting one.
IP = socket.gethostbyname(socket.gethostname())


PORT = 5000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
FILENAME = "info/helloworld.txt"
# MESSAGETEXT = "Hello, world!"
ISFILE = False

messages = []

# print("Message text: ", MESSAGETEXT)
print("Starting server... ")
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def SetMessageText(message):
    global MESSAGETEXT
    MESSAGETEXT = message
    print(f"Set message text to {MESSAGETEXT}!")

def receive():
    while True:
        try:
            newmessage = client.recv(SIZE).decode(FORMAT)
            printToBrowser(newmessage)         
            # print(newmessage)        
        except OSError:
            print("forcibly close 1")
            client.close()
            break


    # print("Message text: ", MESSAGETEXT)
    # print("Starting server... ")
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(ADDR)


newthread = threading.Thread(target=receive)
    #thread ends whenever main thread ends.
newthread.daemon = True
newthread.start()
    # while True:

def sendMessage():
   

    # file = open(FILENAME, 'r')
    # data = file.read()

    # #send name of file to server
    global ISFILE
    if(ISFILE):

        filename = open(FILENAME, 'r')
        filedata = filename.read()

        client.send(bytes(filedata, FORMAT))

        ISFILE = False
        filename.close()

    else:

        outmessage = ui.messageBox.toPlainText()
        print("Message Text = " + outmessage)
                    
        client.send(bytes(outmessage, FORMAT))

        if outmessage == 'bye':
            client.close()

    # client.send(MESSAGETEXT.encode(FORMAT))
    # client.send(data.encode(FORMAT))

    # file.close()
    # client.close()

# client.close()

def browseFiles():

    global FILENAME

    # Open file selection dialog and get path of selected file.
    fileName = QFileDialog.getOpenFileName()
    FILENAME = fileName[0]
    # clientApp.fileNameLabel.setText(FILENAME)
    global ISFILE
    ISFILE = True
    
    return FILENAME

def onBrowseClick():
    fileName = browseFiles()
    ui.fileNameLabel.setText(fileName)
    print("File Name: ", fileName)

def onSendClick():
    sendMessage()
    # __init__()
    # SetMessageText(ui.messageBox.toPlainText())
    # snd = threading.Thread(target=)
    # snd.start()

def printToBrowser(textmessage):
    # print("tm: ", textmessage)
    try:
        ui.textBrowser.append(ADDR[0] + ": " +textmessage)
        # ui.textBrowser.setText(ui.textBrower.toPlainText() + textmessage)
    except:
        print("Couldn't print to browser... ")
        pass

#run client server application
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    global ui
    ui = clientApp.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    ui.browseButton.clicked.connect(onBrowseClick)
    ui.sendButton.clicked.connect(onSendClick)

    sys.exit(app.exec_())

