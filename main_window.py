import datetime
import sqlite3
import time
import os
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QDialog, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy)
from training_window import TrainingWindow
from profile_window import ProfileWindow


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.profile_window = None
        self.training_window = None
        self.setWindowTitle("Главное окно")
        self.setFixedSize(1000, 700)

        layout = QVBoxLayout()

        # Создаем кнопки
        buttons = ['Профиль', 'Русская раскладка', 'Английская раскладка', 'Python', 'SQL']

        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedWidth(self.width() // 3)
            button.setFixedHeight(
                self.height() * 2 // 14)  # Устанавливаем ширину кнопки равной двум третям ширины окна

            if button_text == 'Профиль':
                button.clicked.connect(
                    self.open_profile_window)  # При нажатии на кнопку "Профиль", вызываем функцию open_profile_window

            else:
                button.clicked.connect(self.open_training_window)

            # Создаем горизонтальный макет для каждой кнопки
            h_layout = QHBoxLayout()
            h_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding,
                                         QSizePolicy.Minimum))  # Добавляем растягиваемое пространство перед кнопкой
            h_layout.addWidget(button)  # Добавляем кнопку
            h_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding,
                                         QSizePolicy.Minimum))  # Добавляем растягиваемое пространство после кнопки

            layout.addLayout(h_layout)  # Добавляем горизонтальный макет в вертикальный макет

        self.setLayout(layout)

    def open_profile_window(self):
        with open('stamina.cfg') as f:
            lines = f.readlines()
        # Здесь вы должны получить имя текущего пользователя из базы данных или другого источника
        username = lines[0]
        self.profile_window = ProfileWindow(username,
                                            main_window=self)  # Передаем ссылку на главное окно в ProfileWindow
        self.profile_window.show()
        self.close()

    def open_training_window(self):
        # Получаем текст кнопки, которая была нажата
        button_text = self.sender().text()

        # Определяем категорию в зависимости от текста кнопки
        category_dict = {'Русская раскладка': 'ru', 'Английская раскладка': 'eng', 'Python': 'Python', 'SQL': 'SQL'}
        category = category_dict.get(button_text, None)

        self.training_window = TrainingWindow(category)
        self.training_window.show()
        self.close()
