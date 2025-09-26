from PyQt5.QtWidgets import QMainWindow, QComboBox, QLineEdit, QPushButton
from PyQt5 import uic


class Todo:
    id = 0

    def __init__(self, task: str, description: str, time):
        self.task = task
        self.description = description
        self.time = time
        Todo.id = Todo.id + 1  # increase a task existence



class TodoUi(QMainWindow):
    pass
