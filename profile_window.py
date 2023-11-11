import datetime
import sqlite3
import time
import os
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDialog, \
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy

class ProfileWindow(QWidget):
    def __init__(self, username, main_window=None):
        super(ProfileWindow, self).__init__()
        self.username = username
        self.main_window = main_window

        self.setWindowTitle("Профиль")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Получаем данные пользователя из базы данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if db.open():
            query = QSqlQuery()
            query.prepare("SELECT name, registration_date FROM users WHERE name = ?")
            query.addBindValue(self.username)
            query.exec_()

            if query.next():
                name = query.value(0)
                registration_date = query.value(1)

                # Создаем метки для отображения имени пользователя и даты регистрации
                name_label = QLabel('Ваше имя: ' + name)
                date_label = QLabel('Дата регистрации: ' + registration_date)

                layout.addWidget(name_label)
                layout.addWidget(date_label)

            db.close()

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
        self.change_password_window = ChangePasswordWindow()
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

        self.currentpassword = QLineEdit()
        self.currentpassword.setEchoMode(QLineEdit.Password)
        self.currentpassword.setPlaceholderText('Текущий пароль')

        self.newpassword = QLineEdit()
        self.newpassword.setEchoMode(QLineEdit.Password)
        self.newpassword.setPlaceholderText('Новый пароль')

        updatebutton = QPushButton('Обновить')
        updatebutton.clicked.connect(self.updatepassword)

        layout.addWidget(self.currentpassword)
        layout.addWidget(self.newpassword)
        layout.addWidget(updatebutton)

        self.setLayout(layout)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('users.db')
        if not self.db.open():
            QMessageBox.critical(None, 'Ошибка', 'Невозможно открыть базу данных: {}'.format(self.db.lastError().text()))

    def updatepassword(self):
        if not self.db.isOpen():
            QMessageBox.critical(None, 'Ошибка', 'Нет подключения к базе данных')
            return

        query = QSqlQuery()
        with open('stamina.cfg', 'r') as file:
            config_username = file.readline().strip()
            config_password = file.readline().strip()

        query.prepare("SELECT password FROM users WHERE name = ?")
        query.addBindValue(config_username)
        if not query.exec():
            QMessageBox.critical(None, 'Ошибка', 'Ошибка при выполнении запроса: {}'.format(query.lastError().text()))
            return

        if query.next() and query.value(0) == config_password:
            if query.value(0) == config_password:
                new_query = QSqlQuery()
                new_query.prepare("UPDATE users SET password = ? WHERE name = ?")
                new_query.addBindValue(self.newpassword.text())
                new_query.addBindValue(config_username)
                if not new_query.exec():
                    QMessageBox.critical(None, 'Ошибка',
                                         'Ошибка при обновлении пароля: {}'.format(new_query.lastError().text()))
                else:
                    new_password = self.newpassword.text()
                    file_content = f"{config_username}\n{new_password}"
                    with open('stamina.cfg', 'w') as file:
                        file.write(file_content)
                    QMessageBox.information(self, 'Успех', 'Пароль успешно изменен!')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный текущий пароль')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный текущий пароль')

    def closeEvent(self, event):
        self.db.close()