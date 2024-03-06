from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
import sqlite3


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi('main.ui', self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
    
    def calendarDateChanged(self):
        print("Calendar date changed!")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print(dateSelected)
        self.updateTaskList(dateSelected)
        self.saveButton.clicked.connect(self.savedChanges)
        self.addButton.clicked.connect(self.addNewTask)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        query = "SELECT Task, Completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            
            self.tasksListWidget.addItem(item)
    
    def savedChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()
        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET Completed = 'YES' WHERE Task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET Completed = 'NO' WHERE Task = ? AND date = ?"
            row = (task,date,)
            cursor.execute(query, row)
        db.commit()

        message = QMessageBox()
        message.setText("Changes Saved")
        message.setStandardButtons(QMessageBox.Ok)
        message.exec()
    
    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        newTask = str(self.lineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.lineEdit.clear()        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())