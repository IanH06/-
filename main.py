from NEA_UI import MainWindow
import PyQt5.QtWidgets as qtw

def main():
    app = qtw.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()