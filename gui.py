import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt


class GUI(QtWidgets.QMainWindow):
    def __init__(self, db):
        self.db = db

    def run(self):
        app = QtWidgets.QApplication(sys.argv)

        super().__init__()
        self.setCentralWidget(MainWidget(self.db))
        self.show()
        app.exec()


class MainWidget(QtWidgets.QTabWidget):
    def __init__(self, db):
        super().__init__()

        self.addTab(CommentsWindow(db), "Комментарии")
        self.addTab(UsersWindow(db), "Пользователи")
        self.addTab(RunQueryWindow(db), "Свой запрос")


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

        self.table = SortableTable()
        layout.addWidget(self.table)

    def run_query(self):
        query = self.input.text()
        try:
            (columns, comments) = self.db.select(query)
            self.table.setModel(TableModel(columns, comments))
            self.error_label.setText("Запрос прошёл успешно!")
        except Exception as e:
            self.error_label.setText(str(e))


class CommentsWindow(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        form = QtWidgets.QFormLayout()
        layout.addLayout(form)

        self.after = QtWidgets.QDateEdit(self)
        form.addRow("От:", self.after)
        self.until = QtWidgets.QDateEdit(self)
        form.addRow("До:", self.until)

        self.username_field = QtWidgets.QLineEdit(self)
        form.addRow("Имя пользователя:", self.username_field)

        self.title_field = QtWidgets.QLineEdit(self)
        form.addRow("Название видео:", self.title_field)

        self.content_field = QtWidgets.QLineEdit(self)
        form.addRow("Текст комментария:", self.content_field)

        exec_button = QtWidgets.QPushButton("Выполнить запрос")
        exec_button.clicked.connect(self.run)
        form.addRow(exec_button)

        self.error_label = QtWidgets.QLabel("Выполните запросик")
        layout.addWidget(self.error_label)

        self.table = SortableTable()
        layout.addWidget(self.table)

    def run(self):
        after = self.after.date().toPyDate()
        until = self.until.date().toPyDate()
        username = self.username_field.text()
        title = self.title_field.text()
        content = self.content_field.text()
        try:
            (columns, comments) = self.db.comments(
                after, until, username, title, content
            )
        except Exception as e:
            self.error_label.setText(str(e))
        else:
            self.table.setModel(TableModel(columns, comments))
            self.error_label.setText("Запрос выполнен успешно")


class UsersWindow(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        form = QtWidgets.QFormLayout()
        layout.addLayout(form)

        self.lower_bound = QtWidgets.QSpinBox(self)
        form.addRow("Не менее комментариев:", self.lower_bound)
        self.upper_bound = QtWidgets.QSpinBox(self)
        form.addRow("Не более комментариев:", self.upper_bound)

        self.username_field = QtWidgets.QLineEdit(self)
        form.addRow("Имя пользователя:", self.username_field)

        exec_button = QtWidgets.QPushButton("Выполнить запрос")
        exec_button.clicked.connect(self.run)
        form.addRow(exec_button)

        self.error_label = QtWidgets.QLabel("Выполните запросик")
        layout.addWidget(self.error_label)

        self.table = SortableTable()
        layout.addWidget(self.table)

    def run(self):
        username = self.username_field.text()
        lower_bound = self.lower_bound.value()
        upper_bound = self.upper_bound.value()
        try:
            (columns, users) = self.db.users(
                username, lower_bound, upper_bound
            )
        except Exception as e:
            self.error_label.setText(str(e))
        else:
            self.table.setModel(TableModel(columns, users))
            self.error_label.setText("Запрос выполнен успешно")


class SortableTable(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.setSortingEnabled(True)

    def setModel(self, model):
        proxy = QtCore.QSortFilterProxyModel(self)
        proxy.setSourceModel(model)
        super().setModel(proxy)


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
        try:
            return len(self._data[0])
        except IndexError:
            return 0

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]

            if orientation == Qt.Orientation.Vertical:
                return section + 1

    def cellClicked(self, row, col):
        print(row, col)
