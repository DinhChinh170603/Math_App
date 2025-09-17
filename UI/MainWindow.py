import sys
from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QTextEdit, QSpinBox
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QScreen
from .widgets import create_count_groupbox, create_draw_groupbox
from Logic.count_problem import count_numbers, count_numbers_optimized
from Logic.draw_problem import count_cards

class CalculationThread(QThread):
    results_ready = pyqtSignal(int, list, list)  # Added file_paths parameter
    progress_update = pyqtSignal(str)  # For progress messages

    def __init__(self, digits, conditions):
        super().__init__()
        self.digits = digits
        self.conditions = conditions

    def run(self):
        try:
            # Use optimized function that returns file paths for large results
            def progress_callback(message):
                self.progress_update.emit(message)
            
            result, number_list, file_paths = count_numbers_optimized(
                self.digits, self.conditions, progress_callback=progress_callback
            )
            self.results_ready.emit(result, number_list, file_paths)
        except Exception as e:
            print(f"Error in calculation: {e}")
            # Fallback to legacy function
            result, number_list = count_numbers(self.digits, self.conditions)
            self.results_ready.emit(result, number_list, [])

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
        self.resize(720, screen_height)
        self.setWindowIcon(QIcon('D:/TMQ-Math/UI/assets/Logo.png'))
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                border: 16px;
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(47, 204, 113, 255),
                    stop: 1 rgba(34, 152, 83, 255)
                );
                width: 5px;
            }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        scroll_layout = QVBoxLayout(self.scroll_widget)

        self.count_groupbox = create_count_groupbox()
        scroll_layout.addWidget(self.count_groupbox)
        self.draw_groupbox = create_draw_groupbox()
        scroll_layout.addWidget(self.draw_groupbox)
        
        self.result_display = self.create_result_display()
        main_layout.addWidget(self.scroll_area) 
        main_layout.addLayout(self.result_display)

        self.setup_connections()

        self.input_numbers = self.count_groupbox.findChild(QLineEdit, "input_numbers")
        self.checkbox_input_k_digits = self.count_groupbox.findChild(QCheckBox, "checkbox_input_k_digits")
        self.input_k_digits = self.count_groupbox.findChild(QLineEdit, "input_k_digits")
        self.checkbox_divisible_by = self.count_groupbox.findChild(QCheckBox, "checkbox_divisible_by")
        self.divisible_input = self.count_groupbox.findChild(QLineEdit, "divisible_input")
        self.checkbox_digit_sum_compare = self.count_groupbox.findChild(QCheckBox, "checkbox_digit_sum_compare")
        self.digit_sum_compare_input = self.count_groupbox.findChild(QLineEdit, "digit_sum_compare_input")
        self.checkbox_digit_sum_divisible = self.count_groupbox.findChild(QCheckBox, "checkbox_digit_sum_divisible")
        self.input_digit_sum_divisible = self.count_groupbox.findChild(QLineEdit, "digit_sum_divisible_input")
        self.checkbox_starts_by = self.count_groupbox.findChild(QCheckBox, "checkbox_starts_by")
        self.starts_input = self.count_groupbox.findChild(QLineEdit, "starts_input")
        self.checkbox_not_starts_by = self.count_groupbox.findChild(QCheckBox, "checkbox_not_starts_by")
        self.not_starts_input = self.count_groupbox.findChild(QLineEdit, "not_starts_input")
        self.checkbox_ends_by = self.count_groupbox.findChild(QCheckBox, "checkbox_ends_by")
        self.ends_input = self.count_groupbox.findChild(QLineEdit, "ends_input")
        self.checkbox_bigger_than = self.count_groupbox.findChild(QCheckBox, "checkbox_bigger_than")
        self.bigger_than_input = self.count_groupbox.findChild(QLineEdit, "bigger_than_input")
        self.checkbox_includes_digits = self.count_groupbox.findChild(QCheckBox, "checkbox_includes_digits")
        self.includes_digits_input = self.count_groupbox.findChild(QLineEdit, "includes_digits_input")
        self.checkbox_not_includes_by = self.count_groupbox.findChild(QCheckBox, "checkbox_not_includes_by")
        self.not_includes_input = self.count_groupbox.findChild(QLineEdit, "not_includes_input")
        self.checkbox_starts_by_0 = self.count_groupbox.findChild(QCheckBox, "checkbox_starts_by_0")
        self.checkbox_specific_positions = self.count_groupbox.findChild(QCheckBox, "checkbox_specific_positions")
        self.specific_positions_input = self.count_groupbox.findChild(QLineEdit, "specific_positions_input")
        self.checkbox_not_divisible_by = self.count_groupbox.findChild(QCheckBox, "checkbox_not_divisible_by")
        self.not_divisible_input = self.count_groupbox.findChild(QLineEdit, "not_divisible_input")
        self.remainder_input = self.count_groupbox.findChild(QLineEdit, "remainder_input")
        
        self.calculate_sum_checkbox = self.count_groupbox.findChild(QCheckBox, "calculate_sum_checkbox")
        self.checkbox_is_k_digits = self.count_groupbox.findChild(QCheckBox, "checkbox_is_k_digits")
        self.even_checkbox = self.count_groupbox.findChild(QCheckBox, "even_checkbox")
        self.odd_checkbox = self.count_groupbox.findChild(QCheckBox, "odd_checkbox")
        self.palindrome_checkbox = self.count_groupbox.findChild(QCheckBox, "palindrome_checkbox")
        self.prime_checkbox = self.count_groupbox.findChild(QCheckBox, "prime_checkbox")
        self.square_checkbox = self.count_groupbox.findChild(QCheckBox, "square_checkbox")
        self.cube_checkbox = self.count_groupbox.findChild(QCheckBox, "cube_checkbox")
        self.all_diff_checkbox = self.count_groupbox.findChild(QCheckBox, "all_different")
        self.increasing_digits_checkbox = self.count_groupbox.findChild(QCheckBox, "increasing_digits_checkbox")
        self.decreasing_digits_checkbox = self.count_groupbox.findChild(QCheckBox, "decreasing_digits_checkbox")
        
        self.arithmetic_checkbox = self.count_groupbox.findChild(QCheckBox, "arithmetic_checkbox")
        self.arithmetic_input = self.count_groupbox.findChild(QLineEdit, "arithmetic_input")
        self.geometric_checkbox = self.count_groupbox.findChild(QCheckBox, "geometric_checkbox")
        self.geometric_input = self.count_groupbox.findChild(QLineEdit, "geometric_input")

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
        self.result_output.setFixedHeight(300) 
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
        elif any(conditions[k] is not None and not conditions[k] for k in ['divisible_by', 'bigger_than', 'ends_by', 'is_k_digits', 'starts_by', 'not_starts_by', 'not_includes_by'] if k in conditions):
            self.result_output.setText("Vui lòng kiểm tra lại các trường nhập còn thiếu!")
            return
        
        digits = self.input_numbers.text().replace(',', '')
        self.calculation_thread = CalculationThread(digits, conditions)
        self.calculation_thread.results_ready.connect(self.update_results)
        self.calculation_thread.progress_update.connect(self.show_progress_message)
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
            'divisible_by': self.divisible_input.text() if self.checkbox_divisible_by.isChecked() else None,
            'digit_sum_compare': self.digit_sum_compare_input.text() if self.checkbox_digit_sum_compare.isChecked() else None,
            'not_divisible_by': self.not_divisible_input.text() if self.checkbox_not_divisible_by.isChecked() else None,
            'digit_sum_divisible_by': self.input_digit_sum_divisible.text() if self.checkbox_digit_sum_divisible.isChecked() else None,
            'remainder': self.remainder_input.text() if self.count_groupbox.findChild(QCheckBox, "checkbox_remainder").isChecked() else None,
            'starts_by': self.starts_input.text() if self.checkbox_starts_by.isChecked() else None,
            'not_starts_by': self.not_starts_input.text() if self.checkbox_not_starts_by.isChecked() else None,
            'not_includes_by': self.not_includes_input.text() if self.checkbox_not_includes_by.isChecked() else None,
            'ends_by': self.ends_input.text() if self.checkbox_ends_by.isChecked() else None,
            'bigger_than': self.bigger_than_input.text() if self.checkbox_bigger_than.isChecked() else None,
            'includes_digits': self.includes_digits_input.text() if self.checkbox_includes_digits.isChecked() else None,
            'specific_positions': self.specific_positions_input.text() if self.checkbox_specific_positions.isChecked() and 
                                   self.checkbox_includes_digits.isChecked() and self.checkbox_input_k_digits.isChecked() else None,
            'is_even': self.even_checkbox.isChecked(),
            'is_odd': self.odd_checkbox.isChecked(),
            'is_palindrome': self.palindrome_checkbox.isChecked(),
            'is_prime': self.prime_checkbox.isChecked(),
            'is_square': self.square_checkbox.isChecked(),
            'is_cube': self.cube_checkbox.isChecked(),
            'all_different': self.all_diff_checkbox.isChecked(),
            'is_increasing': self.increasing_digits_checkbox.isChecked(),
            'is_decreasing': self.decreasing_digits_checkbox.isChecked(),
            'arithmetic_progression': self.arithmetic_input.text() if self.arithmetic_checkbox.isChecked() else None,
            'geometric_progression': self.geometric_input.text() if self.geometric_checkbox.isChecked() else None,
            'allow_leading_zeros': self.checkbox_starts_by_0.isChecked()
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

    def update_results(self, result, number_list, file_paths=None):
        display_text = f"Số lượng số thỏa mãn: {result}"
        
        if number_list:
            int_numbers = [int(num) for num in number_list]
            min_value = min(int_numbers)
            max_value = max(int_numbers)
            display_text += f" - số nhỏ nhất: {min_value} - số lớn nhất: {max_value}"
        
        display_text += "\n"
        
        # Handle large result sets that were saved to files
        if file_paths and len(file_paths) > 0:
            display_text += f"\n⚠️ KẾT QUẢ LỚN - ĐÃ CHIA THÀNH {len(file_paths)} FILE:\n"
            for i, file_path in enumerate(file_paths, 1):
                display_text += f"📁 File {i}: {file_path}\n"
            display_text += f"\n🔍 Hiển thị {len(number_list):,} số đầu tiên (từ tổng {result:,} số):\n"
        
        if hasattr(self, 'calculate_sum_checkbox') and self.calculate_sum_checkbox.isChecked():
            total_sum = sum(int(num) for num in number_list)
            display_text += f"Tổng các giá trị phần tử thỏa mãn (mẫu hiển thị): {total_sum}\n"
        
        display_text += ", ".join(map(str, number_list))
        self.result_output.setText(display_text)
    
    def show_progress_message(self, message):
        """Display progress messages during calculation."""
        current_text = self.result_output.toPlainText()
        if "Đang tính toán..." not in current_text:
            self.result_output.setText("Đang tính toán...\n" + message)
        else:
            lines = current_text.split('\n')
            lines[-1] = message
            self.result_output.setText('\n'.join(lines))

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
