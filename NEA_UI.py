import typing
from PyQt5 import QtCore
import PyQt5.QtWidgets as qtw
import sqlite3

from PyQt5.QtWidgets import QWidget

users_db = "users.db"
userdb_connect = sqlite3.connect(users_db)
userdb_connect.execute("PRAGMA foreign_keys = 1")

def getNextUID():
    sql = """ SELECT * FROM users"""
    c = userdb_connect.execute(sql)
    l = [x[0] for x in c]
    if l:
        latest = l[-1]
        latest  = str(int(latest.lstrip("0")) +1)
        while len(latest) < 4:
            latest = "0" + latest
        return(latest)
    else:
        return "0001"

class mainMenu(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.userID = None
        self.menuGrid = qtw.QGridLayout()

        self.user_list  = qtw.QComboBox()
        sql = """ SELECT * FROM users"""
        c = userdb_connect.execute(sql)
        for i in c:
            self.user_list.addItem(f"{i[1]} [{i[0]}]")

        self.add_user   = qtw.QLineEdit()
        self.add_user.setPlaceholderText("Enter New User Name Here:")

        self.new_user_button = qtw.QPushButton("Add new User")
        self.new_user_button.clicked.connect(self.addUser)

        self.removeUser = qtw.QPushButton("Remove Selected User")
        self.removeUser.clicked.connect(self.remove)

        self.startB = qtw.QPushButton("Start")
        self.startB.clicked.connect(self.parent)

        self.menuGrid.addWidget(self.user_list,0,0,1,3)
        self.menuGrid.addWidget(self.add_user,1,0,1,1)
        self.menuGrid.addWidget(self.new_user_button,1,1,1,1)
        self.menuGrid.addWidget(self.removeUser,1,2,1,1)
        self.menuGrid.addWidget(self.startB,2,0,1,3)

        self.setLayout(self.menuGrid)

    def parent(self):
        self.parentWidget().ID = self.user_list.currentText()[-5:-1]
        self.parentWidget().deckSel()

    def getUserDecks(self):
        getdecks = f''' SELECT * FROM decks WHERE UID ="{self.userID}" '''
        c =  userdb_connect.execute(getdecks)
        l = [x for x in c]
        print(l)
        return l
    
    def addUser(self):
        nextID = getNextUID()
        username =  self.add_user.text()
        if username:
            self.user_list.addItem(f"{username} [{nextID}]")
            f = [nextID, username]
            sql = ''' INSERT INTO users (UID, Username) VALUES(?,?)'''
            userdb_connect.execute(sql, tuple(f))
            userdb_connect.commit()
        else:
            no_name = qtw.QMessageBox()
            no_name.setIcon(qtw.QMessageBox.Warning)
            no_name.setText(f"Please enter a valid username.")
            no_name.setWindowTitle("No username entered")
            no_name.setStandardButtons(qtw.QMessageBox.Ok)
            no_name.addButton("ayo",qtw.QMessageBox.YesRole)
            no_name.exec()

    def remove(self):
        delete = qtw.QMessageBox()
        delete.setIcon(qtw.QMessageBox.Warning)
        delete.setText(f"Are you sure you would like to remove the selected user? \n{self.user_list.currentText()}\n *Note* This will also remove all decks and notes created by this user.")
        delete.setWindowTitle("Remove User")
        delete.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        returnval = delete.exec()
        if returnval == qtw.QMessageBox.Ok:
            self.deleteUser()

    def deckList(self):
        if not self.user_list.currentText:
            no_name = qtw.QMessageBox()
            no_name.setIcon(qtw.QMessageBox.Warning)
            no_name.setText(f"There is no user selected")
            no_name.setWindowTitle("No User Selected")
            no_name.setStandardButtons(qtw.QMessageBox.Ok)
            no_name.exec()
        else:
            self.userID = self.user_list.currentText()[-5:-1]
            for i in self.getUserDecks():
                self.decks.addItem(i[2])
            self.setCentralWidget(self.WDeck)

    def deleteUser(self):
        ID = self.user_list.currentText()[-5:-1]
        print(ID)
        sql = f''' DELETE FROM users WHERE UID="{ID}"'''
        userdb_connect.execute(sql)
        userdb_connect.commit()
        self.user_list.removeItem(self.user_list.currentIndex())

class deckMenu(qtw.QWidget):
    def __init__(self,a):
        super().__init__()
        self.ID = a
        self.deckSelect = qtw.QGridLayout()
    
        self.decks = qtw.QListWidget()

        self.selectDeck = qtw.QPushButton("Select Deck")
        self.selectDeck.clicked.connect(self.openDeck)

        self.createDeck = qtw.QPushButton("Create a New Deck")
        self.createDeck.clicked.connect(self.newDeck)

        self.deleteDeck = qtw.QPushButton("Delete Selected Deck")
        self.deleteDeck.clicked.connect(self.removeDeck)

        self.goBack = qtw.QPushButton("Return to user select")
        self.goBack.clicked.connect(self.mainMenu)

        self.deckSelect.addWidget(self.decks,0,0,1,4)
        self.deckSelect.addWidget(self.selectDeck,1,0,1,1)
        self.deckSelect.addWidget(self.createDeck,1,1,1,1)
        self.deckSelect.addWidget(self.deleteDeck,1,2,1,1)
        self.deckSelect.addWidget(self.goBack,1,3,1,1)
        
        self.setLayout(self.deckSelect)
        self.getDeckList()

    def getDeckList(self):
        self.decks.clear()
        sql = f'''SELECT * FROM decks WHERE UID = "{self.ID}"'''
        decks =userdb_connect.execute(sql)
        self.deckL = [x for x in decks]
        for i,j in enumerate(self.deckL):
            self.decks.addItem(f"{i+1}: {j[2]}")
        
    def openDeck(self):
        if self.decks.currentItem():
            t = self.decks.currentItem().text()
            self.parentWidget().sDeck(t[len(str(self.getIndex(t)))+2:])
        else:
            nodeck = qtw.QMessageBox()
            nodeck.setIcon(qtw.QMessageBox.Warning)
            nodeck.setText(f"There is no deck currently selected")
            nodeck.setWindowTitle("Please select a deck")
            nodeck.setStandardButtons(qtw.QMessageBox.Ok)
            nodeck.exec()   

    def mainMenu(self):
        self.parentWidget().menuSel()

    def newDeck(self):
        text, ok =  qtw.QInputDialog.getText(self, "Please enter the name of the deck", "Deck Name:")
        if ok and text:
            self.parentWidget().cDeck(text,-1)

    def removeDeck(self):
        if self.decks.currentItem():
            ind = (self.getIndex(self.decks.currentItem().text()))
            b = self.deckL[ind]
            sql = f'''DELETE FROM decks WHERE DID = "{b[0]}"'''
            userdb_connect.execute(sql)
            userdb_connect.commit()
            self.getDeckList()
        else:
            nodeck = qtw.QMessageBox()
            nodeck.setIcon(qtw.QMessageBox.Warning)
            nodeck.setText(f"There is no deck currently selected")
            nodeck.setWindowTitle("Please select a deck")
            nodeck.setStandardButtons(qtw.QMessageBox.Ok)
            nodeck.exec()
    
    def getIndex(self,a):
        text = ""
        for i in a:
            if i == ":":
                break
            text += i
        return int(text) -1

    
class selDeck(qtw.QWidget):
    def __init__(self, dName):
        super().__init__()
        self.gLayout = qtw.QGridLayout()
        self.dName = dName

        self.deckSelect = qtw.QPushButton("Return to Deck Select")
        self.deckSelect.clicked.connect(self.decksel)

        self.gLayout.addWidget(self.deckSelect,0,0,1,1)

        self.setLayout(self.gLayout)

    def decksel(self):
        self.parentWidget().deckSel()

class createDeck(qtw.QWidget):
    def __init__(self, name, ID, new):
        super().__init__()
        self.ID = ID
        self.dName = name
        self.new = new
        self.gLayout = qtw.QGridLayout()

        self.deckSelect = qtw.QPushButton("Return to Deck Select")
        self.deckSelect.clicked.connect(self.deckSel)

        self.promptLabel = qtw.QLabel("Relevant question/prompt")
        self.contentLabel = qtw.QLabel("Content")

        self.titleLE = qtw.QLineEdit()
        self.contentTE = qtw.QTextEdit()

        self.nextB = qtw.QPushButton("Save/Next Card")
        self.nextB.clicked.connect(self.next)

        self.titleLE.setPlaceholderText("Prompt e.g. 'What is the powerhouse of the cell?'")
        self.contentTE.setPlaceholderText("Content e.g. 'An organelle found in large numbers in most cells, in which the biochemical processes of respiration and energy production occur. It has a double membrane, the inner part being folded inwards to form layers (cristae).'")

        self.gLayout.addWidget(self.promptLabel,0,0,1,1)
        self.gLayout.addWidget(self.titleLE,1,0,1,2)
        self.gLayout.addWidget(self.contentLabel,2,0,1,1)
        self.gLayout.addWidget(self.contentTE,3,0,1,2)
        self.gLayout.addWidget(self.nextB,4,0,1,1)
        self.gLayout.addWidget(self.deckSelect,4,1,1,1)

        if self.new == -1:
            self.createSQL()

        self.setLayout(self.gLayout)

    def next(self):
        pass
    
    def deckSel(self):
        self.parentWidget().deckSel()

    def createSQL(self):
        sql = ''' INSERT INTO decks (UID, deckName) VALUES(?,?)'''
        userdb_connect.execute(sql, (self.ID,self.dName))
        userdb_connect.commit()

        sql = f''' SELECT * FROM decks WHERE deckName = "{self.dName}"'''
        self.DID = [x for x in userdb_connect.execute(sql)][0][0]
        

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.setWindowTitle("Note Taking App")
        self.setCentralWidget(mainMenu())
    
    def deckSel(self):
        self.setWindowTitle("Deck Selection")
        self.setCentralWidget(deckMenu(self.ID))

    def menuSel(self):
        self.setWindowTitle("Note Taking App")
        self.setCentralWidget(mainMenu())

    def sDeck(self, dName):
        self.setWindowTitle(dName)
        self.setCentralWidget(selDeck(dName))

    def cDeck(self, dName, new):
        self.setWindowTitle(f"Edit: {dName}")
        self.setCentralWidget(createDeck(dName,self.ID , new))


def main():
    app = qtw.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()