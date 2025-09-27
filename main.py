import mysql.connector
from mysql.connector import errorcode

from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QLineEdit, QPushButton, QApplication, QLabel, QTableWidgetItem, \
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
import sys


# import sqlite3

class Todo:
    """ Todo Model Class """

    def __init__(self, task_id: int, task_name: str, duration: str, deadline: str):
        self.id = task_id  # each task with a unique id
        self.task_name = task_name
        self.duration = duration
        self.deadline = deadline


class TodoUi(QMainWindow):
    """ interface of to do app class"""

    def __init__(self):
        super(TodoUi, self).__init__()
        self.tasks = []
        self.next_id = 1
        self.initUi()
        self.connect_signals()
        self.connect_db()
        # self.load_from_db()

    def initUi(self):
        # load ui and define widgets
        uic.loadUi('todo.ui', self)
        self.subjectEditor = self.findChild(QLineEdit, "subjectEditor")
        self.durationEditor = self.findChild(QLineEdit, "durationEditor")
        self.deadlineEditor = self.findChild(QLineEdit, "deadlineEditor")
        # buttons
        self.addTask = self.findChild(QPushButton, "addTaskButton")
        self.deleteTask = self.findChild(QPushButton, "deleteTaskButton")
        self.clear = self.findChild(QPushButton, "clearTasksButton")
        self.save = self.findChild(QPushButton, "saveToDBButton")

        # table
        self.taskTable = self.findChild(QTableWidget, "taskTable")
        self.taskTable.setColumnWidth(0, 250)
        self.taskTable.setColumnWidth(1, 200)
        self.taskTable.setColumnWidth(2, 288)
        self.taskTable.setHorizontalHeaderLabels(["Task", "Duration", "Deadline"])

        # label of tasks count
        self.taskCountLabel = self.findChild(QLabel, "taskCountLabel")

    def connect_signals(self):
        """ connect button signals to functions"""
        self.addTask.clicked.connect(self.add_task)
        self.deleteTask.clicked.connect(self.delete)
        self.clear.clicked.connect(self.clear_table)

    def delete(self):
        current_row = self.taskTable.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning', 'Please select a task to delete')

        button = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure that you want to delete the selected task?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            # Get task name (or use ID if stored)
            task_name = self.taskTable.item(current_row, 0).text()

            # Remove row from table
            self.taskTable.removeRow(current_row)

            # Remove matching object from list
            self.tasks = [t for t in self.tasks if t.task_name != task_name]

            # Reassign IDs
            for idx, task in enumerate(self.tasks, start=1):
                task.id = idx
            self.next_id = len(self.tasks) + 1

            # Update label
            self.update_task_count()
            for task in self.tasks:
                print(task.task_name)

    def clear_table(self):
        if self.taskTable.rowCount() == 0:
            return QMessageBox.warning(
                self,
                'Warning',
                'No tasks to be cleared!!')
        # Clear the table widget
        self.taskTable.setRowCount(0)

        # Clear the task objects
        self.tasks.clear()

        # Reset the counter
        self.next_id = 1

        # Update label
        self.update_task_count()

    def display_table(self):
        """ display table """
        for row in range(self.taskTable.rowCount()):
            for col in range(self.taskTable.columnCount()):
                item = self.taskTable.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

    def add_task(self):
        """ add a single task to task table"""
        task = self.subjectEditor.text()
        duration = self.durationEditor.text()
        deadline = self.deadlineEditor.text()

        if not deadline or not duration or not task:
            return QMessageBox.warning(self, 'Warning',
                                       'Please add task name or duration or deadline. can\'t be empty!!')
        # print(task, duration, deadline)
        # add to table
        todo_task = Todo(self.next_id, task, duration, deadline)
        self.tasks.append(todo_task)
        self.taskTable.insertRow(0)
        self.taskTable.setItem(0, 0, QTableWidgetItem(todo_task.task_name))
        self.taskTable.setItem(0, 1, QTableWidgetItem(todo_task.duration))
        self.taskTable.setItem(0, 2, QTableWidgetItem(todo_task.deadline))
        self.next_id += 1
        self.subjectEditor.clear()
        self.durationEditor.clear()
        self.deadlineEditor.clear()
        self.display_table()
        self.update_task_count()

    def update_task_count(self):
        """Updates the task count label."""

        self.taskCountLabel.setText(f"Total Tasks: {len(self.tasks)}")

    #  database stuff
    def connect_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='ali@22',
                database='test_project_db'
            )
            QTimer.singleShot(1500, lambda: (
                QMessageBox.information(self, "Confirmation", "Database Connected")

            ))

            self.cursor = self.connection.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT PRIMARY KEY,
                    task_name VARCHAR(255),
                    duration VARCHAR(100),
                    deadline VARCHAR(100)
                )
            """)
            self.connection.commit()

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "DB Error", "Invalid username or password")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "DB Error", "Database does not exist")
            else:
                QMessageBox.critical(self, "DB Error", str(error))

    def load_from_db(self):
        pass

    def save_to_db(self):
        pass


app = QApplication(sys.argv)
Todo_UI = TodoUi()
Todo_UI.show()
sys.exit(app.exec_())
