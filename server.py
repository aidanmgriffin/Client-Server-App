import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog
import socket
import serverApp
import threading

# Dynamically get IP address rather than manually inputting one.
IP = socket.gethostbyname(socket.gethostname())

PORT = 5000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

print("Starting server... \n")
#AF_INET is the address domain in the socket. SOCK_STREAM is the type of socket. We chose this because the data is read in a continous flow.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Make port reusable 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Bind the socket to the specified address  
server.bind(ADDR)

#Keep track of the connected threads in order to display to all of them.
clients = []

def main():

    #Wait for client to connect. Maximum number of connections is 5
    server.listen()

    athread = threading.Thread(target = accept)
    athread.start()
    athread.join()
    server.close()

    print("Server is listening...\n")

# Wait for new connections from clients.
def accept():

    while True:
        #Accept connection from client. Conn - the connection socket. Addr - the IP address of sender.
        try:
            connection, addr = server.accept()
            connection.send(bytes("Name: ", FORMAT))
            print(f"{addr} Connected. \n")
            thread = threading.Thread(target=newThread, args = (connection, addr))
            thread.start()
        except:
            break


#Concurrently listens for new messages from clients.
def newThread(connection, addr):

    broadcast(f"New connection {addr}")

    name = connection.recv(SIZE).decode(FORMAT)
    connection.send(bytes(f'Welcome {name}', FORMAT))
    clients.append(connection)

    while True:
        message = connection.recv(SIZE).decode(FORMAT)

        print(ADDR[0] + ": " + message)

        broadcast(message)

        if message == 'bye':
            connection.close()
            break

        if '[FILE]' in message:
            file = open("output.txt", 'w')
            file.write(message)
            print("File written")

#Send message to all connecte threads.
def broadcast(message):
    for client in clients:
        client.send(bytes(message, FORMAT))

# Open file selection dialog and get path of selected file.
def browseFiles():
    global FILENAME
    fileName = QFileDialog.getOpenFileName()
    FILENAME = fileName[0]    
    return FILENAME

def SetMessageText(ui, message):
    global MESSAGETEXT
    MESSAGETEXT = message
    print(f"Message text set to {MESSAGETEXT}")

##The following code is all deprecated, as it was used to provide server-side GUI support, which doesn't work.
# def OnStartClick():
#     main()
#     # pass

# def OnEndClick(file, connection, addr):
#     file.close()
#     connection.close()
#     print(f"{addr} disconnected. ")

# def OnSendClick(self):
#         SetMessageText(ui.messageBox.toPlainText())

#         #Initiate start of server to send messages/files to client.
    
# def onBrowseClick(self):
#     fileName = browseFiles()
#     ui.openFileLabel.setText(fileName)
#     print("File Uploaded: " + fileName + "\n")
    

# def printToBrowser(textmessage):
#     try:
#         ui.incomingText.setText(ui.incomingText.toPlainText() + textmessage)
#     except:
#         print("Couldn't print to browser")
#         pass

#run client server application
if __name__ == '__main__':

    main()

    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # global ui
    # ui = serverApp.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # ui.serverButton.clicked.connect(OnSendClick)
    # ui.openFileButton.clicked.connect(onBrowseClick)
    # ui.endButton_2.clicked.connect(OnStartClick)

    # MainWindow.show()
    # sys.exit(app.exec_())

