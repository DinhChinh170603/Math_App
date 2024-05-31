import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QHBoxLayout
from .widgets import create_count_groupbox
from Logic.count_problem import count_numbers

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bài Toán Đếm Số & Rút Thẻ")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Tạo các widget từ widgets.py
        self.count_groupbox = create_count_groupbox()
        main_layout.addWidget(self.count_groupbox)

        # Tạo kết quả hiển thị
        self.result_display = self.create_result_display()
        main_layout.addLayout(self.result_display)

        # Truy xuất và lưu trữ các widget cụ thể
        self.input_numbers = self.count_groupbox.findChild(QLineEdit, "input_numbers")
        self.input_k_digits = self.count_groupbox.findChild(QLineEdit, "input_k_digits")
        self.input_divisible_by = self.count_groupbox.findChild(QLineEdit, "divisible_input")
        self.checkbox_divisible_by = self.count_groupbox.findChild(QCheckBox, "checkbox_divisible_by")

        # Lấy nút tính toán và kết nối với hàm xử lý
        calculate_button = self.count_groupbox.findChild(QPushButton, "calculate_button")

        # Kết nối sự kiện
        calculate_button.clicked.connect(self.handle_calculation)

    def create_result_display(self):
        layout = QHBoxLayout()
        result_label = QLabel("Số lượng số thỏa mãn: ")
        self.result_output = QLineEdit()
        self.result_output.setObjectName("result_output")
        self.result_output.setReadOnly(True)
        layout.addWidget(result_label)
        layout.addWidget(self.result_output)
        return layout

    def handle_calculation(self):
        input_digits = self.input_numbers.text().replace(',', '')  # ví dụ: '2,3,4'
        num_length = int(self.input_k_digits.text())  # số chữ số, ví dụ: 4
        print(f"Digits: {input_digits}")
        print(f"Number length: {num_length}")

        conditions = {}
        if self.checkbox_divisible_by.isChecked():
            divisible_by = int(self.input_divisible_by.text())
            conditions['divisible_by'] = divisible_by
            print(f"Divisible by: {divisible_by}")

        result = count_numbers(input_digits, num_length, conditions)
        self.result_output.setText(str(result))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
