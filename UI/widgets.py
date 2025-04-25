from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QSpinBox
)
from .ui_utils import create_labeled_checkbox_input, create_calculation_button, create_checkbox

# addWidget(widget, row, column, rowspan, colspan)
### *** Bài toán đếm số ***

def create_count_groupbox():
    groupbox = QGroupBox("Bài Toán Đếm Số")
    layout = QGridLayout(groupbox)

    # Nhập chuỗi chữ số
    layout.addWidget(QLabel("Nhập chuỗi chữ số (ví dụ: 0,1,2,3,...):"), 0, 0)
    input_numbers = QLineEdit()
    input_numbers.setObjectName("input_numbers")
    layout.addWidget(input_numbers, 0, 1, 1, 3)

    # Create checkboxes with linked inputs
    create_labeled_checkbox_input(
        layout, "Có k chữ số", "checkbox_input_k_digits", "input_k_digits", 
        "Nhập số chữ số", 1, 0, 1, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Chia hết cho", "checkbox_divisible_by", "divisible_input", 
        "Nhập a,b,c,...", 2, 0, 2, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Bắt đầu bằng", "checkbox_starts_by", "starts_input", 
        "Nhập a,b,c,...", 3, 0, 3, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Không bắt đầu bằng", "checkbox_not_starts_by", "not_starts_input", 
        "Nhập a,b,c,...", 4, 0, 4, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Không có mặt các chữ số", "checkbox_not_includes_by", "not_includes_input", 
        "Nhập a,b,c,...", 6, 2, 6, 3
    )
    
    create_labeled_checkbox_input(
        layout, "Nhỏ hơn", "checkbox_ends_by", "ends_input", 
        "Nhập số", 5, 0, 5, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Lớn hơn", "checkbox_bigger_than", "bigger_than_input", 
        "Nhập số", 5, 2, 5, 3
    )
    
    create_labeled_checkbox_input(
        layout, "Luôn có mặt các chữ số", "checkbox_is_k_digits", "is_k_digits_input", 
        "Nhập a,b,c,...", 6, 0, 6, 1
    )

    # Create simple checkboxes
    create_checkbox(layout, "Số chẵn", "even_checkbox", 1, 2)
    create_checkbox(layout, "Số đối xứng", "palindrome_checkbox", 2, 2)
    create_checkbox(layout, "Số lẻ", "odd_checkbox", 1, 3)
    create_checkbox(layout, "Số nguyên tố", "prime_checkbox", 2, 3)
    create_checkbox(layout, "Số chính phương", "square_checkbox", 3, 2)
    create_checkbox(layout, "Số lập phương", "cube_checkbox", 3, 3)
    create_checkbox(layout, "Chữ số khác nhau", "all_different", 4, 2)

    # Nút tính toán
    calculate_button = create_calculation_button("Tính toán bài đếm số", "calculate_button")
    layout.addWidget(calculate_button, 7, 0, 1, 5)

    return groupbox


### *** Bài toán rút thẻ ***

def create_draw_groupbox():
    groupbox = QGroupBox("Bài Toán Rút Thẻ")
    layout = QGridLayout()
    groupbox.setLayout(layout)

    # SpinBoxes for selecting the start and end card
    layout.addWidget(QLabel("Từ thẻ:"), 0, 0) 
    input_start_at = QSpinBox()
    input_start_at.setRange(1, 999)
    input_start_at.setObjectName("start_at_input")
    layout.addWidget(input_start_at, 0, 1) 

    layout.addWidget(QLabel("Đến thẻ:"), 0, 2)  
    input_end_at = QSpinBox()
    input_end_at.setRange(2, 1000)
    input_end_at.setObjectName("end_at_input")
    layout.addWidget(input_end_at, 0, 3)

    # QLineEdit for entering specific cards
    layout.addWidget(QLabel("Nhập các thẻ (ví dụ: 1,2,...,1000):"), 1, 0) 
    input_cards = QLineEdit()
    input_cards.setObjectName("input_cards")
    layout.addWidget(input_cards, 2, 0, 1, 4)  

    # Create checkbox-input pairs
    create_labeled_checkbox_input(
        layout, "Số thẻ được rút", "checkbox_input_drawn", "input_drawn", 
        "Nhập số thẻ", 3, 0, 3, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Số thẻ chẵn", "checkbox_input_even", "input_even", 
        "Nhập số thẻ", 3, 2, 3, 3
    )
    
    create_labeled_checkbox_input(
        layout, "Tổng chia hết cho", "checkbox_input_sum_divi", "input_sum_divi", 
        "Nhập chữ số", 4, 0, 4, 1
    )
    
    create_labeled_checkbox_input(
        layout, "Tích chia hết cho", "checkbox_input_product_divi", "input_product_divi", 
        "Nhập chữ số", 4, 2, 4, 3
    )

    # Button to perform calculation
    calculate_button1 = create_calculation_button("Tính toán bài rút thẻ", "calculate_button1")
    layout.addWidget(calculate_button1, 5, 0, 1, 4)

    return groupbox


### *** Bài toán vách ngăn ***

def create_partition_groupbox():
    groupbox = QGroupBox("Bài Toán Vách Ngăn")
    layout = QGridLayout(groupbox)

    # Input cho tên các loại
    layout.addWidget(QLabel("Nhập các loại (vd: Nam,Nữ,..):"), 0, 0)
    input_labels = QLineEdit()
    input_labels.setObjectName("input_partition_labels")
    input_labels.setPlaceholderText("Nhập tên các loại")
    layout.addWidget(input_labels, 0, 1, 1, 3)

    # Input cho số lượng các loại
    layout.addWidget(QLabel("Nhập số lượng các loại (vd: 5,22):"), 1, 0)
    input_numbers = QLineEdit()
    input_numbers.setObjectName("input_partition_numbers")
    input_numbers.setPlaceholderText("Nhập số lượng các loại")
    layout.addWidget(input_numbers, 1, 1, 1, 3)

    # Create option checkboxes
    create_checkbox(layout, "Vòng tròn", "checkbox_circle", 2, 0)
    create_checkbox(layout, "Hàng ngang", "checkbox_row", 2, 1)

    # Button layout
    button_layout = QHBoxLayout()
    
    # Calculate button
    calculate_button = create_calculation_button("Tính toán bài toán vách ngăn", "calculate_partition_button")
    button_layout.addWidget(calculate_button)
    
    # Stop button
    stop_button = QPushButton("Dừng tính toán")
    stop_button.setObjectName("stop_partition_button")
    stop_button.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(
                spread:pad, 
                x1:0.034, y1:0.034, 
                x2:0.924, y2:0.920, 
                stop:0 rgba(204, 47, 47, 255), 
                stop:1 rgba(152, 34, 34, 255)
            );
            color: white;
            font-weight: bold;
            border: none;
            padding: 5px;
            border-radius: 5px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: qlineargradient(
                spread:pad, 
                x1:0.034, y1:0.034, 
                x2:0.924, y2:0.920, 
                stop:0 rgba(224, 67, 67, 255), 
                stop:1 rgba(182, 44, 44, 255)
            );
        }
    """)
    button_layout.addWidget(stop_button)
    
    layout.addLayout(button_layout, 3, 0, 1, 4)

    return groupbox