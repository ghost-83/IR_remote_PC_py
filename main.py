#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, threading,serial,pyautogui, subprocess
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QIcon

signal_ui = False # Создаем глобальную перененную для завершение цикла в порлельном потоке

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        global qbtn, qbtn_Stop, qlbl, thre # Создаем глобальные переменные для доступа к ним из любой функции класса
        self.initUI()

    def initUI(self):
        self.move(300, 300)# Задаем отступы от краев экрана
        self.setFixedSize(200, 70)# Задаем статический не изменяемый размер окна
        self.setWindowTitle('ИК пульт')# Пишем имя окна
        self.setWindowIcon(QIcon('MyIcon.ico'))# Зодаем эконку окна
        self.qbtn = QPushButton('Старт', self)# Создаем кнопку Старт
        self.qbtn.move(10, 20)# Задаем отступы от края окна
        self.qbtn_Stop = QPushButton('Стоп', self)
        self.qbtn_Stop.move(110, 20)
        self.qbtn_Stop.setEnabled(False)# Делае кнопку Стоп не активной
        self.qlbl = QLabel('Готов', self)# Создаем этикетку
        self.qlbl.move(10, 50)# Задаем положение этикетки в окне
        self.qlbl.resize(180, 20)# Задарем размер этикетки

        self.qbtn.clicked.connect(self.buttonClicked)# Связываем кнопки с функциями
        self.qbtn_Stop.clicked.connect(self.buttonOnClicked)# при нажатии на кнопку будет вызвана заданная функция
        self.show()# Отображаем окно

    def buttonClicked(self):
        global signal_ui# Сообщаем что данная переменная к которой мы будем обращаться глобальная
        signal_ui = True# Меняем значение глобальной переменной
        self.qbtn.setEnabled(False)# Делаем кнопку Старт не активной,
        self.qbtn_Stop.setEnabled(True)# а кнотку стоп активной
        self.thre = threading.Thread(target=self.PriemChikl, name=self.PriemChikl)# Создаем поралельный поток с в которой будет выполняться функция PriemChikl с именм PriemChikl
        self.thre.start()# Запускаем поралельный поток
        self.qlbl.setText('Запущен')# Пишем в этикетку что поток запущен

    def buttonOnClicked(self):
        global signal_ui
        signal_ui = False
        self.thre.join()# Ожидаем завершение потока
        self.qbtn.setEnabled(True)
        self.qbtn_Stop.setEnabled(False)
        self.qlbl.setText('Готов')

    def PriemChikl(self):

        """
        В процессе работы с функцией serial было выяснены следующие особенности:

            Если не задать timeout= в com = serial.Serial('COM18', 9600, timeout=0.2) тотпрограмма зависнет на проверке сигнала
            rezault = int(com.readline().decode('UTF-8')) и будет висеть пока сигнал не поступит

            Информация с порта поступает в бинарном виде, по этому для преобразования ее в строку мы используем декодер decode('UTF-8')

           Усли в функии com = serial.Serial('COM18', 9600, timeout=0.2) не задовать timeout= то в переменную reza будет записони строка имеюшая 
           только номер нажатой клавиши (например "5624451"). По этому для выполнения проверок на жатой клавиши достаточно прописать 
           reza = int(com.readline().decode('UTF-8'))  и далее делать проверку:
           ПРИМЕР
           rezault = int(com.readline().decode('UTF-8'))
           elif rezault == space:
                pyautogui.press("space")

            
            Если же мы задаем timeout= то в переменную запишится строка содержащая номер кнопки пробел и символ переноса строки (например "54454 \n")
            По этому чтобы удалить символ переноса строки мы используеми .rstrip('\n'), а чтоды удалитьпробел перезаписываем переменную отнимая
            последний символ и преобразовывая в число rezault = int(reza[0:-1]). Так же потребцется дополнительноя проверка так как если сигнала от 
            пульта не будет то переменная будет при каждом цикле проверки пуст что выдаст ошибку при преобразовании.
        """

        global signal_ui
        com = serial.Serial('COM19', 9600, timeout=0.2)# Создаем подключение к COM потру указывая его номер, скорость подключения и время между проверками поступившего сигнала

        playpause = 11497# Создаем переменные с номераи кнопок
        space = 3772782313
        volumeup = 3772833823
        volumedown = 3772829743
        volumemute = 656
        left = 720
        right = 3280
        up = 752
        down = 2800
        enter = 2672
        multiply = 24101
        stop = 3305
        pover = 2704
        esc = 25321

        while (signal_ui):# Запускаем цикл для проверки поступаемого сигнала и сиуляции нажатия кнопки

            reza = com.readline().decode('UTF-8').rstrip('\n')# Получаем сигнал от СОМ порта преобразуем из бинарника в строку и идоляем перенос строки
            if reza !='':# Провеняем что резуьтат проверки приема порта не пустота
                rezault = int(reza[0:-1])# Удаляем з преременной пробул, преобразуем int и записываем в переменную
                self.qlbl.setText(str(rezault))# Отображаем поступивший сугнал в этикетке
                if rezault == playpause:# Проводим сравнение поступившего сигнала с заданными
                    pyautogui.press("space")# Симулируем нажатие нужной кнопки.
                elif rezault == space:
                    pyautogui.press("space")
                elif rezault == volumeup:
                    pyautogui.press("up")
                elif rezault == volumedown:
                    pyautogui.press("down")
                elif rezault == volumemute:
                    pyautogui.press("m")
                elif rezault == left:
                    pyautogui.press("left")
                elif rezault == right:
                    pyautogui.press("right")
                elif rezault == up:
                    pyautogui.press("up")
                elif rezault == down:
                    pyautogui.press("down")
                elif rezault == enter:
                    pyautogui.press("enter")
                elif rezault == multiply:
                    pyautogui.press("f")
                elif rezault == stop:
                    pyautogui.press("stop")
                elif rezault == pover:
                    subprocess.run(['shutdown', '-P'])# Производим выключение компьютера при нажатии на заданную кнопку
                elif rezault == esc:
                    pyautogui.press("esc")


if __name__ == '__main__':# Проверяем что произведен запуск именно данного файла
    app = QApplication(sys.argv)# Запускаем перехват событий
    ex = MyWidget()# Создаем окно
    sys.exit(app.exec())# При нажатии на крестик завершаем программу