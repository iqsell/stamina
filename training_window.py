import datetime
import sqlite3
import time
import os
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDialog, \
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy

class TrainingWindow(QMainWindow):
    def __init__(self, category=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.category = category  # Сохраняем выбранную категорию
        self.timer = QTimer()  # Создаем объект QTimer
        self.timer.timeout.connect(self.update_timer)  # Подключаем сигнал timeout к слоту self.update_timer
        self.elapsed_time = 0  # Инициализируем переменную для отслеживания прошедшего времени
        self.ui.pushButton_esc.installEventFilter(self)
        # Создаем виджет QLineEdit
        self.ui.lineEdit = QLineEdit(self)
        self.total_characters = 0  # общее количество набранных символов
        self.total_symbols = 0
        self.total_time_seconds = 0  # общее количество времени в секундах
        self.start_time = 0  # время начала ввода
        # Задаем размер и положение виджета
        self.ui.lineEdit.setGeometry(340, 200, 400, 40)  # Параметры: x, y, width, height
        self.ui.lineEdit.textChanged.connect(self.check_input)
        self.ui.pushButton_back.clicked.connect(self.returntowindow)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.key_button_map = {
            Qt.Key_0: self.ui.pushButton_48,
            Qt.Key_1: self.ui.pushButton_49,
            Qt.Key_2: self.ui.pushButton_50,
            Qt.Key_3: self.ui.pushButton_51,
            Qt.Key_4: self.ui.pushButton_52,
            Qt.Key_5: self.ui.pushButton_53,
            Qt.Key_6: self.ui.pushButton_54,
            Qt.Key_7: self.ui.pushButton_55,
            Qt.Key_8: self.ui.pushButton_56,
            Qt.Key_9: self.ui.pushButton_57,
            Qt.Key_A: self.ui.pushButton_65,
            Qt.Key_B: self.ui.pushButton_66,
            Qt.Key_C: self.ui.pushButton_67,
            Qt.Key_D: self.ui.pushButton_68,
            Qt.Key_E: self.ui.pushButton_69,
            Qt.Key_F: self.ui.pushButton_70,
            Qt.Key_G: self.ui.pushButton_71,
            Qt.Key_H: self.ui.pushButton_72,
            Qt.Key_I: self.ui.pushButton_73,
            Qt.Key_J: self.ui.pushButton_74,
            Qt.Key_K: self.ui.pushButton_75,
            Qt.Key_L: self.ui.pushButton_76,
            Qt.Key_M: self.ui.pushButton_77,
            Qt.Key_N: self.ui.pushButton_78,
            Qt.Key_O: self.ui.pushButton_79,
            Qt.Key_P: self.ui.pushButton_80,
            Qt.Key_Q: self.ui.pushButton_81,
            Qt.Key_R: self.ui.pushButton_82,
            Qt.Key_S: self.ui.pushButton_83,
            Qt.Key_T: self.ui.pushButton_84,
            Qt.Key_U: self.ui.pushButton_85,
            Qt.Key_V: self.ui.pushButton_86,
            Qt.Key_W: self.ui.pushButton_87,
            Qt.Key_X: self.ui.pushButton_88,
            Qt.Key_Y: self.ui.pushButton_89,
            Qt.Key_Z: self.ui.pushButton_90,
            Qt.Key_Comma: self.ui.pushButton_44,
            Qt.Key_Period: self.ui.pushButton_46,
            Qt.Key_Semicolon: self.ui.pushButton_59,
            Qt.Key_Apostrophe: self.ui.pushButton_39,
            Qt.Key_Slash: self.ui.pushButton_47,
            Qt.Key_Space: self.ui.pushButton_32,
            Qt.Key_Alt: self.ui.pushButton_alt,
            Qt.Key_Minus: self.ui.pushButton_minus,
            Qt.Key_F1: self.ui.pushButton_f1,
            Qt.Key_F2: self.ui.pushButton_f2,
            Qt.Key_F3: self.ui.pushButton_f3,
            Qt.Key_F4: self.ui.pushButton_f4,
            Qt.Key_F5: self.ui.pushButton_f5,
            Qt.Key_F6: self.ui.pushButton_f6,
            Qt.Key_F7: self.ui.pushButton_f7,
            Qt.Key_F8: self.ui.pushButton_f8,
            Qt.Key_F9: self.ui.pushButton_f9,
            Qt.Key_F10: self.ui.pushButton_f10,
            Qt.Key_F11: self.ui.pushButton_f11,
            Qt.Key_F12: self.ui.pushButton_f12,
            Qt.Key_Escape: self.ui.pushButton_esc,
            Qt.Key_Equal: self.ui.pushButton_plus,

        }

    def return_to_window(self):
        from main_window import MainWindow  # Импортируйте класс MainWindow здесь, в функции
        self.main_window = MainWindow()  # Создание экземпляра класса MainWindow
        self.main_window.show()
    def keyPressEvent(self, event):
        key = event.key()
        if key in self.key_button_map:
            self.key_button_map[key].setStyleSheet("background: #999")

            # Получаем текущее слово и введенный текст
            current_word = self.ui.label.text()
            entered_text = self.ui.lineEdit.text()  # Предполагается, что у вас есть QLineEdit с именем lineEdit для ввода текста

            # Проверяем, правильно ли введена буква
            if len(entered_text) <= len(current_word) and entered_text[-1] != current_word[len(entered_text) - 1]:
                # Если введена неправильная буква, подсвечиваем ее красным
                self.key_button_map[key].setStyleSheet("background: #f00")
            elif len(entered_text) == len(current_word):
                # Если слово введено полностью и правильно, отображаем следующее слово
                self.display_random_word()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key in self.key_button_map:
            # Возвращаем обычный цвет кнопки после отпускания клавиши
            self.key_button_map[key].setStyleSheet("background: #666")

    def returntowindow(self):
        from main_window import MainWindow  # Импортируйте класс MainWindow здесь, в функции
        self.mainwindow = MainWindow()  # Создание экземпляра класса MainWindow
        self.mainwindow.show()
        self.hide()
    def start(self):
        self.ui.pushButton_start.setStyleSheet('background-color: orange')
        for i in range(3):
            self.ui.pushButton_start.setText(f'Начало через {3 - i}')
            self.repaint()
            QCoreApplication.processEvents()
            time.sleep(1)
        self.ui.pushButton_start.setStyleSheet('background-color: yellow')
        self.ui.pushButton_start.setText(f'Заново')
        self.repaint()
        self.elapsed_time = 0  # Сбрасываем счетчик времени
        self.timer.start(1000)  # Запускаем таймер
        self.display_random_word()  # Отображаем случайное слово

    def display_random_word(self):
        # Подключаемся к базе данных
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Выбираем случайное слово из базы данных в зависимости от выбранной категории
        c.execute(f"SELECT {self.category} FROM words ORDER BY RANDOM() LIMIT 1")
        word = c.fetchone()[0]

        # Отображаем слово в метке
        self.ui.label.setText(word)

        # Закрываем соединение с базой данных
        conn.close()

    # Запускаем таймер

    def update_timer(self):
        self.elapsed_time += 1  # Увеличиваем счетчик времени
        self.ui.label_record.setText(str(datetime.timedelta(seconds=self.elapsed_time)))

    def check_input(self, text):
        current_word = self.ui.label.text()

        if not self.start_time:  # Проверяем, если start_time равен None (т.е. первое слово)
            self.start_time = time.time()  # Запоминаем время начала первого слова

        # Проверяем, произошло ли удаление символов
        if len(text) < len(current_word):
            # Не выполняем сброс счетчика
            self.total_characters = len(text)
        else:
            # Обновляем общее количество набранных символов
            self.total_characters = len(text)
            self.total_symbols += self.total_characters

            elapsed_time = time.time() - self.start_time  # Вычисляем прошедшее время с начала ввода текущего слова в секундах
            elapsed_time_minutes = elapsed_time / 60  # Пересчитываем в минуты
            characters_per_minute = (self.total_characters) / elapsed_time_minutes  # Рассчитываем CPM
            self.ui.label_symb.setText(f'Всего знаков: {self.total_symbols}')
            self.ui.label_dif.setText(f'Знаков в минуту: {characters_per_minute:.2f}')

        if text == current_word:
            self.display_random_word()
            self.ui.lineEdit.clear()
            self.start_time = time.time()  # Сбрасываем starttime для отслеживания времени начала следующего слова
        elif len(text) <= len(current_word) and text != current_word[:len(text)]:
            self.ui.lineEdit.setStyleSheet("background: #f00")
        else:
            self.ui.lineEdit.setStyleSheet("background: #fff")


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'training.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1028, 600)
        MainWindow.setStyleSheet("QWidget {\n"
"    color: black;\n"
"    background-color: white;\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #666;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  #888;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_dif = QtWidgets.QLabel(self.centralwidget)
        self.label_dif.setObjectName("label_dif")
        self.label_symb = QtWidgets.QLabel(self.centralwidget)
        self.label_symb.setObjectName("label_symb")
        self.label_dif = QtWidgets.QLabel(self.centralwidget)
        self.label_dif.setObjectName("label_dif")
        self.horizontalLayout.addWidget(self.label_dif)
        self.label_dif.setObjectName("label_symb")
        self.horizontalLayout.addWidget(self.label_symb)

        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setObjectName("label_time")
        self.horizontalLayout.addWidget(self.label_time)
        self.label_record = QtWidgets.QLabel(self.centralwidget)
        self.label_record.setObjectName("label_record")
        self.horizontalLayout.addWidget(self.label_record)
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setStyleSheet("QWidget {\n"
"    color: white;\n"
"    background-color: white;\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: green;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  #888;\n"
"}")
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setStyleSheet("QWidget {\n"
"    color: black;\n"
"    background-color: white;\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: rgb(176, 176, 176) ;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:  #888;\n"
"}")
        self.pushButton_back.setObjectName("pushButton_back")
        self.horizontalLayout.addWidget(self.pushButton_back)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_78 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_78.setObjectName("pushButton_78")
        self.gridLayout.addWidget(self.pushButton_78, 4, 8, 1, 1)
        self.pushButton_74 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_74.setObjectName("pushButton_74")
        self.gridLayout.addWidget(self.pushButton_74, 3, 8, 1, 1)
        self.pushButton_75 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_75.setObjectName("pushButton_75")
        self.gridLayout.addWidget(self.pushButton_75, 3, 9, 1, 1)
        self.pushButton_77 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_77.setObjectName("pushButton_77")
        self.gridLayout.addWidget(self.pushButton_77, 4, 9, 1, 1)
        self.pushButton_57 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_57.setObjectName("pushButton_57")
        self.gridLayout.addWidget(self.pushButton_57, 1, 10, 1, 1)
        self.pushButton_44 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_44.setObjectName("pushButton_44")
        self.gridLayout.addWidget(self.pushButton_44, 4, 10, 1, 1)
        self.pushButton_76 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_76.setObjectName("pushButton_76")
        self.gridLayout.addWidget(self.pushButton_76, 3, 10, 1, 1)
        self.pushButton_59 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_59.setObjectName("pushButton_59")
        self.gridLayout.addWidget(self.pushButton_59, 3, 11, 1, 1)
        self.pushButton_46 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_46.setObjectName("pushButton_46")
        self.gridLayout.addWidget(self.pushButton_46, 4, 11, 1, 1)
        self.pushButton_48 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_48.setObjectName("pushButton_48")
        self.gridLayout.addWidget(self.pushButton_48, 1, 11, 1, 1)
        self.pushButton_47 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_47.setObjectName("pushButton_47")
        self.gridLayout.addWidget(self.pushButton_47, 4, 12, 1, 1)
        self.pushButton_39 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_39.setObjectName("pushButton_39")
        self.gridLayout.addWidget(self.pushButton_39, 3, 12, 1, 1)
        self.pushButton_minus = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_minus.setObjectName("pushButton_minus")
        self.gridLayout.addWidget(self.pushButton_minus, 1, 12, 1, 1)
        self.pushButton_68 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_68.setObjectName("pushButton_68")
        self.gridLayout.addWidget(self.pushButton_68, 3, 4, 1, 1)
        self.pushButton_kos = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_kos.setObjectName("pushButton_kos")
        self.gridLayout.addWidget(self.pushButton_kos, 2, 14, 1, 1)
        self.pushButton_plus = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_plus.setObjectName("pushButton_plus")
        self.gridLayout.addWidget(self.pushButton_plus, 1, 13, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 1, 14, 1, 1)
        self.pushButton_67 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_67.setObjectName("pushButton_67")
        self.gridLayout.addWidget(self.pushButton_67, 4, 5, 1, 1)
        self.pushButton_86 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_86.setObjectName("pushButton_86")
        self.gridLayout.addWidget(self.pushButton_86, 4, 6, 1, 1)
        self.pushButton_73 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_73.setObjectName("pushButton_73")
        self.gridLayout.addWidget(self.pushButton_73, 2, 9, 1, 1)
        self.pushButton_70 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_70.setObjectName("pushButton_70")
        self.gridLayout.addWidget(self.pushButton_70, 3, 5, 1, 1)
        self.pushButton_80 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_80.setObjectName("pushButton_80")
        self.gridLayout.addWidget(self.pushButton_80, 2, 11, 1, 1)
        self.pushButton_79 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_79.setObjectName("pushButton_79")
        self.gridLayout.addWidget(self.pushButton_79, 2, 10, 1, 1)
        self.pushButton_71 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_71.setObjectName("pushButton_71")
        self.gridLayout.addWidget(self.pushButton_71, 3, 6, 1, 1)
        self.pushButton_72 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_72.setObjectName("pushButton_72")
        self.gridLayout.addWidget(self.pushButton_72, 3, 7, 1, 1)
        self.pushButton_66 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_66.setObjectName("pushButton_66")
        self.gridLayout.addWidget(self.pushButton_66, 4, 7, 1, 1)
        self.pushButton_91 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_91.setObjectName("pushButton_91")
        self.gridLayout.addWidget(self.pushButton_91, 2, 12, 1, 1)
        self.pushButton_193 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_193.setObjectName("pushButton_193")
        self.gridLayout.addWidget(self.pushButton_193, 2, 13, 1, 1)
        self.pushButton_88 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_88.setObjectName("pushButton_88")
        self.gridLayout.addWidget(self.pushButton_88, 4, 4, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout.addWidget(self.pushButton_17, 5, 0, 1, 1)
        self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout.addWidget(self.pushButton_20, 3, 0, 1, 1)
        self.pushButton_85 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_85.setObjectName("pushButton_85")
        self.gridLayout.addWidget(self.pushButton_85, 2, 8, 1, 1)
        self.pushButton_f6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f6.setObjectName("pushButton_f6")
        self.gridLayout.addWidget(self.pushButton_f6, 0, 8, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_84 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_84.setObjectName("pushButton_84")
        self.gridLayout.addWidget(self.pushButton_84, 2, 6, 1, 1)
        self.pushButton_69 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_69.setObjectName("pushButton_69")
        self.gridLayout.addWidget(self.pushButton_69, 2, 4, 1, 1)
        self.pushButton_82 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_82.setObjectName("pushButton_82")
        self.gridLayout.addWidget(self.pushButton_82, 2, 5, 1, 1)
        self.pushButton_89 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_89.setObjectName("pushButton_89")
        self.gridLayout.addWidget(self.pushButton_89, 2, 7, 1, 1)
        self.pushButton_f11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f11.setObjectName("pushButton_f11")
        self.gridLayout.addWidget(self.pushButton_f11, 0, 13, 1, 1)
        self.pushButton_f12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f12.setObjectName("pushButton_f12")
        self.gridLayout.addWidget(self.pushButton_f12, 0, 14, 1, 1)
        self.pushButton_f8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f8.setObjectName("pushButton_f8")
        self.gridLayout.addWidget(self.pushButton_f8, 0, 10, 1, 1)
        self.pushButton_f10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f10.setObjectName("pushButton_f10")
        self.gridLayout.addWidget(self.pushButton_f10, 0, 12, 1, 1)
        self.pushButton_f9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f9.setObjectName("pushButton_f9")
        self.gridLayout.addWidget(self.pushButton_f9, 0, 11, 1, 1)
        self.pushButton_f7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f7.setObjectName("pushButton_f7")
        self.gridLayout.addWidget(self.pushButton_f7, 0, 9, 1, 1)
        self.pushButton_f2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f2.setObjectName("pushButton_f2")
        self.gridLayout.addWidget(self.pushButton_f2, 0, 4, 1, 1)
        self.pushButton_f3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f3.setObjectName("pushButton_f3")
        self.gridLayout.addWidget(self.pushButton_f3, 0, 5, 1, 1)
        self.pushButton_esc = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_esc.setObjectName("pushButton_esc")
        self.gridLayout.addWidget(self.pushButton_esc, 0, 0, 1, 1)
        self.pushButton_f5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f5.setObjectName("pushButton_f5")
        self.gridLayout.addWidget(self.pushButton_f5, 0, 7, 1, 1)
        self.pushButton_f4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f4.setObjectName("pushButton_f4")
        self.gridLayout.addWidget(self.pushButton_f4, 0, 6, 1, 1)
        self.pushButton_192 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_192.setObjectName("pushButton_192")
        self.gridLayout.addWidget(self.pushButton_192, 1, 0, 1, 1)
        self.pushButton_53 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_53.setObjectName("pushButton_53")
        self.gridLayout.addWidget(self.pushButton_53, 1, 6, 1, 1)
        self.pushButton_52 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_52.setObjectName("pushButton_52")
        self.gridLayout.addWidget(self.pushButton_52, 1, 5, 1, 1)
        self.pushButton_51 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_51.setObjectName("pushButton_51")
        self.gridLayout.addWidget(self.pushButton_51, 1, 4, 1, 1)
        self.pushButton_56 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_56.setObjectName("pushButton_56")
        self.gridLayout.addWidget(self.pushButton_56, 1, 9, 1, 1)
        self.pushButton_55 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_55.setObjectName("pushButton_55")
        self.gridLayout.addWidget(self.pushButton_55, 1, 8, 1, 1)
        self.pushButton_54 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_54.setObjectName("pushButton_54")
        self.gridLayout.addWidget(self.pushButton_54, 1, 7, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_16.setStyleSheet("")
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout.addWidget(self.pushButton_16, 4, 0, 1, 2)
        self.pushButton_65 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_65.setObjectName("pushButton_65")
        self.gridLayout.addWidget(self.pushButton_65, 3, 1, 1, 1)
        self.pushButton_windows = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_windows.setObjectName("pushButton_windows")
        self.gridLayout.addWidget(self.pushButton_windows, 5, 1, 1, 1)
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout.addWidget(self.pushButton_18, 5, 2, 1, 1)
        self.pushButton_90 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_90.setObjectName("pushButton_90")
        self.gridLayout.addWidget(self.pushButton_90, 4, 2, 1, 1)
        self.pushButton_83 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_83.setObjectName("pushButton_83")
        self.gridLayout.addWidget(self.pushButton_83, 3, 2, 1, 1)
        self.pushButton_81 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_81.setObjectName("pushButton_81")
        self.gridLayout.addWidget(self.pushButton_81, 2, 1, 1, 1)
        self.pushButton_49 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_49.setObjectName("pushButton_49")
        self.gridLayout.addWidget(self.pushButton_49, 1, 1, 1, 1)
        self.pushButton_f1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_f1.setObjectName("pushButton_f1")
        self.gridLayout.addWidget(self.pushButton_f1, 0, 2, 1, 1)
        self.pushButton_50 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_50.setObjectName("pushButton_50")
        self.gridLayout.addWidget(self.pushButton_50, 1, 2, 1, 1)
        self.pushButton_87 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_87.setObjectName("pushButton_87")
        self.gridLayout.addWidget(self.pushButton_87, 2, 2, 1, 1)
        self.pushButton_enter = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.gridLayout.addWidget(self.pushButton_enter, 3, 13, 1, 2)
        self.pushButton_shift_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_shift_2.setObjectName("pushButton_shift_2")
        self.gridLayout.addWidget(self.pushButton_shift_2, 4, 13, 1, 2)
        self.pushButton_ctrl_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ctrl_2.setObjectName("pushButton_ctrl_2")
        self.gridLayout.addWidget(self.pushButton_ctrl_2, 5, 14, 1, 1)
        self.pushButton_dop_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_dop_2.setObjectName("pushButton_dop_2")
        self.gridLayout.addWidget(self.pushButton_dop_2, 5, 13, 1, 1)
        self.pushButton_dop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_dop.setObjectName("pushButton_dop")
        self.gridLayout.addWidget(self.pushButton_dop, 5, 12, 1, 1)
        self.pushButton_alt = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_alt.setObjectName("pushButton_alt")
        self.gridLayout.addWidget(self.pushButton_alt, 5, 11, 1, 1)
        self.pushButton_32 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_32.setObjectName("pushButton_32")
        self.gridLayout.addWidget(self.pushButton_32, 5, 4, 1, 7)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label_record.setText(_translate("MainWindow", "Время: "))

        self.pushButton_start.setText(_translate("MainWindow", "Старт"))
        self.pushButton_back.setText(_translate("MainWindow", "Вернуться"))
        self.label.setText(_translate('MainWindow', ''))
        self.label.setText(_translate("MainWindow", "Тут будет текст"))
        self.pushButton_78.setText(_translate("MainWindow", "Т"))
        self.pushButton_74.setText(_translate("MainWindow", "О"))
        self.pushButton_75.setText(_translate("MainWindow", "Л"))
        self.pushButton_77.setText(_translate("MainWindow", "Ь"))
        self.pushButton_57.setText(_translate("MainWindow", "9"))
        self.pushButton_44.setText(_translate("MainWindow", "Б"))
        self.pushButton_76.setText(_translate("MainWindow", "Д"))
        self.pushButton_59.setText(_translate("MainWindow", "Ж"))
        self.pushButton_46.setText(_translate("MainWindow", "Ю"))
        self.pushButton_48.setText(_translate("MainWindow", "0"))
        self.pushButton_47.setText(_translate("MainWindow", "."))
        self.pushButton_39.setText(_translate("MainWindow", "Э"))
        self.pushButton_minus.setText(_translate("MainWindow", "-"))
        self.pushButton_68.setText(_translate("MainWindow", "В"))
        self.pushButton_kos.setText(_translate("MainWindow", "\\"))
        self.pushButton_plus.setText(_translate("MainWindow", "+"))
        self.pushButton_8.setText(_translate("MainWindow", "<-"))
        self.pushButton_67.setText(_translate("MainWindow", "С"))
        self.pushButton_86.setText(_translate("MainWindow", "М"))
        self.pushButton_73.setText(_translate("MainWindow", "Ш"))
        self.pushButton_70.setText(_translate("MainWindow", "А"))
        self.pushButton_80.setText(_translate("MainWindow", "З"))
        self.pushButton_79.setText(_translate("MainWindow", "Щ"))
        self.pushButton_71.setText(_translate("MainWindow", "П"))
        self.pushButton_72.setText(_translate("MainWindow", "Р"))
        self.pushButton_66.setText(_translate("MainWindow", "И"))
        self.pushButton_91.setText(_translate("MainWindow", "Х"))
        self.pushButton_193.setText(_translate("MainWindow", "Ъ"))
        self.pushButton_88.setText(_translate("MainWindow", "Ч"))
        self.pushButton_17.setText(_translate("MainWindow", "CTRL"))
        self.pushButton_20.setText(_translate("MainWindow", "CAPS"))
        self.pushButton_85.setText(_translate("MainWindow", "Г"))
        self.pushButton_f6.setText(_translate("MainWindow", "F6"))
        self.pushButton.setText(_translate("MainWindow", "TAB"))
        self.pushButton_84.setText(_translate("MainWindow", "Е"))
        self.pushButton_69.setText(_translate("MainWindow", "У"))
        self.pushButton_82.setText(_translate("MainWindow", "К"))
        self.pushButton_89.setText(_translate("MainWindow", "Н"))
        self.pushButton_f11.setText(_translate("MainWindow", "F11"))
        self.pushButton_f12.setText(_translate("MainWindow", "F12"))
        self.pushButton_f8.setText(_translate("MainWindow", "F8"))
        self.pushButton_f10.setText(_translate("MainWindow", "F10"))
        self.pushButton_f9.setText(_translate("MainWindow", "F9"))
        self.pushButton_f7.setText(_translate("MainWindow", "F7"))
        self.pushButton_f2.setText(_translate("MainWindow", "F2"))
        self.pushButton_f3.setText(_translate("MainWindow", "F3"))
        self.pushButton_esc.setText(_translate("MainWindow", "ESC"))
        self.pushButton_f5.setText(_translate("MainWindow", "F5"))
        self.pushButton_f4.setText(_translate("MainWindow", "F4"))
        self.pushButton_192.setText(_translate("MainWindow", "Ё"))
        self.pushButton_53.setText(_translate("MainWindow", "5"))
        self.pushButton_52.setText(_translate("MainWindow", "4"))
        self.pushButton_51.setText(_translate("MainWindow", "3"))
        self.pushButton_56.setText(_translate("MainWindow", "8"))
        self.pushButton_55.setText(_translate("MainWindow", "7"))
        self.pushButton_54.setText(_translate("MainWindow", "6"))
        self.pushButton_16.setText(_translate("MainWindow", "SHIFT"))
        self.pushButton_65.setText(_translate("MainWindow", "Ф"))
        self.pushButton_windows.setText(_translate("MainWindow", "WINDOWS"))
        self.pushButton_18.setText(_translate("MainWindow", "ALT"))
        self.pushButton_90.setText(_translate("MainWindow", "Я"))
        self.pushButton_83.setText(_translate("MainWindow", "Ы"))
        self.pushButton_81.setText(_translate("MainWindow", "Й"))
        self.pushButton_49.setText(_translate("MainWindow", "1"))
        self.pushButton_f1.setText(_translate("MainWindow", "F1"))
        self.pushButton_50.setText(_translate("MainWindow", "2"))
        self.pushButton_87.setText(_translate("MainWindow", "Ц"))
        self.pushButton_enter.setText(_translate("MainWindow", "ENTER"))
        self.pushButton_shift_2.setText(_translate("MainWindow", "SHIFT"))
        self.pushButton_ctrl_2.setText(_translate("MainWindow", "CTRL"))
        self.pushButton_dop_2.setText(_translate("MainWindow", "1"))
        self.pushButton_dop.setText(_translate("MainWindow", "2"))
        self.pushButton_alt.setText(_translate("MainWindow", "ALT"))
        self.pushButton_32.setText(_translate("MainWindow", "SPACE"))
