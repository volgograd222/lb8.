import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QFileDialog, QPushButton
from PyQt6.QtCore import Qt


class OlympicResultsViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Olympic Results Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Login", "Name", "Score"])

        self.school_filter = QComboBox(self)
        self.school_filter.addItem("All Schools")
        self.school_filter.currentIndexChanged.connect(self.filter_results)

        self.class_filter = QComboBox(self)
        self.class_filter.addItem("All Classes")
        self.class_filter.currentIndexChanged.connect(self.filter_results)

        self.load_button = QPushButton("Load CSV", self)
        self.load_button.clicked.connect(self.load_csv)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.school_filter)
        layout.addWidget(self.class_filter)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data = []
        self.schools = set()
        self.classes = set()

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.data = []
                    self.schools.clear()
                    self.classes.clear()

                    for row in reader:
                        if len(row) < 8:
                            continue  # Пропуск некорректных строк

                        place, user_name, login, *_, score = row
                        score = int(score)
                        self.data.append((login, user_name, score))

                        _, school, school_class, _ = login.split('-')
                        self.schools.add(school)
                        self.classes.add(school_class)

                self.update_filters()
                self.filter_results()
            except Exception as e:
                print(f"Error loading CSV: {e}")  # Вы можете использовать здесь диалоговое окно для отображения ошибки

    def update_filters(self):
        self.school_filter.clear()
        self.school_filter.addItem("All Schools")
        self.school_filter.addItems(sorted(self.schools))

        self.class_filter.clear()
        self.class_filter.addItem("All Classes")
        self.class_filter.addItems(sorted(self.classes))

    def filter_results(self):
        selected_school = self.school_filter.currentText()
        selected_class = self.class_filter.currentText()

        filtered_data = [
            (login, user_name, score) for login, user_name, score in self.data
            if (selected_school == "All Schools" or f"-{selected_school}-" in login)
            and (selected_class == "All Classes" or f"-{selected_class}-" in login)
        ]

        self.table.setRowCount(len(filtered_data))
        for row_idx, (login, user_name, score) in enumerate(filtered_data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(login))
            self.table.setItem(row_idx, 1, QTableWidgetItem(user_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(score)))

        self.highlight_top_places(filtered_data)

    def highlight_top_places(self, filtered_data):
        sorted_data = sorted(filtered_data, key=lambda x: x[2], reverse=True)
        place_colors = {1: Qt.GlobalColor.yellow, 2: Qt.GlobalColor.lightGray, 3: Qt.GlobalColor.darkGray}

        place_rank = 1
        previous_score = None
        for index, (_, _, score) in enumerate(sorted_data):
            if previous_score is not None and score < previous_score:
                place_rank += 1
            if place_rank > 3:
                break
            previous_score = score

            for col in range(self.table.columnCount()):
                self.table.item(index, col).setBackground(place_colors.get(place_rank, Qt.GlobalColor.white))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = OlympicResultsViewer()
    viewer.show()
    sys.exit(app.exec())