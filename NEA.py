import PyQt5.QtWidgets as qtw
import sqlite3
import random

users_db = "users.db"
userdb_connect = sqlite3.connect(users_db)
userdb_connect.execute("PRAGMA foreign_keys = 1")

def getNotes(DID):
    sql = f"""SELECT * FROM notes WHERE DID = '{DID}'"""
    c = userdb_connect.execute(sql)
    return [x for x in c]

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

def getIndex(a):
    text = ""
    for i in a:
        if i == ":":
            break
        text += i
    return int(text) -1

class startMenu(qtw.QWidget):   
    def __init__(self):
        super().__init__()


        self.menuGrid = qtw.QGridLayout()

        self.user_list  = qtw.QComboBox()

        sql = """ SELECT * FROM users"""
        c = userdb_connect.execute(sql)
        count = 1
        for i in c:
            self.user_list.addItem(f"{i[1]} [{i[0]}]")
            self.userID = i[0]
            count += 1

        self.sUser = qtw.QLabel("Select User:")
        self.newUser = qtw.QLabel("Add a New User:")

        self.add_user   = qtw.QLineEdit()
        self.add_user.setPlaceholderText("Enter New User Name Here:")

        self.new_user_button = qtw.QPushButton("Add new User")
        self.new_user_button.clicked.connect(self.addUser)

        self.removeUser = qtw.QPushButton("Remove Selected User")
        self.removeUser.clicked.connect(self.remove)

        self.startB = qtw.QPushButton("Start")
        self.startB.clicked.connect(self.deckSelect)

        self.menuGrid.addWidget(self.sUser,0,0,1,3)
        self.menuGrid.addWidget(self.newUser,2,0,1,3)
        self.menuGrid.addWidget(self.user_list,1,0,1,3)
        self.menuGrid.addWidget(self.add_user,3,0,1,1)
        self.menuGrid.addWidget(self.new_user_button,3,1,1,1)
        self.menuGrid.addWidget(self.removeUser,3,2,1,1)
        self.menuGrid.addWidget(self.startB,4,0,1,3)

        self.setLayout(self.menuGrid)

    def deckSelect(self):
        self.parentWidget().deckSel(self.user_list.currentText()[-5:-1])

    
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

    def deleteUser(self):
        self.userID = self.user_list.currentText()[-5:-1]
        sql = f''' DELETE FROM users WHERE UID="{self.userID}"'''
        userdb_connect.execute(sql)
        userdb_connect.commit()
        self.user_list.removeItem(self.user_list.currentIndex())

class deckMenu(qtw.QWidget):
    def __init__(self,ID):
        super().__init__()
        self.ID = ID
        self.deckSelect = qtw.QGridLayout()
    
        self.decks = qtw.QListWidget()

        self.dLabel = qtw.QLabel("List of Decks:")

        self.editDeck = qtw.QPushButton("Create a New Deck")
        self.editDeck.clicked.connect(self.newDeck)

        self.deleteDeck = qtw.QPushButton("Delete Selected Deck")
        self.deleteDeck.clicked.connect(self.removeDeck)

        self.goBack = qtw.QPushButton("Return")
        self.goBack.clicked.connect(self.mainMenu)

        self.decks.doubleClicked.connect(self.openDeck)

        self.deckSelect.addWidget(self.dLabel,0,0,1,3)
        self.deckSelect.addWidget(self.decks,1,0,1,3)
        self.deckSelect.addWidget(self.editDeck,2,0,1,1)
        self.deckSelect.addWidget(self.deleteDeck,2,1,1,1)
        self.deckSelect.addWidget(self.goBack,2,2,1,1)
        
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
            DID = self.deckL[getIndex(t)][0]
            self.parentWidget().sDeck(DID)
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
            sql = ''' INSERT INTO decks (UID, deckName) VALUES(?,?)'''
            userdb_connect.execute(sql, (self.ID,text))
            userdb_connect.commit()

            sql = f''' SELECT * FROM decks WHERE deckName = "{text}"'''
            DID = [x for x in userdb_connect.execute(sql)][-1][0]
            self.parentWidget().eDeck(DID)


    def removeDeck(self):
        if self.decks.currentItem():
            delete = qtw.QMessageBox()
            delete.setIcon(qtw.QMessageBox.Warning)
            delete.setText(f"Are you sure you would like to remove the selected deck? \n{self.decks.currentItem().text()}")
            delete.setWindowTitle("Remove User")
            delete.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            returnval = delete.exec()
            if returnval == qtw.QMessageBox.Ok:
                ind = (getIndex(self.decks.currentItem().text()))
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
    
class selDeck(qtw.QWidget):
    def __init__(self, dName, DID):
        super().__init__()
        self.gLayout = qtw.QGridLayout()
        self.dName = dName
        self.DID = DID

        self.sumLabel = qtw.QLabel()    
        self.summaryLabel()
        self.label = qtw.QLabel(f" Deck:{self.dName}")
        

        self.deckSelect = qtw.QPushButton("Return")
        self.deckSelect.clicked.connect(self.decksel)

        self.viewN = qtw.QPushButton("View Notes")
        self.viewN.clicked.connect(self.vNote)

        self.study =  qtw.QPushButton("Study Deck")
        self.study.clicked.connect(self.studyDeck)

        self.edit = qtw.QPushButton("Edit/Add notes")
        self.edit.clicked.connect(self.editDeck)

        self.addSummary = qtw.QPushButton("Edit/Add Summary")
        self.addSummary.clicked.connect(self.summary)

        self.gLayout.addWidget(self.sumLabel,1,0,1,5)
        self.gLayout.addWidget(self.label,0,0,1,5)
        self.gLayout.addWidget(self.deckSelect,2,4,1,1)
        self.gLayout.addWidget(self.addSummary,2,1,1,1)
        self.gLayout.addWidget(self.viewN,2,2,1,1)
        self.gLayout.addWidget(self.study,2,3,1,1)
        self.gLayout.addWidget(self.edit,2,0,1,1)

        self.setLayout(self.gLayout)


    def summary(self):
        text, ok =  qtw.QInputDialog.getText(self, "Enter Topic Summary", "Summary:")
        if ok and not text == "":
            sql = f"""UPDATE decks SET  summary = '{text}' WHERE DID = {self.DID} """
            userdb_connect.execute(sql)
            userdb_connect.commit()
            self.summaryLabel()

    def decksel(self):
        self.parentWidget().deckSel()

    def vNote(self):
        self.parentWidget().vNote(self.DID)

    def studyDeck(self):
        if getNotes(self.DID):
            #self.parentWidget().oStudy(self.DID)
            self.parentWidget().study(0,self.DID)

        else:
            emptydeck = qtw.QMessageBox()
            emptydeck.setIcon(qtw.QMessageBox.Warning)
            emptydeck.setText(f"This deck is empty, add notes to the deck to study")
            emptydeck.setWindowTitle("Empty Deck")
            emptydeck.setStandardButtons(qtw.QMessageBox.Ok)
            emptydeck.exec()  

    def editDeck(self):
        self.parentWidget().eDeck(self.DID)

    def summaryLabel(self):
        sql = f"""SELECT summary FROM decks WHERE DID = {self.DID}"""
        self.sum = [x for x in userdb_connect.execute(sql)][0][0]
        if not self.sum:
            self.sum = "No Deck Summary\nDeck Summary e.g. 'Cells are the building blocks of life. All living organisms are made up of cells. Cells need to be viewed through a microscope. Cell membrane Controls entry and exit of substances such as oxygen and carbon dioxide.'"
        self.sumLabel.setText(f"Summary:\n{self.sum}")

class editDeck(qtw.QWidget):
    def __init__(self, name, ID, DID, edit=False):
        super().__init__()
        self.NID = False
        self.ID = ID
        self.dName = name
        self.DID = DID
        self.edit = edit
        self.gLayout = qtw.QGridLayout()

        self.deckSelect = qtw.QPushButton("Return")
        self.deckSelect.clicked.connect(self.sDeck)

        self.promptLabel = qtw.QLabel("Relevant question/prompt")
        self.contentLabel = qtw.QLabel("Content")

        self.titleLE = qtw.QLineEdit()
        self.contentTE = qtw.QTextEdit()

        self.nextB = qtw.QPushButton("Save/Next Card")
        self.nextB.clicked.connect(self.next)

        self.viewNotes =  qtw.QPushButton("View Notes")
        self.viewNotes.clicked.connect(self.vNotes)

        if self.edit:
            self.NID = self.edit[1]
            self.titleLE.setText(self.edit[2])
            self.contentTE.setText(self.edit[3])

        self.titleLE.setPlaceholderText("Prompt e.g. 'What is the powerhouse of the cell?'")
        self.contentTE.setPlaceholderText("Content e.g. 'An organelle found in large numbers in most cells, in which the biochemical processes of respiration and energy production occur. It has a double membrane, the inner part being folded inwards to form layers (cristae).'")

        self.gLayout.addWidget(self.viewNotes,4,1,1,1)
        self.gLayout.addWidget(self.promptLabel,0,0,1,1)
        self.gLayout.addWidget(self.titleLE,1,0,1,3)
        self.gLayout.addWidget(self.contentLabel,2,0,1,1)
        self.gLayout.addWidget(self.contentTE,3,0,1,3)
        self.gLayout.addWidget(self.nextB,4,0,1,1)
        self.gLayout.addWidget(self.deckSelect,4,2,1,1)

        self.setLayout(self.gLayout)

    def vNotes(self):
        self.parentWidget().vNote(self.DID)

    def next(self):
        if not self.contentTE.toPlainText() or not self.titleLE.text():
            emptyfields = qtw.QMessageBox()
            emptyfields.setIcon(qtw.QMessageBox.Warning)
            emptyfields.setText(f"There are empty field(s)")
            emptyfields.setWindowTitle("Empty Fields")
            emptyfields.setStandardButtons(qtw.QMessageBox.Ok)
            emptyfields.exec()
        else:
            if not self.NID:
                sql = '''INSERT INTO notes (DID, Title, Content) VALUES(?,?,?)'''
                userdb_connect.execute(sql,(self.DID, self.titleLE.text(), self.contentTE.toPlainText()))
                userdb_connect.commit()

                self.contentTE.clear()
                self.titleLE.clear()
            else:
                delete_sql = f'''DELETE FROM notes WHERE NID = "{self.NID}"'''
                userdb_connect.execute(delete_sql)

                sql = '''INSERT INTO notes (DID, Title, Content) VALUES(?,?,?)'''
                userdb_connect.execute(sql,(self.DID, self.titleLE.text(), self.contentTE.toPlainText()))
                userdb_connect.commit()

                self.edit = self.NID = False
                self.contentTE.clear()
                self.titleLE.clear()
                
    
    def sDeck(self):
        self.parentWidget().sDeck(self.DID)
        
class notesList(qtw.QWidget):
    def __init__(self, dName, DID):
        super().__init__()
        self.DID = DID
        self.dName = dName
        self.gLayout = qtw.QGridLayout()

        self.nList = getNotes(self.DID)
        self.notes = qtw.QListWidget()
        for i,j in enumerate(self.nList):
            self.notes.addItem(f"{i+1}: {j[2]}:\n{j[3]}")

        self.nLabel =  qtw.QLabel("List of notes:")

        self.editDeck = qtw.QPushButton("Return")
        self.editDeck.clicked.connect(self.deckE)
        
        self.notes.doubleClicked.connect(self.editNote)

        self.gLayout.addWidget(self.nLabel,0,0,1,1)
        self.gLayout.addWidget(self.notes,1,0,1,1)
        self.gLayout.addWidget(self.editDeck,2,0,1,1)

        self.setLayout(self.gLayout)

    def deckE(self):
        self.parentWidget().sDeck(self.DID)

    
    def editNote(self):
        ind = (getIndex(self.notes.currentItem().text()))
        note = (self.nList[ind])
        self.parentWidget().eDeck(self.DID,note)

class studying(qtw.QWidget):
    def __init__(self,mode, DID, dName):
        super().__init__()
        print(mode)
        self.gLayout = qtw.QGridLayout()
        self.mode = mode
        self.DID =  DID
        self.dName = dName


        self.notes =  getNotes(self.DID)
        self.noteIndex = 0

        self.Return =  qtw.QPushButton("Return")
        self.Return.clicked.connect(self.deckSel)

        self.flip = qtw.QPushButton("Flip Flashcard")
        
        self.nextCard = qtw.QPushButton("Next")
        self.nextCard.clicked.connect(self.next)

        self.prevCard = qtw.QPushButton("Previous")
        self.prevCard.clicked.connect(self.prev)

        self.titleText = qtw.QLabel(f"Title:\n{self.notes[self.noteIndex][2]}")
        self.content = qtw.QLabel(f"Content:\n{self.notes[self.noteIndex][3]}")

        self.ans = qtw.QLineEdit()
        self.ans.setPlaceholderText("Answer:")
        self.ans.returnPressed.connect(self.enter)

        self.confirm = qtw.QPushButton("Enter")
        self.confirm.clicked.connect(self.enter)

        self.prompt = qtw.QLabel()

        self.understanding = qtw.QLabel()


        self.tryTest = qtw.QPushButton("Test Yourself")
        self.tryTest.clicked.connect(self.testMode)

        if self.mode == 0:
            self.gLayout.addWidget(self.tryTest,3,0,1,1)
            self.gLayout.addWidget(self.titleText,0,0,1,2)
            self.gLayout.addWidget(self.content,1,0,1,2)
            self.gLayout.addWidget(self.nextCard,2,1,1,1)
            self.gLayout.addWidget(self.prevCard,2,0,1,1)
        elif self.mode == 1:
            self.untested = self.notes.copy()
            self.half = []
            self.known = []
            self.update()
            self.gLayout.addWidget(self.ans,2,0,1,2)
            self.gLayout.addWidget(self.confirm,3,0,1,1)
            self.gLayout.addWidget(self.understanding,0,0,1,1)
            self.gLayout.addWidget(self.prompt,1,0,1,1)
            
        self.gLayout.addWidget(self.Return,3,1,1,1)

        self.setLayout(self.gLayout)

    def update(self):
        self.ans.clear()
        self.understanding.setText(f"Unleanrt :{len(self.untested)}\nHalf learnt :{len(self.half)}\nFully learn :{len(self.known)}")
        self.current = ["-","-","Placeholder","Placeholder"]
        if self.untested:
            self.current = random.choice(self.untested)
        elif self.half:
            self.current = random.choice(self.half)
        else:
            done = qtw.QMessageBox()
            done.setIcon(qtw.QMessageBox.Warning)
            done.setText(f"Congratulations! You have finished studying for the whole deck!\nReturning to previous page.")
            done.setWindowTitle("Done!")
            done.addButton("Ok", qtw.QMessageBox.YesRole)
            done.exec()
            self.parentWidget().oStudy(self.DID)
        self.prompt.setText(self.current[2])

            
        

    def enter(self):
        def clicked(btn):
            txt  = btn.text()
            if txt == "Wrong":
                self.update()
            elif txt == "Half Right":
                if self.current in self.untested:
                    self.untested.remove(self.current)
                    self.half.append(self.current)
                self.update()
            elif txt == "Close Enough" or txt == "Nice":
                if self.current in self.untested:
                    self.untested.remove(self.current)
                else:
                    self.half.remove(self.current)
                self.known.append(self.current)
                self.update()

        if not self.ans.text():
            ent = qtw.QMessageBox()
            ent.setIcon(qtw.QMessageBox.Warning)
            ent.setText(f"Please enter the solution to the prompt!")
            ent.setWindowTitle("Please provide an answer")
            ent.addButton("Ok", qtw.QMessageBox.YesRole)
            ent.buttonClicked.connect(clicked)
            ent.exec()
        else:
            if self.current[3] == self.ans.text():
                ent = qtw.QMessageBox()
                ent.setIcon(qtw.QMessageBox.Information)
                ent.setText(f"That is correct!")
                ent.setWindowTitle("Correct!")
                ent.addButton("Nice", qtw.QMessageBox.YesRole)
                ent.buttonClicked.connect(clicked)
                ent.exec()
            else:
                ent = qtw.QMessageBox()
                ent.setIcon(qtw.QMessageBox.Question)
                ent.setWindowTitle("Accuracy of the answer?")
                ent.setText(f"The answer was supposed to be: {self.current[3]}\n\nYou entered: {self.ans.text()}")
                ent.addButton("Wrong", qtw.QMessageBox.YesRole)
                ent.addButton("Half Right", qtw.QMessageBox.YesRole)
                ent.addButton("Close Enough", qtw.QMessageBox.YesRole)
                ent.buttonClicked.connect(clicked)
                ent.exec()


    def testMode(self):
        self.parentWidget().study(1,self.DID)

    def deckSel(self):
        self.parentWidget().sDeck(self.DID)

    def updateLabels(self):
        self.titleText.setText(f"Title:\n{self.notes[self.noteIndex][2]}")
        self.content.setText(f"Content:\n{self.notes[self.noteIndex][3]}")

    def next(self):
        if self.noteIndex + 1 >= len(self.notes):
            self.noteIndex = 0 
        else:
            self.noteIndex += 1
        self.updateLabels()

    def prev(self):
        if self.noteIndex <= 0:
            self.noteIndex = len(self.notes)-1
        else:
            self.noteIndex -= 1
        self.updateLabels()
    

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.setWindowTitle("Revision Tool")
        self.setCentralWidget(startMenu())
    
    def deckSel(self,ID):
        self.setWindowTitle("Deck Selection")
        self.setCentralWidget(deckMenu(ID))

    def menuSel(self):
        self.setWindowTitle("Revision Tool")
        self.setCentralWidget(startMenu())

    def sDeck(self, DID):
        self.setWindowTitle(f"Deck: {getdName(DID)}")
        self.setCentralWidget(selDeck(getdName(DID), DID))

    def eDeck(self, DID, edit = False):
        self.setWindowTitle(f"Edit: {getdName(DID)}")
        self.setCentralWidget(editDeck(getdName(DID),self.ID , DID, edit))

    def vNote(self, DID):
        self.setCentralWidget(notesList(getdName(DID), DID))

    def study(self,mode,DID):
        if mode == 0:
            self.setWindowTitle(f"Learning notes in: {getdName(DID)}")
        elif mode == 1:
            self.setWindowTitle(f"Testing notes in: {getdName(DID)}")
        self.setCentralWidget(studying(mode,DID,getdName(DID)))


def getdName(DID):
    sql = f"""SELECT deckName FROM decks WHERE DID = '{DID}'"""
    return [x for x in (userdb_connect.execute(sql))][0][0]

def main():
    app = qtw.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()