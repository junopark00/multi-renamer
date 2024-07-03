__author__ = "Juno Park"
__github__ = "https://github.com/junopark00/multi-renamer"


from PySide2 import QtWidgets, QtCore, QtGui

import qdarktheme


class RenamerUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(RenamerUI, self).__init__()
        self.set_ui()
        self.center()
        self.test_connection()
        self.show()
        
    def set_ui(self) -> None:
        """
        Setup the UI of the application.
        """
        self.setWindowTitle("Multi Renamer")
        self.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.sub_layout_1 = QtWidgets.QVBoxLayout()
        self.sub_layout_2 = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.sub_layout_1)
        self.main_layout.addLayout(self.sub_layout_2)
        self.central_widget.setLayout(self.main_layout)
        self.hbox_1 = QtWidgets.QHBoxLayout()
        self.lineEdit_path = QtWidgets.QLineEdit()
        self.lineEdit_path.setPlaceholderText("/Path/to/Directory")
        self.lineEdit_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.hbox_1.addWidget(self.lineEdit_path)
        self.button_browse = QtWidgets.QPushButton("Browse")
        self.hbox_1.addWidget(self.button_browse)
        self.sub_layout_1.addLayout(self.hbox_1)
        self.hbox_2 = QtWidgets.QHBoxLayout()
        self.spacer = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_add = QtWidgets.QPushButton("Add")
        self.button_remove = QtWidgets.QPushButton("Remove")
        self.hbox_2.addItem(self.spacer)
        self.hbox_2.addWidget(self.button_add)
        self.hbox_2.addWidget(self.button_remove)
        self.sub_layout_1.addLayout(self.hbox_2)
        self.list_widget = QtWidgets.QListWidget()
        self.sub_layout_1.addWidget(self.list_widget)
        self.button_rename = QtWidgets.QPushButton("Click to Rename")
        self.sub_layout_1.addWidget(self.button_rename)
        self.hbox_3 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("File List")
        self.hbox_3.addWidget(self.label)
        self.spacer_2 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.hbox_3.addItem(self.spacer_2)
        self.button_ascend = QtWidgets.QPushButton()
        self.button_ascend.setIcon(
            QtGui.QIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowUp))
        )
        self.button_ascend.setFixedSize(30, 30)
        self.button_descend = QtWidgets.QPushButton()
        self.button_descend.setIcon(
            QtGui.QIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown))
        )
        self.button_descend.setFixedSize(30, 30)
        self.hbox_3.addWidget(self.button_ascend)
        self.hbox_3.addWidget(self.button_descend)
        self.sub_layout_2.addLayout(self.hbox_3)
        self.list_widget_2 = QtWidgets.QListWidget()
        self.list_widget_2.setFixedWidth(300)
        self.sub_layout_2.addWidget(self.list_widget_2)
        qdarktheme.setup_theme()
    
    def center(self) -> None:
        """
        Set the window to the center of the screen.
        """
        frame_geometry = self.frameGeometry()
        screen_center = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        
    def test_connection(self) -> None:
        """
        Test the connection between the UI and the backend.
        """
        self.button_add.clicked.connect(lambda: print("Add button clicked"))
        self.button_remove.clicked.connect(lambda: print("Remove button clicked"))
        self.button_rename.clicked.connect(lambda: print("Rename button clicked"))
        self.button_browse.clicked.connect(lambda: print("Browse button clicked"))
        self.button_ascend.clicked.connect(lambda: print("Ascend button clicked"))
        self.button_descend.clicked.connect(lambda: print("Descend button clicked"))
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    renamer_ui = RenamerUI()
    renamer_ui.show()
    app.exec_()