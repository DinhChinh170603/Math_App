import sys
from PyQt6.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QTextEdit, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .widgets import create_count_groupbox, create_draw_groupbox, create_partition_groupbox
from .view_models import (
    CalculationThread, CardCalculationThread, 
    PartitionCalculationThread, ResultFormatter,
    AsyncPartitionCalculationThread
)
from Logic.partition_problem import parse_partition_input, parse_labels_input

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
        """Create and setup the main UI layout"""
        main_layout = QVBoxLayout(self)

        # Create scrollable area for input sections
        self.scroll_area = self.create_scroll_area()
        
        # Create results display area
        self.result_display = self.create_result_display()
        
        # Add components to main layout
        main_layout.addWidget(self.scroll_area) 
        main_layout.addLayout(self.result_display)

        # Initialize widget references and connect signals
        self.initialize_widgets()
        self.setup_connections()

    def create_scroll_area(self):
        """Create a scrollable area containing the input sections"""
        scroll_area = QScrollArea(self)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
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
        scroll_area.setWidgetResizable(True)
        
        # Create widget to hold content
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_layout = QVBoxLayout(scroll_widget)

        # Add groupboxes to scroll area
        self.count_groupbox = create_count_groupbox()
        scroll_layout.addWidget(self.count_groupbox)
        
        self.draw_groupbox = create_draw_groupbox()
        scroll_layout.addWidget(self.draw_groupbox)
        
        self.partition_groupbox = create_partition_groupbox()
        scroll_layout.addWidget(self.partition_groupbox)
        
        return scroll_area

    def create_result_display(self):
        """Create the results display area"""
        layout = QVBoxLayout()
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setFixedHeight(300) 
        layout.addWidget(self.result_output)
        return layout

    def initialize_widgets(self):
        """Initialize and store references to UI widgets"""
        # Count group widgets
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

        # Draw group widgets
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

    def setup_connections(self):
        """Connect UI signals to their handlers"""
        # Count problem
        calculate_button = self.count_groupbox.findChild(QPushButton, "calculate_button")
        calculate_button.clicked.connect(self.handle_calculation)
        
        # Card problem
        calculate_button1 = self.draw_groupbox.findChild(QPushButton, "calculate_button1")
        calculate_button1.clicked.connect(self.handle_drawcard_calculation)
        
        # Partition problem
        calculate_partition_button = self.partition_groupbox.findChild(QPushButton, "calculate_partition_button")
        calculate_partition_button.clicked.connect(self.handle_partition_calculation)
        
        stop_partition_button = self.partition_groupbox.findChild(QPushButton, "stop_partition_button")
        stop_partition_button.clicked.connect(self.stop_partition_calculation)

        # Link checkboxes for mutual exclusivity
        checkbox_circle = self.partition_groupbox.findChild(QCheckBox, "checkbox_circle")
        checkbox_row = self.partition_groupbox.findChild(QCheckBox, "checkbox_row")
        checkbox_circle.toggled.connect(lambda checked: self.ensure_single_checkbox(checked, checkbox_row))
        checkbox_row.toggled.connect(lambda checked: self.ensure_single_checkbox(checked, checkbox_circle))
        
    def ensure_single_checkbox(self, checked, other_checkbox):
        """Ensure only one checkbox can be checked at a time"""
        if checked:
            other_checkbox.setChecked(False)

    def setup_conditions(self):
        """Get the conditions for count problem calculations"""
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
        return conditions

    def setup_draw_conditions(self):
        """Get the conditions for card draw problem calculations"""
        conditions = {
            'drawn_cards': self.input_drawn.text() if self.checkbox_drawn.isChecked() else None,
            'num_even': self.input_even.text() if self.checkbox_even.isChecked() else None,
            'sum_divi': self.input_sum_divi.text() if self.checkbox_sum_divisible.isChecked() else None,
            'pro_divi': self.input_product_divi.text() if self.checkbox_product_divisible.isChecked() else None
        }
        return conditions

    def handle_calculation(self):
        """Handle calculation for number counting problems"""
        self.result_output.setText("Đang tính toán...")
        QApplication.processEvents()
        
        # Validate inputs
        conditions = self.setup_conditions()
        
        # Check for missing required inputs
        if not self.validate_count_inputs(conditions):
            return
        
        # Start calculation thread
        self.calculation_thread = CalculationThread(
            self.input_numbers.text().replace(',', ''), 
            conditions
        )
        self.calculation_thread.results_ready.connect(self.update_results)
        self.calculation_thread.start()

    def validate_count_inputs(self, conditions):
        """Validate inputs for count problem calculations"""
        # Check enabled checkboxes with empty inputs
        if any(v is None for k, v in conditions.items() 
              if k.startswith('has_') or k.startswith('divisible_') or k.startswith('starts_') or
                 k.startswith('not_') or k.startswith('ends_') or k.startswith('bigger_') or k.startswith('is_k_')
              and self.count_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()):
            missing_inputs = [k for k, v in conditions.items() 
                             if v is None 
                             and (k.startswith('has_') or k.startswith('divisible_') or k.startswith('starts_') or
                                 k.startswith('not_') or k.startswith('ends_') or k.startswith('bigger_') or k.startswith('is_k_'))
                             and self.count_groupbox.findChild(QCheckBox, f"checkbox_{k}").isChecked()]
            self.result_output.setText(f"Vui lòng nhập thông tin cho: {', '.join(missing_inputs)}")
            return False
        
        # Check for required inputs
        if not self.input_numbers.text().strip():
            self.result_output.setText("Vui lòng nhập chuỗi chữ số mong muốn!")
            return False
        elif not self.checkbox_input_k_digits.isChecked() and not self.input_k_digits.text().strip():
            self.result_output.setText("Vui lòng chọn và nhập số chữ số mong muốn!")
            return False
            
        # Check for empty but enabled condition inputs
        check_keys = ['divisible_by', 'bigger_than', 'ends_by', 'is_k_digits', 'starts_by', 'not_starts_by', 'not_includes_by']
        if any(conditions[k] is not None and not conditions[k] for k in check_keys if k in conditions):
            self.result_output.setText("Vui lòng kiểm tra lại các trường nhập còn thiếu!")
            return False
            
        return True

    def handle_drawcard_calculation(self):
        """Handle calculation for card drawing problems"""
        self.result_output.setText("Đang tính toán...")
        QApplication.processEvents()
        
        conditions = self.setup_draw_conditions()

        # Validate inputs
        if not self.validate_draw_inputs(conditions):
            return
        
        # Start calculation thread
        start_value = int(self.input_start_at.text())
        end_value = int(self.input_end_at.text())
        card_value = self.input_cards.text() if self.input_cards.text() else None
        
        self.card_calculation_thread = CardCalculationThread(
            start_value, end_value, card_value, conditions
        )
        self.card_calculation_thread.results_ready.connect(self.update_draw_results)
        self.card_calculation_thread.start()
    
    def validate_draw_inputs(self, conditions):
        """Validate inputs for card draw problem calculations"""
        if any(v is None for k, v in conditions.items() if k in ['drawn_cards', 'num_even', 'sum_divi', 'pro_divi'] 
              and getattr(self, f"checkbox_{k.replace('drawn_cards', 'drawn').replace('num_even', 'even').replace('sum_divi', 'sum_divisible').replace('pro_divi', 'product_divisible')}").isChecked()):
            missing_inputs = [k for k, v in conditions.items() 
                             if v is None and k in ['drawn_cards', 'num_even', 'sum_divi', 'pro_divi'] 
                             and getattr(self, f"checkbox_{k.replace('drawn_cards', 'drawn').replace('num_even', 'even').replace('sum_divi', 'sum_divisible').replace('pro_divi', 'product_divisible')}").isChecked()]
            self.result_output.setText(f"Vui lòng nhập thông tin cho: {', '.join(missing_inputs)}")
            return False
        
        if not self.checkbox_drawn.isChecked() and not self.input_drawn.text().strip():
            self.result_output.setText("Vui lòng chọn và nhập số thẻ trong một bộ!")
            return False
        
        if any(conditions[k] is not None and not conditions[k] for k in ['drawn_cards', 'num_even', 'sum_divi', 'pro_divi'] if k in conditions):
            self.result_output.setText("Vui lòng kiểm tra lại các trường nhập còn thiếu!")
            return False
            
        return True
    
    def handle_partition_calculation(self):
        """Handle calculation for partition problems"""
        # Get widgets
        input_numbers = self.partition_groupbox.findChild(QLineEdit, "input_partition_numbers")
        input_labels = self.partition_groupbox.findChild(QLineEdit, "input_partition_labels")
        checkbox_circle = self.partition_groupbox.findChild(QCheckBox, "checkbox_circle")
        checkbox_row = self.partition_groupbox.findChild(QCheckBox, "checkbox_row")

        # Default to row if nothing selected
        if not checkbox_circle.isChecked() and not checkbox_row.isChecked():
            checkbox_row.setChecked(True)

        self.result_output.setText("Đang chuẩn bị tính toán...")
        QApplication.processEvents()

        try:
            # Parse input and start calculation
            counts = parse_partition_input(input_numbers.text())
            labels = parse_labels_input(input_labels.text()) if input_labels.text().strip() else None
            
            # Validate labels match counts
            if labels and len(labels) != len(counts):
                self.result_output.setText(f"Lỗi: Số lượng nhãn ({len(labels)}) phải bằng số lượng loại ({len(counts)}).")
                return
                
            is_circle = checkbox_circle.isChecked()
            
            # Create and connect the calculation thread
            if hasattr(self, 'partition_thread') and self.partition_thread.isRunning():
                self.partition_thread.stop()
                self.partition_thread.wait()
                
            # Use AsyncPartitionCalculationThread for better performance
            self.partition_thread = AsyncPartitionCalculationThread(counts, labels, is_circle)
            self.partition_thread.results_ready.connect(self.update_partition_results)
            self.partition_thread.progress_updated.connect(self.update_partition_progress)
            self.partition_thread.start()

        except Exception as e:
            self.result_output.setText(f"Lỗi: {str(e)}")

    def stop_partition_calculation(self):
        """Stop the partition calculation thread if it's running"""
        if hasattr(self, 'partition_thread') and self.partition_thread.isRunning():
            self.partition_thread.stop()
            self.result_output.setText("Tính toán đã bị hủy.")

    def update_partition_progress(self, progress, count):
        """Update UI with partition calculation progress"""
        if progress <= 100:  # Update for all progress
            if count == 0 and progress == 100:
                display_text = "Không có cách xếp thỏa mãn với điều kiện đã cho."
            else:
                display_text = ResultFormatter.format_partition_progress(progress, count)
            
            self.result_output.setText(display_text)
            QApplication.processEvents()  # Make sure UI updates

    def update_partition_results(self, count, arrangements, labels, result_file):
        """Update UI with partition results"""
        checkbox_circle = self.partition_groupbox.findChild(QCheckBox, "checkbox_circle")
        is_circle = checkbox_circle.isChecked()
        
        display_text = ResultFormatter.format_partition_results(
            count, arrangements, is_circle, labels, result_file
        )
        self.result_output.setText(display_text)

    def update_draw_results(self, result, card_list):
        """Update UI with card draw results"""
        display_text = ResultFormatter.format_card_results(result, card_list)
        self.result_output.setText(display_text)

    def update_results(self, result, number_list):
        """Update UI with number counting results"""
        display_text = ResultFormatter.format_number_results(result, number_list)
        self.result_output.setText(display_text)