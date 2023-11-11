
from main_window import MainWindow
from training_window import TrainingWindow
import datetime
import sqlite3
import time
import os

from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDialog, \
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy

from profile_window import ProfileWindow
class LoginWindow(QDialog):
    def __init__(self, reg_window=None):
        super(LoginWindow, self).__init__()

        self.reg_window = reg_window

        self.setWindowTitle("Вход")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        label = QLabel('Вход')
        self.username = QLineEdit()
        self.username.setPlaceholderText('Имя')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')
        button = QPushButton('Войти')
        button.clicked.connect(self.login)

        back_button = QPushButton('Назад')  # Создаем кнопку "Назад"
        back_button.clicked.connect(self.go_back)  # При нажатии на кнопку "Назад", вызываем функцию go_back

        layout.addWidget(label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addWidget(back_button)  # Добавляем кнопку "Назад" в макет

        self.setLayout(layout)

    def login(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')
        username = self.username.text()
        password = self.password.text()

        if db.open():
            query = QSqlQuery()
            query.prepare("SELECT * FROM users WHERE name = ? AND password = ?")
            query.addBindValue(self.username.text())
            query.addBindValue(self.password.text())
            query.exec_()
            with open("stamina.cfg", "w") as file:
                file.write("")
                file.write(f"{username}\n")
                file.write(f"{password}\n")
            if query.next():
                QMessageBox.information(self, 'Успех',
                                        'Вы успешно вошли в систему!')  # Выводим сообщение об успешной авторизации
                self.main_window = MainWindow()
                self.main_window.show()
                global current_user
                current_user = self.username.text()
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверное имя пользователя или пароль')

            db.close()

    def go_back(self):
        if self.reg_window is not None:
            self.reg_window.show()  # Показываем окно Reg_Window
            self.close()  # Закрываем текущее окно


class RegisterWindow(QDialog):
    def __init__(self, reg_window=None):
        super(RegisterWindow, self).__init__()

        self.reg_window = reg_window
        self.LoginWindow = LoginWindow()
        self.setWindowTitle("Регистрация")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        label = QLabel('Регистрация')
        self.username = QLineEdit()
        self.username.setPlaceholderText('Имя')
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')
        button = QPushButton('Создать аккаунт')
        button.clicked.connect(self.register)

        back_button = QPushButton('Назад')  # Создаем кнопку "Назад"
        back_button.clicked.connect(self.go_back)  # При нажатии на кнопку "Назад", вызываем функцию go_back

        layout.addWidget(label)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(button)
        layout.addWidget(back_button)  # Добавляем кнопку "Назад" в макет

        self.setLayout(layout)

    def register(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if not db.open():
            QMessageBox.critical(self, 'Ошибка', 'Невозможно открыть базу данных: {}'.format(db.lastError().text()))
            return

        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, registration_date TEXT)")

        query.prepare("SELECT * FROM users WHERE name = ?")
        query.addBindValue(self.username.text())
        if not query.exec_():
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при выполнении запроса: {}'.format(query.lastError().text()))
            db.close()
            return

        if query.next():
            QMessageBox.warning(self, 'Ошибка', 'Данное имя уже используется, введите другое')
        else:
            query.prepare("INSERT INTO users (name, password, registration_date) VALUES (?, ?, ?)")
            query.addBindValue(self.username.text())
            query.addBindValue(self.password.text())
            query.addBindValue(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if not query.exec_():
                QMessageBox.critical(self, 'Ошибка',
                                     'Ошибка при выполнении запроса: {}'.format(query.lastError().text()))
            else:
                QMessageBox.information(self, 'Успешная регистрация', 'Аккаунт успешно создан')
                if self.LoginWindow is not None:
                    self.LoginWindow.show()
                    self.close()

    def go_back(self):
        if self.reg_window is not None:
            self.reg_window.show()  # Показываем окно Reg_Window
            self.close()  # Закрываем текущее окно


class Reg_Window(QWidget):
    def __init__(self):
        super(Reg_Window, self).__init__()

        self.setWindowTitle("Окно регистрации")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        button1 = QPushButton('Вход')
        button1.clicked.connect(self.open_login_window)

        button2 = QPushButton('Регистрация')
        button2.clicked.connect(self.open_register_window)

        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)

    def open_login_window(self):
        # Создаем экземпляр LoginWindow и передаем ссылку на текущий объект (self)
        # Это позволит нам вызвать метод show() этого объекта из LoginWindow
        self.login_window = LoginWindow(reg_window=self)
        self.login_window.show()
        self.close()

    def open_register_window(self):
        # Создаем экземпляр RegisterWindow и передаем ссылку на текущий объект (self)
        # Это позволит нам вызвать метод show() этого объекта из RegisterWindow
        self.register_window = RegisterWindow(reg_window=self)
        self.register_window.show()
        self.close()







app = QApplication([])
if os.path.exists("stamina.cfg"):
    with open("stamina.cfg", "r") as file:
        lines = file.read().split('\n')
        if len(lines) >= 2:
            username = lines[0]
            password = lines[1]
            if LoginWindow.login:
                window = MainWindow()
            else:
                with open("stamina.cfg", "w") as file:
                    file.write("")
        else:
            with open("stamina.cfg", "w") as file:
                file.write("")
            window = Reg_Window()
else:
    with open("stamina.cfg", "w") as file:
        file.write("")
    window = Reg_Window()
window.show()
app.exec_()