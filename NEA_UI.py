import PyQt5.QtWidgets as qtw
import sqlite3

users_db = "users.db"
userdb_connect = sqlite3.connect(users_db)

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wassup")
        self.fl = qtw.QGridLayout()
        self.user_list  = qtw.QComboBox()
        self.add_user   = qtw.QLineEdit()
        self.add_user.setPlaceholderText("Enter New User Name Here:")
        self.new_user_button = qtw.QPushButton("Add new User")
        self.new_user_button.clicked.connect(self.addUser)
        self.removeUser = qtw.QPushButton("Remove Selected User")
        self.removeUser.clicked.connect(self.remove)

        sql = """ SELECT * FROM users"""
        c = userdb_connect.execute(sql)
        for i in c:
            self.user_list.addItem(f"{i[1]} [{i[0]}]")

        self.fl.addWidget(self.user_list,0,0,1,3)
        self.fl.addWidget(self.add_user,1,0,1,1)
        self.fl.addWidget(self.new_user_button,1,1,1,1)
        self.fl.addWidget(self.removeUser,1,2,1,1)

        widget = qtw.QWidget()
        widget.setLayout(self.fl)
        self.setCentralWidget(widget)

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
        self.user_list.addItem(f"{username} [{nextID}]")
        f = [nextID, username]
        sql = ''' INSERT INTO users (UID, Username) VALUES(?,?)'''
        c = userdb_connect.execute(sql, tuple(f))
        userdb_connect.commit()

        
        
app = qtw.QApplication([])
window = MainWindow()
window.show()
app.exec_()