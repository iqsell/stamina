import datetime
import sqlite3
import time
import os
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QDialog, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy)


class ProfileWindow(QWidget):
    def __init__(self, username, main_window=None):
        super(ProfileWindow, self).__init__()
        self.change_password_window = ChangePasswordWindow()
        self.username = username
        self.main_window = main_window

        self.setWindowTitle("Профиль")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Создаем кнопку для смены пароля
        change_password_button = QPushButton('Сменить пароль')
        change_password_button.clicked.connect(
            self.open_change_password_window)

        layout.addWidget(change_password_button)

        # Создаем кнопку "Назад"
        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_change_password_window(self):
        # Создаем экземпляр ChangePasswordWindow
        self.change_password_window.exec_()

    def go_back(self):
        if self.main_window is not None:
            self.main_window.show()
            self.close()


class ChangePasswordWindow(QDialog):
    def __init__(self):
        super(ChangePasswordWindow, self).__init__()
        self.setWindowTitle("Смена пароля")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Создание полей ввода для текущего и нового пароля
        self.currentpassword = QLineEdit()
        self.currentpassword.setEchoMode(QLineEdit.Password)
        self.currentpassword.setPlaceholderText('Текущий пароль')

        self.newpassword = QLineEdit()
        self.newpassword.setEchoMode(QLineEdit.Password)
        self.newpassword.setPlaceholderText('Новый пароль')

        # Создание кнопки обновления пароля
        updatebutton = QPushButton('Обновить')
        updatebutton.clicked.connect(self.updatepassword)

        # Добавление полей ввода и кнопки на форму
        layout.addWidget(self.currentpassword)
        layout.addWidget(self.newpassword)
        layout.addWidget(updatebutton)

        self.setLayout(layout)

        # Подключение к базе данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('users.db')
        if not self.db.open():
            QMessageBox.critical(None, 'Ошибка',
                                 'Невозможно открыть базу данных: {}'.format(self.db.lastError().text()))

    def updatepassword(self):
        # Проверка подключения к базе данных
        if not self.db.isOpen():
            QMessageBox.critical(None, 'Ошибка', 'Нет подключения к базе данных')
            return

        query = QSqlQuery()
        # Чтение конфигурации из файла
        config_username, config_password = self.read_config()

        # Подготовка запроса для получения текущего пароля пользователя
        query.prepare("SELECT password FROM users WHERE name = ?")
        query.addBindValue(config_username)
        if not query.exec():
            QMessageBox.critical(None, 'Ошибка', 'Ошибка при выполнении запроса: {}'.format(query.lastError().text()))
            return

        # Если текущий пароль совпадает, обновляем пароль
        if query.next() and query.value(0) == self.currentpassword.text():
            self.update_user_password(config_username)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный текущий пароль')

    @staticmethod
    def read_config():
        # Функция для чтения конфигурации из файла
        with open('stamina.cfg', 'r') as file:
            config_username = file.readline().strip()
            config_password = file.readline().strip()
        return config_username, config_password

    def update_user_password(self, config_username):
        # Функция для обновления пароля пользователя в базе данных
        new_query = QSqlQuery()
        new_query.prepare("UPDATE users SET password = ? WHERE name = ?")
        new_query.addBindValue(self.newpassword.text())
        new_query.addBindValue(config_username)
        if not new_query.exec():
            QMessageBox.critical(None, 'Ошибка',
                                 'Ошибка при обновлении пароля: {}'.format(new_query.lastError().text()))
        else:
            # Обновление конфигурации в файле
            self.update_config(config_username)
            QMessageBox.information(self, 'Успех', 'Пароль успешно изменен!')

    def update_config(self, config_username):
        # Функция для обновления конфигурации в файле
        new_password = self.newpassword.text()
        file_content = f"{config_username}\n{new_password}"
        with open('stamina.cfg', 'w') as file:
            file.write(file_content)

    def closeEvent(self, event):
        # Закрытие подключения к базе данных при закрытии окна
        self.db.close()
