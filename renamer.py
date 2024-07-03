__author__ = "Juno Park"
__github__ = "https://github.com/junopark00/multi-renamer"


import os

from PySide2 import QtWidgets, QtCore, QtGui

from renamer_ui import RenamerUI


class RenameThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.rename_dict = {}

    def set_params(self, rename_dict) -> None:
        """
        Set the parameters for the thread.

        Args:
            rename_dict (dict): Dictionary containing the rename data.
        """
        self.rename_dict = rename_dict

    def run(self):
        """
        Rename files in the given directory by replacing 'before_str' with 'after_str'.
        """
        for before_str, after_str in self.rename_dict.items():
            for dirpath, _, filenames in os.walk(self.parent.path):
                for filename in filenames:
                    if before_str in filename:
                        old_filepath = os.path.join(dirpath, filename)
                        new_filename = filename.replace(before_str, after_str)
                        new_filepath = os.path.join(dirpath, new_filename)

                        os.rename(old_filepath, new_filepath)
        

class MultiRenamer(RenamerUI):
    def __init__(self):
        super().__init__()
        self.rename_thread = RenameThread(self)
        self.set_ui()
        self.connections()
        
    def connections(self) -> None:
        """
        Connects the signals to slots.
        """
        self.button_browse.clicked.connect(self.browse)
        self.button_add.clicked.connect(self.add)
        self.button_remove.clicked.connect(self.remove)
        self.button_rename.clicked.connect(self.rename)
        self.button_ascend.clicked.connect(lambda: self.sort("ascend"))
        self.button_descend.clicked.connect(lambda: self.sort("descend"))
        self.rename_thread.finished.connect(self.on_rename_finished)
        
    def browse(self) -> None:
        """
        Gets the directory path from the user.
        """
        self.path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.lineEdit_path.setText(self.path)
        
        # Get file list from path
        self.get_files()
        
    def get_files(self) -> None:
        """
        Gets the files from the directory.
        """
        if not self.path:
            return
        
        self.list_widget.clear()
        
        files = sorted(os.listdir(self.path))
        for file in files:
            item = QtWidgets.QListWidgetItem(self.list_widget_2)
            item.setText(file)
            self.list_widget_2.addItem(item)
    
    def sort(self, sorting) -> None:
        """
        Sorts the items in the list_widget.
        
        Args:
            sorting (str): The sorting order.
        """
        if sorting == "ascend":
            order = QtCore.Qt.AscendingOrder
        else:
            order = QtCore.Qt.DescendingOrder
        
        self.list_widget_2.sortItems(order)
        
    def add(self) -> None:
        """
        Adds a new item to the list_widget.
        """
        item_widget = QtWidgets.QWidget()
        item_layout = QtWidgets.QHBoxLayout(item_widget)
        
        line_edit1 = QtWidgets.QLineEdit()
        line_edit2 = QtWidgets.QLineEdit()
        
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(
            QtGui.QIcon(
                self.style().standardIcon(
                    QtWidgets.QStyle.SP_ArrowRight
                    )
                ).pixmap(
                    QtCore.QSize(20, 20)
                    )
            )
        icon_label.setFixedSize(20, 20)
        icon_label.setScaledContents(True)
        
        item_layout.addWidget(line_edit1)
        item_layout.addWidget(icon_label)
        item_layout.addWidget(line_edit2)
        
        item = QtWidgets.QListWidgetItem(self.list_widget)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item_widget)
        item.setSizeHint(item_widget.sizeHint())
        
    def remove(self) -> None:
        """
        Removes the last item from the list_widget.
        """
        count = self.list_widget.count()
        if count >= 1:
            item = self.list_widget.takeItem(count - 1)
            del item

    def rename(self) -> None:
        """
        Renames the files in the directory.
        """
        if not self.validate_path():
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid Path")
            return
        
        if self.list_widget.count() == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "No Items to Rename")
            return
        
        # Disable rename button during operation to prevent re-entrancy
        self.button_rename.setEnabled(False)
        
        rename_dict = {}
        
        # Iterate through each item in the list_widget
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            item_widget = self.list_widget.itemWidget(item)
            
            if item_widget:
                # Assuming the structure of item_widget is QHBoxLayout with QLineEdit at index 0 and 2
                line_edit1 = item_widget.layout().itemAt(0).widget()
                line_edit2 = item_widget.layout().itemAt(2).widget()
                
                if line_edit1 and line_edit2:
                    before_str = line_edit1.text()
                    after_str = line_edit2.text()
                    
                    # if both strings are empty, skip
                    if not before_str and not after_str:
                        continue
                    
                    # if only one string is empty, show a message box and return
                    elif not before_str or not after_str:
                        QtWidgets.QMessageBox.critical(self, "Error", "Both fields must be filled")
                        self.button_rename.setEnabled(True)
                        return
                    
                    elif before_str == after_str:
                        continue
                    
                    # add rename data to dictionary
                    rename_dict[before_str] = after_str
        
        # Run thread       
        self.rename_thread.set_params(rename_dict)
        self.rename_thread.start()
        
    def on_rename_finished(self) -> None:
        """
        If the renaming operation is successful, show a message box and clear the list_widget.
        """
        self.button_rename.setEnabled(True)
        self.list_widget_2.clear()
        self.get_files()
        QtWidgets.QMessageBox.information(self, "Success", "Files Renamed Successfully")
    
    def validate_path(self) -> bool:
        """
        Validates the path.
        
        Returns:
            bool: True if the path is valid, False otherwise.
        """
        path = self.lineEdit_path.text()
        if not path:
            return False
        
        if not os.path.exists(path):
            return False
        
        return True

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MultiRenamer()
    window.show()
    app.exec_()
