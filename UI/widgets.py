from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QSpinBox
)

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

    # Checkbox và input cho "Có k chữ số"
    checkbox_input_k_digits = QCheckBox("Có k chữ số")
    layout.addWidget(checkbox_input_k_digits, 1, 0)
    input_k_digits = QLineEdit()
    input_k_digits.setObjectName("input_k_digits")
    input_k_digits.setPlaceholderText("Nhập số chữ số")
    input_k_digits.setEnabled(False)
    layout.addWidget(input_k_digits, 1, 1)
    checkbox_input_k_digits.toggled.connect(lambda checked: input_k_digits.setEnabled(checked))
    checkbox_input_k_digits.setObjectName("checkbox_input_k_digits")

    # Checkbox và input cho "Chia hết cho"
    checkbox_divisible_by = QCheckBox("Chia hết cho")
    layout.addWidget(checkbox_divisible_by, 2, 0)
    input_divisible_by = QLineEdit()
    input_divisible_by.setObjectName("divisible_input")
    input_divisible_by.setPlaceholderText("Nhập a,b,c,...")
    input_divisible_by.setEnabled(False)
    layout.addWidget(input_divisible_by, 2, 1)
    checkbox_divisible_by.toggled.connect(lambda checked: input_divisible_by.setEnabled(checked))
    checkbox_divisible_by.setObjectName("checkbox_divisible_by")

    # Checkbox và input cho "Bắt đầu bằng"
    checkbox_starts_by = QCheckBox("Bắt đầu bằng")
    layout.addWidget(checkbox_starts_by, 3, 0)
    input_starts_by = QLineEdit()
    input_starts_by.setObjectName("starts_input")
    input_starts_by.setPlaceholderText("Nhập a,b,c,...")
    input_starts_by.setEnabled(False)
    layout.addWidget(input_starts_by, 3, 1)
    checkbox_starts_by.toggled.connect(lambda checked: input_starts_by.setEnabled(checked))
    checkbox_starts_by.setObjectName("checkbox_starts_by")

    # Checkbox và input cho "Không bắt đầu bằng"
    checkbox_not_starts_by = QCheckBox("Không bắt đầu bằng")
    layout.addWidget(checkbox_not_starts_by, 4, 0)
    input_not_starts_by = QLineEdit()
    input_not_starts_by.setObjectName("not_starts_input")
    input_not_starts_by.setPlaceholderText("Nhập a,b,c,...")
    input_not_starts_by.setEnabled(False)
    layout.addWidget(input_not_starts_by, 4, 1)
    checkbox_not_starts_by.toggled.connect(lambda checked: input_not_starts_by.setEnabled(checked))
    checkbox_not_starts_by.setObjectName("checkbox_not_starts_by")

    # Checkbox và input cho "Không có mặt các chữ số"
    checkbox_not_includes_by = QCheckBox("Không có mặt các chữ số")
    layout.addWidget(checkbox_not_includes_by, 6, 2)
    input_not_includes_by = QLineEdit()
    input_not_includes_by.setObjectName("not_includes_input")
    input_not_includes_by.setPlaceholderText("Nhập a,b,c,...")
    input_not_includes_by.setEnabled(False)
    layout.addWidget(input_not_includes_by, 6, 3)
    checkbox_not_includes_by.toggled.connect(lambda checked: input_not_includes_by.setEnabled(checked))
    checkbox_not_includes_by.setObjectName("checkbox_not_includes_by")

    # Checkbox và input cho "Nhỏ hơn"
    checkbox_ends_by = QCheckBox("Nhỏ hơn")
    layout.addWidget(checkbox_ends_by, 5, 0)
    input_ends_by = QLineEdit()
    input_ends_by.setObjectName("ends_input")
    input_ends_by.setPlaceholderText("Nhập số")
    input_ends_by.setEnabled(False)
    layout.addWidget(input_ends_by, 5, 1)
    checkbox_ends_by.toggled.connect(lambda checked: input_ends_by.setEnabled(checked))
    checkbox_ends_by.setObjectName("checkbox_ends_by")

    # Checkbox và input cho "Lớn hơn"
    checkbox_bigger_than = QCheckBox("Lớn hơn")
    layout.addWidget(checkbox_bigger_than, 5, 2)
    input_bigger_than = QLineEdit()
    input_bigger_than.setObjectName("bigger_than_input")
    input_bigger_than.setPlaceholderText("Nhập số")
    input_bigger_than.setEnabled(False)
    layout.addWidget(input_bigger_than, 5, 3)
    checkbox_bigger_than.toggled.connect(lambda checked: input_bigger_than.setEnabled(checked))
    checkbox_bigger_than.setObjectName("checkbox_bigger_than")

    # Checkbox và input cho "Luôn có mặt các chữ số"
    checkbox_is_k_digits = QCheckBox("Luôn có mặt các chữ số")
    layout.addWidget(checkbox_is_k_digits, 6, 0)
    input_is_k_digits = QLineEdit()
    input_is_k_digits.setObjectName("is_k_digits_input")
    input_is_k_digits.setPlaceholderText("Nhập a,b,c,...")
    input_is_k_digits.setEnabled(False)
    layout.addWidget(input_is_k_digits, 6, 1)
    checkbox_is_k_digits.toggled.connect(lambda checked: input_is_k_digits.setEnabled(checked))
    checkbox_is_k_digits.setObjectName("checkbox_is_k_digits")

    # Checkbox

    # Checkbox thuần
    even_checkbox = QCheckBox("Số chẵn")
    even_checkbox.setObjectName("even_checkbox")
    layout.addWidget(even_checkbox, 1, 2)

    palindrome_checkbox = QCheckBox("Số đối xứng")
    palindrome_checkbox.setObjectName("palindrome_checkbox")
    layout.addWidget(palindrome_checkbox, 2, 2)

    odd_checkbox = QCheckBox("Số lẻ")
    odd_checkbox.setObjectName("odd_checkbox")
    layout.addWidget(odd_checkbox, 1, 3)

    prime_checkbox = QCheckBox("Số nguyên tố")
    prime_checkbox.setObjectName("prime_checkbox")
    layout.addWidget(prime_checkbox, 2, 3)

    square_checkbox = QCheckBox("Số chính phương")
    square_checkbox.setObjectName("square_checkbox")
    layout.addWidget(square_checkbox, 3, 2)

    cube_checkbox = QCheckBox("Số lập phương")
    cube_checkbox.setObjectName("cube_checkbox")
    layout.addWidget(cube_checkbox, 3, 3)

    all_diff_checkbox = QCheckBox("Chữ số khác nhau")
    all_diff_checkbox.setObjectName("all_different")
    layout.addWidget(all_diff_checkbox, 4, 2)

    # Nút tính toán
    calculate_button = QPushButton("Tính toán bài đếm số")
    calculate_button.setObjectName("calculate_button")  # Đặt tên đối tượng cho nút này
    calculate_button.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(
                spread:pad, 
                x1:0.034, y1:0.034, 
                x2:0.924, y2:0.920, 
                stop:0 rgba(47, 204, 113, 255), 
                stop:1 rgba(34, 152, 83, 255)
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
                stop:0 rgba(67, 224, 133, 255), 
                stop:1 rgba(44, 182, 113, 255)
            );
        }
    """)

    layout.addWidget(calculate_button, 7, 0, 1, 5)
    print("start")

    return groupbox


# ---------------------------------------------------------

# Assuming the same pattern for create_draw_groupbox and create_result_display
# Continue to define them similarly with proper QObject names

### *** Bài toán rút thẻ ***

def create_draw_groupbox():
    groupbox = QGroupBox("Bài Toán Rút Thẻ")
    layout = QGridLayout()

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

    # Checkboxes for conditions
    checkbox_drawn = QCheckBox("Số thẻ được rút")
    layout.addWidget(checkbox_drawn, 3, 0)
    input_drawn = QLineEdit()
    input_drawn.setObjectName("input_drawn")
    input_drawn.setPlaceholderText("Nhập số thẻ")
    input_drawn.setEnabled(False)
    layout.addWidget(input_drawn, 3, 1)
    checkbox_drawn.toggled.connect(lambda checked: input_drawn.setEnabled(checked))
    checkbox_drawn.setObjectName("checkbox_input_drawn")

    checkbox_even = QCheckBox("Số thẻ chẵn")
    layout.addWidget(checkbox_even, 3, 2)
    input_even = QLineEdit()
    input_even.setObjectName("input_even")
    input_even.setPlaceholderText("Nhập số thẻ")
    input_even.setEnabled(False)
    layout.addWidget(input_even, 3, 3)
    checkbox_even.toggled.connect(lambda checked: input_even.setEnabled(checked))
    checkbox_even.setObjectName("checkbox_input_even")
    
    checkbox_sum_divisible = QCheckBox("Tổng chia hết cho")
    layout.addWidget(checkbox_sum_divisible, 4, 0)
    input_sum_divi = QLineEdit()
    input_sum_divi.setObjectName("input_sum_divi")
    input_sum_divi.setPlaceholderText("Nhập chữ số")
    input_sum_divi.setEnabled(False)
    layout.addWidget(input_sum_divi, 4, 1)
    checkbox_sum_divisible.toggled.connect(lambda checked: input_sum_divi.setEnabled(checked))
    checkbox_sum_divisible.setObjectName("checkbox_input_sum_divi")  

    checkbox_product_divisible = QCheckBox("Tích chia hết cho")
    layout.addWidget(checkbox_product_divisible, 4, 2)
    input_product_divi = QLineEdit()
    input_product_divi.setObjectName("input_product_divi")
    input_product_divi.setPlaceholderText("Nhập chữ số")
    input_product_divi.setEnabled(False)
    layout.addWidget(input_product_divi, 4, 3)
    checkbox_product_divisible.toggled.connect(lambda checked: input_product_divi.setEnabled(checked))
    checkbox_product_divisible.setObjectName("checkbox_input_product_divi") 

    # Button to perform calculation
    calculate_button1 = QPushButton("Tính toán bài rút thẻ")
    calculate_button1.setObjectName("calculate_button1")
    calculate_button1.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(
                spread:pad, 
                x1:0.034, y1:0.034, 
                x2:0.924, y2:0.920, 
                stop:0 rgba(47, 204, 113, 255), 
                stop:1 rgba(34, 152, 83, 255)
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
                stop:0 rgba(67, 224, 133, 255), 
                stop:1 rgba(44, 182, 113, 255)
            );
        }
    """)
    layout.addWidget(calculate_button1, 5, 0, 1, 4)  

    groupbox.setLayout(layout)
    return groupbox

# def create_student_groupbox():
#     groupbox = QGroupBox("Bài Toán Học Sinh")
#     layout = QGridLayout()

#     # SpinBoxes for selecting the start and end card
#     layout.addWidget(QLabel("Nam:"), 0, 0) 
#     input_man = QSpinBox()
#     input_man.setRange(0, 1000)
#     input_man.setObjectName("man_input")
#     layout.addWidget(input_man, 0, 1) 

#     layout.addWidget(QLabel("Nữ:"), 0, 2)  
#     input_woman = QSpinBox()
#     input_woman.setRange(0, 1000)
#     input_woman.setObjectName("woman_input")
#     layout.addWidget(input_woman, 0, 3)

#     # Checkboxes for conditions
#     checkbox_inline = QCheckBox("Bàn thẳng")
#     layout.addWidget(checkbox_inline, 2, 0)
#     checkbox_inline.setObjectName("checkbox__inline")

#     checkbox_circle = QCheckBox("Bàn tròn")
#     layout.addWidget(checkbox_circle, 2, 2)
#     checkbox_circle.setObjectName("checkbox_input_even")
    
#     checkbox_man_toge = QCheckBox("Có k nam cạnh nhau")
#     layout.addWidget(checkbox_man_toge, 3, 0)
#     input_man_toge = QLineEdit()
#     input_man_toge.setObjectName("input_sum_divi")
#     input_man_toge.setPlaceholderText("Nhập chữ số")
#     input_man_toge.setEnabled(False)
#     layout.addWidget(input_man_toge, 3, 1)
#     checkbox_man_toge.toggled.connect(lambda checked: input_man_toge.setEnabled(checked))
#     checkbox_man_toge.setObjectName("checkbox_input_man_toge")  

#     checkbox_woman_toge = QCheckBox("Có k nữ cạnh nhau")
#     layout.addWidget(checkbox_woman_toge, 3, 2)
#     input_woman_toge = QLineEdit()
#     input_woman_toge.setObjectName("input_sum_divi")
#     input_woman_toge.setPlaceholderText("Nhập chữ số")
#     input_woman_toge.setEnabled(False)
#     layout.addWidget(input_woman_toge, 3, 3)
#     checkbox_woman_toge.toggled.connect(lambda checked: input_woman_toge.setEnabled(checked))
#     checkbox_woman_toge.setObjectName("checkbox_input_woman_toge")

#     # Button to perform calculation
#     calculate_button2 = QPushButton("Tính toán bài học sinh")
#     calculate_button2.setObjectName("calculate_button2")
#     calculate_button2.setStyleSheet("""
#         QPushButton {
#             background-color: qlineargradient(
#                 spread:pad, 
#                 x1:0.034, y1:0.034, 
#                 x2:0.924, y2:0.920, 
#                 stop:0 rgba(47, 204, 113, 255), 
#                 stop:1 rgba(34, 152, 83, 255)
#             );
#             color: white;
#             font-weight: bold;
#             border: none;
#             padding: 5px;
#             border-radius: 5px;
#             font-size: 12px;
#         }
#         QPushButton:hover {
#             background-color: qlineargradient(
#                 spread:pad, 
#                 x1:0.034, y1:0.034, 
#                 x2:0.924, y2:0.920, 
#                 stop:0 rgba(67, 224, 133, 255), 
#                 stop:1 rgba(44, 182, 113, 255)
#             );
#         }
#     """)
#     layout.addWidget(calculate_button2, 5, 0, 1, 4)  

#     groupbox.setLayout(layout)
#     return groupbox
