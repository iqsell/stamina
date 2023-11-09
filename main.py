import datetime
import sqlite3
import time

from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDialog, \
    QLineEdit, QMessageBox, QSpacerItem, QSizePolicy

from training import Ui_MainWindow


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

        if db.open():
            query = QSqlQuery()
            query.prepare("SELECT * FROM users WHERE name = ? AND password = ?")
            query.addBindValue(self.username.text())
            query.addBindValue(self.password.text())
            query.exec_()

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

        if db.open():
            query = QSqlQuery()
            query.exec_("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT, registration_date TEXT)")
            query.prepare("SELECT * FROM users WHERE name = ?")
            query.addBindValue(self.username.text())
            query.exec_()

            if query.next():
                QMessageBox.warning(self, 'Ошибка', 'Данное имя уже используется, введите другое')
            else:
                query.prepare("INSERT INTO users (name, password, registration_date) VALUES (?, ?, ?)")
                query.addBindValue(self.username.text())
                query.addBindValue(self.password.text())
                query.addBindValue(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                query.exec_()
                self.close()

            db.close()

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


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Главное окно")
        self.setFixedSize(1000, 700)

        layout = QVBoxLayout()

        # Создаем кнопки
        buttons = ['Профиль', 'Русская раскладка', 'Английская раскладка', 'Python', 'SQL']

        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedWidth(self.width() // 3)
            button.setFixedHeight(self.height() * 2 // 14)  # Устанавливаем ширину кнопки равной двум третям ширины окна

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
        # Здесь вы должны получить имя текущего пользователя из базы данных или другого источника
        username = current_user
        self.profile_window = ProfileWindow(username,
                                            main_window=self)  # Передаем ссылку на главное окно в ProfileWindow
        self.profile_window.show()
        self.close()

    def open_training_window(self):
        # Получаем текст кнопки, которая была нажата
        button_text = self.sender().text()

        # Определяем категорию в зависимости от текста кнопки
        if button_text == 'Русская раскладка':
            category = 'ru'
        elif button_text == 'Английская раскладка':
            category = 'eng'
        else:
            category = None

        self.training_window = TrainingWindow(category)
        self.training_window.show()
        self.close()


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
            self.open_change_password_window)  # При нажатии на кнопку "Сменить пароль", вызываем функцию open_change_password_window

        layout.addWidget(change_password_button)

        # Создаем кнопку "Назад"
        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)  # При нажатии на кнопку "Назад", вызываем функцию go_back

        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_change_password_window(self):
        # Создаем экземпляр ChangePasswordWindow и показываем его
        self.change_password_window = ChangePasswordWindow(self.username)
        self.change_password_window.show()

    def go_back(self):
        if self.main_window is not None:
            self.main_window.show()  # Показываем главное окно
            self.close()  # Закрываем текущее окно


class ChangePasswordWindow(QWidget):
    def __init__(self, username):
        super(ChangePasswordWindow, self).__init__()

        self.username = username

        self.setWindowTitle("Смена пароля")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        # Создаем поля для ввода текущего и нового пароля
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.Password)
        self.current_password.setPlaceholderText('Текущий пароль')

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText('Новый пароль')

        # Создаем кнопку для обновления пароля
        update_button = QPushButton('Обновить')
        update_button.clicked.connect(
            self.update_password)  # При нажатии на кнопку "Обновить", вызываем функцию update_password

        layout.addWidget(self.current_password)
        layout.addWidget(self.new_password)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def update_password(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('users.db')

        if db.open():
            query = QSqlQuery()
            query.prepare("SELECT password FROM users WHERE name = ?")
            query.addBindValue(self.username)
            query.exec_()

            if query.next() and query.value(0) == self.current_password.text():
                # Если текущий пароль верный, обновляем пароль в базе данных
                query.prepare("UPDATE users SET password = ? WHERE name = ?")
                query.addBindValue(self.new_password.text())
                query.addBindValue(self.username)
                query.exec_()

                QMessageBox.information(self, 'Успех', 'Пароль успешно изменен!')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный текущий пароль')

            db.close()


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
        self.mainwindow = MainWindow()
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
        self.ui.label_time.setText(str(datetime.timedelta(seconds=self.elapsed_time)))

    def check_input(self, text):
        # Получаем текущее слово
        current_word = self.ui.label.text()

        # Проверяем, правильно ли введено слово
        if text == current_word:
            # Если слово введено правильно, отображаем следующее слово и очищаем поле ввода
            self.display_random_word()
            self.ui.lineEdit.clear()
        elif len(text) <= len(current_word) and text != current_word[:len(text)]:
            # Если введена неправильная буква, подсвечиваем поле ввода красным
            self.ui.lineEdit.setStyleSheet("background: #f00")
        else:
            # Если все буквы введены правильно, возвращаем обычный цвет поля ввода
            self.ui.lineEdit.setStyleSheet("background: #fff")


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
