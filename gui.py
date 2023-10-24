import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt


class GUI(QtWidgets.QMainWindow):
    def __init__(self, db):
        self.db = db

    def run(self):
        app = QtWidgets.QApplication(sys.argv)

        super().__init__()
        self.setCentralWidget(RunQueryWindow(self.db))
        self.show()
        app.exec()


class RunQueryWindow(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.input = QtWidgets.QLineEdit()
        layout.addWidget(self.input)

        run_query_button = QtWidgets.QPushButton("Выполнить запросик")
        run_query_button.clicked.connect(self.run_query)
        layout.addWidget(run_query_button)

        self.error_label = QtWidgets.QLabel()
        layout.addWidget(self.error_label)

        self.table = QtWidgets.QTableView()
        layout.addWidget(self.table)

    def run_query(self):
        query = self.input.text()
        try:
            (columns, comments) = self.db.select(query)
            self.table.setModel(TableModel(columns, comments))
            self.error_label.setText("Запрос прошёл успешно!")
        except Exception as e:
            self.error_label.setText(str(e))


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
