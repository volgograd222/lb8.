import sys
import csv
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QApplication
)

class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.students = []
        self.initUI()

    def initUI(self):
        self.resize(1000, 600)
        self.setWindowTitle('Результаты олимпиады: фильтрация')

        self.school_combo = QComboBox()
        self.class_combo = QComboBox()

        self.school_combo.addItem('Школа', 'all_schools')
        self.school_combo.addItem('01')
        self.school_combo.addItem('02')
        self.school_combo.addItem('03')

        self.class_combo.addItem('Класс', 'all_classes')
        self.class_combo.addItem('09')
        self.class_combo.addItem('10')
        self.class_combo.addItem('11')

        self.table = QTableWidget()

        self.result_button = QPushButton('Узнать результаты')
        self.select_file_btn = QPushButton('Выберите файл')

        main_l = QVBoxLayout()
        h_l1 = QHBoxLayout()
        h_l2 = QHBoxLayout()

        main_l.addLayout(h_l1)
        main_l.addLayout(h_l2)

        h_l1.addWidget(self.school_combo)
        h_l1.addWidget(self.class_combo)
        h_l1.addWidget(self.result_button)
        h_l1.addWidget(self.select_file_btn)

        h_l2.addWidget(self.table)

        self.setLayout(main_l)

        self.school_combo.currentIndexChanged.connect(self.load_values)
        self.class_combo.currentIndexChanged.connect(self.load_values)
        self.result_button.clicked.connect(self.load_values)
        self.select_file_btn.clicked.connect(self.select_file)

    def select_file(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(self, 'Выберите CSV файл', '', 'CSV Files (*.csv)')
        if self.selected_file:
            self.load_values()

    def load_values(self):
        if not self.selected_file:
            return

        school_filter = self.school_combo.currentData()
        class_filter = self.class_combo.currentData()

        self.read_csv(school_filter, class_filter)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Фамилия', 'Результат', 'Логин'])
        self.table.setRowCount(len(self.students))

        for row, student in enumerate(self.students):
            self.table.setItem(row, 0, QTableWidgetItem(student['family']))
            self.table.setItem(row, 1, QTableWidgetItem(student['result']))
            self.table.setItem(row, 2, QTableWidgetItem(student['login']))

    def read_csv(self, school_filter, class_filter):
        self.students = []

        with open(self.selected_file, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            next(reader)

            for row in reader:
                login = row[2]
                _, school, class_, _ = login.split('-')

                if (school_filter == 'all_schools' or school_filter == school) and (class_filter == 'all_classes' or class_filter == class_):
                    family = row[1].split(' ')[-1]
                    result = row[-1]
                    self.students.append({'family': family, 'result': result, 'login': login})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec())
