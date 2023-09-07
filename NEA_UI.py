import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
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

        self.fl.addWidget(self.user_list,0,0,2,1)
        self.fl.addWidget(self.add_user,1,0,1,1)
        self.fl.addWidget(self.new_user_button,1,1,1,1)

        widget = qtw.QWidget()
        widget.setLayout(self.fl)
        self.setCentralWidget(widget)

    def addUser(self):
        self.user_list.addItem(self.add_user.text)

        
        
app = qtw.QApplication([])
window = MainWindow()
window.show()
app.exec_()