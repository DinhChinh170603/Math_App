from msilib.schema import CheckBox
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QTextEdit, QSpinBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QScreen
from .widgets import create_count_groupbox, create_draw_groupbox
from Logic.count_problem import count_numbers
from Logic.draw_problem import count_cards

class CalculationThread(QThread):
    results_ready = pyqtSignal(int, list)

    def __init__(self, digits, conditions):
        super().__init__()
        self.digits = digits
        self.conditions = conditions

    def run(self):
        result, number_list = count_numbers(self.digits, self.conditions)
        self.results_ready.emit(result, number_list)

class CardCalculationThread(QThread):
    results_ready = pyqtSignal(object, list)

    def __init__(self, start, end, cards, conditions):
        super().__init__()
        self.start_value = start
        self.end_value = end
        self.cards = cards
        self.conditions = conditions

    def run(self):
        if self.cards:
            result, card_list = count_cards(None, None, self.cards, self.conditions)
        else:
            result, card_list = count_cards(self.start_value, self.end_value, None, self.conditions)
        self.results_ready.emit(result, card_list)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bài Toán Đếm Số & Rút Thẻ")
        screen = QApplication.primaryScreen()
        size = screen.size()
        screen_height = size.height() - 90
        self.resize(650, screen_height)
        self.setWindowIcon(QIcon('D:/TMQ-Math/UI/assets/Logo.png'))
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.count_groupbox = create_count_groupbox()
        main_layout.addWidget(self.count_groupbox)
        self.draw_groupbox = create_draw_groupbox()
        main_layout.addWidget(self.draw_groupbox)
        self.result_display = self.create_result_display()
        main_layout.addLayout(self.result_display)
        self.setup_connections()

        # Truy xuất và lưu trữ các widget cụ thể
        self.input_numbers = self.count_groupbox.findChild(QLineEdit, "input_numbers")
        self.checkbox_input_k_digits = self.count_groupbox.findChild(QCheckBox, "checkbox_input_k_digits")
        self.input_k_digits = self.count_groupbox.findChild(QLineEdit, "input_k_digits")
        self.checkbox_starts_by = self.count_groupbox.findChild(QCheckBox, "checkbox_starts_by")
        self.input_starts_by = self.count_groupbox.findChild(QLineEdit, "starts_input")
        self.checkbox_not_starts_by = self.count_groupbox.findChild(QCheckBox, "checkbox_not_starts_by")
        self.input_not_starts_by = self.count_groupbox.findChild(QLineEdit, "not_starts_input")
        self.checkbox_not_includes_by = self.count_groupbox.findChild(QCheckBox, "checkbox_not_includes_by")
        self.input_not_includes_by = self.count_groupbox.findChild(QLineEdit, "not_includes_input")
        self.input_divisible_by = self.count_groupbox.findChild(QLineEdit, "divisible_input")
        self.checkbox_divisible_by = self.count_groupbox.findChild(QCheckBox, "checkbox_divisible_by")
        self.input_ends_by = self.count_groupbox.findChild(QLineEdit, "ends_input")
        self.checkbox_ends_by = self.count_groupbox.findChild(QCheckBox, "checkbox_ends_by")
        self.input_bigger_than = self.count_groupbox.findChild(QLineEdit, "bigger_than_input")
        self.checkbox_bigger_than = self.count_groupbox.findChild(QCheckBox, "checkbox_bigger_than")
        self.input_is_k_digits = self.count_groupbox.findChild(QLineEdit, "is_k_digits_input")
        self.checkbox_is_k_digits = self.count_groupbox.findChild(QCheckBox, "checkbox_is_k_digits")
        self.even_checkbox = self.count_groupbox.findChild(QCheckBox, "even_checkbox")
        self.odd_checkbox = self.count_groupbox.findChild(QCheckBox, "odd_checkbox")
        self.palindrome_checkbox = self.count_groupbox.findChild(QCheckBox, "palindrome_checkbox")
        self.prime_checkbox = self.count_groupbox.findChild(QCheckBox, "prime_checkbox")
        self.square_checkbox = self.count_groupbox.findChild(QCheckBox, "square_checkbox")
        self.cube_checkbox = self.count_groupbox.findChild(QCheckBox, "cube_checkbox")
        self.all_diff_checkbox = self.count_groupbox.findChild(QCheckBox, "all_different")

        self.input_cards = self.draw_groupbox.findChild(QLineEdit, "input_cards")
        self.input_start_at = self.draw_groupbox.findChild(QSpinBox, "start_at_input")
        self.input_end_at = self.draw_groupbox.findChild(QSpinBox, "end_at_input")
        self.checkbox_drawn = self.draw_groupbox.findChild(QCheckBox, "checkbox_input_drawn")
        self.input_drawn = self.draw_groupbox.findChild(QLineEdit, "input_drawn")
        self.checkbox_even = self.draw_groupbox.findChild(QCheckBox, "checkbox_input_even")
        self.input_even = self.draw_groupbox.findChild(QLineEdit, "input_even")
        self.checkbox_sum_divisible = self.draw_groupbox.findChild(QCheckBox, "checkbox_input_sum_divi")
        self.input_sum_divi = self.draw_groupbox.findChild(QLineEdit, "input_sum_divi")
        self.checkbox_product_divisible = self.draw_groupbox.findChild(QCheckBox, "checkbox_input_product_divi")
        self.input_product_divi = self.draw_groupbox.findChild(QLineEdit, "input_product_divi")

    def create_result_display(self):
        layout = QVBoxLayout()
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)
        return layout

    def handle_calculation(self):
        self.result_output.setText("Waiting...")
        QApplication.processEvents()
        conditions = self.setup_conditions()
        if any(v is None for k, v in conditions.items() if 'input' in k and self.count_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()):
            missing_inputs = [k.replace('input_', '') for k, v in conditions.items() if v is None and 'input' in k and self.count_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()]
            self.result_output.setText(f"Vui lòng nhập thông tin cho: {', '.join(missing_inputs)}")
            return
        
        if not self.input_numbers.text().strip():
            self.result_output.setText("Vui lòng nhập chuỗi chữ số mong muốn!")
            return
        elif not self.checkbox_input_k_digits.isChecked() and not self.input_k_digits.text().strip():
            self.result_output.setText("Vui lòng chọn và nhập số chữ số mong muốn!")
            return
        # Add additional checks for any key condition that requires a valid integer but is empty or invalid
        elif any(conditions[k] is not None and not conditions[k] for k in ['divisible_by', 'bigger_than', 'ends_by', 'is_k_digits', 'starts_by', 'not_starts_by', 'not_includes_by'] if k in conditions):
            self.result_output.setText("Vui lòng kiểm tra lại các trường nhập còn thiếu!")
            return
        
        self.calculation_thread = CalculationThread(self.input_numbers.text().replace(',', ''), conditions)
        self.calculation_thread.results_ready.connect(self.update_results)
        self.calculation_thread.start()

    def handle_drawcard_calculation(self):
        self.result_output.setText("Waiting...")
        QApplication.processEvents()
        conditions = self.setup_draw_conditions()

        if any(v is None for k, v in conditions.items() if 'input' in k and self.draw_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()):
            missing_inputs = [k.replace('input_', '') for k, v in conditions.items() if v is None and 'input' in k and self.draw_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()]
            self.result_output.setText(f"Vui lòng nhập thông tin cho: {', '.join(missing_inputs)}")
            return
        
        if not self.checkbox_drawn.isChecked() and not self.input_drawn.text().strip():
            self.result_output.setText("Vui lòng chọn và nhập số thẻ trong một bộ!")
            return
        
        if any(conditions[k] is not None and not conditions[k] for k in ['drawn_cards', 'num_even', 'sum_divi', 'pro_divi'] if k in conditions):
            self.result_output.setText("Vui lòng kiểm tra lại các trường nhập còn thiếu!")
            return
        
        start_value = int(self.input_start_at.text())
        end_value = int(self.input_end_at.text())
        card_value = self.input_cards.text() if self.input_cards.text() else None
        self.card_calculation_thread = CardCalculationThread(start_value, end_value, card_value, conditions)
        self.card_calculation_thread.results_ready.connect(self.update_draw_results)
        self.card_calculation_thread.start()

    def setup_connections(self):
        calculate_button = self.count_groupbox.findChild(QPushButton, "calculate_button")
        calculate_button.clicked.connect(self.handle_calculation)
        calculate_button1 = self.draw_groupbox.findChild(QPushButton, "calculate_button1")
        calculate_button1.clicked.connect(self.handle_drawcard_calculation)

    def setup_conditions(self):
        conditions = {
            'has_k_digits': self.input_k_digits.text() if self.checkbox_input_k_digits.isChecked() else None,
            'divisible_by': self.input_divisible_by.text() if self.checkbox_divisible_by.isChecked() else None,
            'starts_by': self.input_starts_by.text() if self.checkbox_starts_by.isChecked() else None,
            'not_starts_by': self.input_not_starts_by.text() if self.checkbox_not_starts_by.isChecked() else None,
            'not_includes_by': self.input_not_includes_by.text() if self.checkbox_not_includes_by.isChecked() else None,
            'ends_by': self.input_ends_by.text() if self.checkbox_ends_by.isChecked() else None,
            'bigger_than': self.input_bigger_than.text() if self.checkbox_bigger_than.isChecked() else None,
            'is_k_digits': self.input_is_k_digits.text() if self.checkbox_is_k_digits.isChecked() else None,
            'is_even': self.even_checkbox.isChecked(),
            'is_odd': self.odd_checkbox.isChecked(),
            'is_palindrome': self.palindrome_checkbox.isChecked(),
            'is_prime': self.prime_checkbox.isChecked(),
            'is_square': self.square_checkbox.isChecked(),
            'is_cube': self.cube_checkbox.isChecked(),
            'all_different': self.all_diff_checkbox.isChecked()
        }
        print(f"Conditions: {conditions}")
        return conditions

    def setup_draw_conditions(self):
        conditions1 = {
            'drawn_cards': self.input_drawn.text() if self.checkbox_drawn.isChecked() else None,
            'num_even': self.input_even.text() if self.checkbox_even.isChecked() else None,
            'sum_divi': self.input_sum_divi.text() if self.checkbox_sum_divisible.isChecked() else None,
            'pro_divi': self.input_product_divi.text() if self.checkbox_product_divisible.isChecked() else None
        }
        return conditions1

    def update_results(self, result, number_list):
        display_text = f"Số lượng số thỏa mãn: {result}\n" + ", ".join(map(str, number_list))
        self.result_output.setText(display_text)

    def update_draw_results(self, result, card_list):
        def format_card_list(card_list, max_line_length=125):
            lines = []
            current_line = ""
            for card in card_list:
                card_str = str(card)
                if len(current_line) + len(card_str) + 2 > max_line_length:  # +2 for ", "
                    lines.append(current_line)
                    current_line = card_str
                else:
                    if current_line:
                        current_line += ", " + card_str
                    else:
                        current_line = card_str
            if current_line:
                lines.append(current_line)
            return "\n".join(lines)
        formatted_card_list = format_card_list(card_list)
        display_text = f"Số lượng thẻ thỏa mãn: {result}\n[" + formatted_card_list + "]"
        self.result_output.setText(display_text)
