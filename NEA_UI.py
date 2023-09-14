import PyQt5.QtWidgets as qtw
import sqlite3

users_db = "users.db"
userdb_connect = sqlite3.connect(users_db)

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        self.page = 0
        super().__init__()
        self.setWindowTitle("Notes Taking App")

        self.menuGrid = qtw.QGridLayout()
        self.deckSelect = qtw.QGridLayout()

        self.user_list  = qtw.QComboBox()
        self.users = qtw.QListWidget()

        self.add_user   = qtw.QLineEdit()
        self.add_user.setPlaceholderText("Enter New User Name Here:")

        self.new_user_button = qtw.QPushButton("Add new User")
        self.new_user_button.clicked.connect(self.addUser)

        self.removeUser = qtw.QPushButton("Remove Selected User")
        self.removeUser.clicked.connect(self.remove)

        self.startB = qtw.QPushButton("Start")
        self.startB.clicked.connect(self.deckList)

        self.selectDeck = qtw.QPushButton("Use Selected Deck")
        self.selectDeck.clicked.connect(self.openDeck)

        sql = """ SELECT * FROM users"""
        c = userdb_connect.execute(sql)
        for i in c:
            self.users.addItem("Ayou")
            self.user_list.addItem(f"{i[1]} [{i[0]}]")

        self.deckSelect.addWidget(self.users,0,0,1,1)
        
        self.menuGrid.addWidget(self.user_list,0,0,1,3)
        self.menuGrid.addWidget(self.add_user,1,0,1,1)
        self.menuGrid.addWidget(self.new_user_button,1,1,1,1)
        self.menuGrid.addWidget(self.removeUser,1,2,1,1)
        self.menuGrid.addWidget(self.startB,2,0,1,3)

        self.WDeck = qtw.QWidget()
        self.WDeck.setLayout(self.deckSelect)

        self.start = qtw.QWidget()
        self.start.setLayout(self.menuGrid)
        self.setCentralWidget(self.start)

    def deckList(self):
        self.setCentralWidget(self.WDeck)


    def getNextUID(self):
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

    def remove(self):
        delete = qtw.QMessageBox()
        delete.setIcon(qtw.QMessageBox.Warning)
        delete.setText(f"Are you sure you would like to remove the selected user? {self.user_list.currentText()}")
        delete.setWindowTitle("Remove User")
        delete.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        returnval = delete.exec()
        if returnval == qtw.QMessageBox.Ok:
            self.deleteUser()

    def deleteUser(self):
        ID = self.user_list.currentText()[-5:-1]
        print(ID)
        sql = f''' DELETE FROM users WHERE UID="{ID}"'''
        c = userdb_connect.execute(sql)
        userdb_connect.commit()
        self.user_list.removeItem(self.user_list.currentIndex())

    def addUser(self):
        nextID = self.getNextUID()
        username =  self.add_user.text()
        if username:
            self.user_list.addItem(f"{username} [{nextID}]")
            f = [nextID, username]
            sql = ''' INSERT INTO users (UID, Username) VALUES(?,?)'''
            c = userdb_connect.execute(sql, tuple(f))
            userdb_connect.commit()
        else:
            no_name = qtw.QMessageBox()
            no_name.setIcon(qtw.QMessageBox.Warning)
            no_name.setText(f"Please enter a valid username.")
            no_name.setWindowTitle("No username entered")
            no_name.setStandardButtons(qtw.QMessageBox.Ok)
            no_name.exec()


        
