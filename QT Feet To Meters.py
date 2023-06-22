import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion Tool")
        fl = qtw.QFormLayout()
        self.feet = qtw.QLineEdit()
        self.feet.setPlaceholderText("feet")
        self.label = qtw.QLabel("0.0")
        self.button = qtw.QPushButton("GO!")
        self.button.clicked.connect(self.tchanged)

        open_action = qtw.QAction("Open",self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_text)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(open_action)

        file_menu.addSeparator()
        file_menu.addAction("Exit",self.close)

        edit_menu = menubar.addMenu('Edit')
        copy_action = qtw.QAction("Copy",self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)

        fl.addRow("Feet",self.feet)
        fl.addRow("Metres",self.label)
        fl.addRow("",self.button)
        widget = qtw.QWidget()
        widget.setLayout(fl)
        self.setCentralWidget(widget)

    def tchanged(self,new_text):
        try:
            self.label.setText(str(round(float(self.feet.text())*0.3048,2)))
        except ValueError:
            self.label.setText("Please enter numerical values only")
    def open_text(self):
        return
    def copy(self):
        clipboard = qtw.QApplication.clipboard()
        clipboard.setText(self.label.text())
app = qtw.QApplication([])
window = MainWindow()
window.show()
app.exec_()