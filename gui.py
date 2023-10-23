import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt


class GUI:
    def __init__(self, db):
        self.db = db

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow(["Id", "Name", "Age"], [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
        ])
        window.show()

        app.exec()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, columns, data):
        super(TableModel, self).__init__()
        self.columns = columns
        self._data = data

    def data(self, index, role):
        """Cell value wrapper."""
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]

            if orientation == Qt.Orientation.Vertical:
                return section + 1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, columns, data):
        super().__init__()

        self.table = QtWidgets.QTableView()

        self.model = TableModel(columns, data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)
