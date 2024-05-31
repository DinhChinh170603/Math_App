from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout
)

def create_count_groupbox():
    groupbox = QGroupBox("Bài Toán Đếm Số")
    layout = QGridLayout(groupbox)

    # Nhập chuỗi chữ số
    layout.addWidget(QLabel("Nhập chuỗi chữ số (ví dụ: 0,1,2,3,...):"), 0, 0)
    input_numbers = QLineEdit()
    input_numbers.setObjectName("input_numbers")
    layout.addWidget(input_numbers, 0, 1, 1, 2)

    # Checkbox và input cho "Có k chữ số"
    layout.addWidget(QLabel("Có k chữ số"))
    input_k_digits = QLineEdit()
    input_k_digits.setObjectName("input_k_digits")
    input_k_digits.setPlaceholderText("Nhập số chữ số")
    layout.addWidget(input_k_digits, 1, 1)

    # Checkbox và input cho "Chia hết cho"
    checkbox_divisible_by = QCheckBox("Chia hết cho")
    layout.addWidget(checkbox_divisible_by, 2, 0)
    input_divisible_by = QLineEdit()
    input_divisible_by.setObjectName("divisible_input")
    input_divisible_by.setPlaceholderText("Nhập số chia hết")
    input_divisible_by.setVisible(False)
    layout.addWidget(input_divisible_by, 2, 1)
    checkbox_divisible_by.toggled.connect(lambda checked: input_divisible_by.setVisible(checked))
    checkbox_divisible_by.setObjectName("checkbox_divisible_by")

    # Nút tính toán
    calculate_button = QPushButton("Tính toán bài đếm số")
    calculate_button.setObjectName("calculate_button")  # Đặt tên đối tượng cho nút này

    layout.addWidget(calculate_button, 3, 0, 1, 2)

    return groupbox


# ---------------------------------------------------------

# from PyQt6.QtWidgets import (
#     QGroupBox, QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QSpinBox
# )

# def create_count_groupbox():
#     groupbox = QGroupBox("Bài Toán Đếm Số")
#     layout = QGridLayout()

#     # Input 1
#     layout.addWidget(QLabel("Nhập chuỗi chữ số (ví dụ: 0,1,2,3,4,5):"), 0, 0)
#     input1_edit = QLineEdit()
#     input1_edit.setObjectName("input1_edit")
#     layout.addWidget(input1_edit, 0, 1, 1, 2)

#     # Checkboxes 1
#     checkbox1_1 = QCheckBox("Có k chữ số")
#     checkbox1_1.setObjectName("checkbox1_1")
#     layout.addWidget(checkbox1_1, 1, 0)

#     checkbox1_2 = QCheckBox("Chia hết cho")
#     checkbox1_2.setObjectName("checkbox_divisible_by")
#     layout.addWidget(checkbox1_2, 1, 1)
#     divisible_input = QLineEdit()
#     divisible_input.setObjectName("divisible_input")
#     divisible_input.setPlaceholderText("Nhập số để chia hết")
#     divisible_input.setVisible(False)  # Mặc định ẩn
#     layout.addWidget(divisible_input, 1, 2)

#     # Kết nối checkbox với hàm xử lý để hiển thị hoặc ẩn trường nhập liệu
#     checkbox1_2.toggled.connect(lambda checked: divisible_input.setVisible(checked))

    # checkbox1_3 = QCheckBox("Bắt đầu bằng")
    # checkbox1_3.setObjectName("checkbox1_3")
    # layout.addWidget(checkbox1_3, 1, 2)

    # # Additional checkboxes
    # checkbox1_4 = QCheckBox("Không bắt đầu bằng")
    # checkbox1_4.setObjectName("checkbox1_4")
    # layout.addWidget(checkbox1_4, 2, 0)
    # checkbox1_5 = QCheckBox("Nhỏ hơn")
    # checkbox1_5.setObjectName("checkbox1_5")
    # layout.addWidget(checkbox1_5, 2, 1)
    # checkbox1_6 = QCheckBox("Luôn có mặt các chữ số")
    # checkbox1_6.setObjectName("checkbox1_6")
    # layout.addWidget(checkbox1_6, 2, 2)

    # # Input 2

    # # Additional Inputs
    # input3_edit = QLineEdit()
    # input3_edit.setObjectName("input3_edit")
    # layout.addWidget(QLabel("Nhập ab"), 4, 0)
    # layout.addWidget(input3_edit, 4, 1, 1, 2)

    # input4_edit = QLineEdit()
    # input4_edit.setObjectName("input4_edit")
    # layout.addWidget(QLabel("Nhập ab"), 5, 0)
    # layout.addWidget(input4_edit, 5, 1, 1, 2)

    # input5_edit = QLineEdit()
    # input5_edit.setObjectName("input5_edit")
    # layout.addWidget(QLabel("Nhập a,b"), 6, 0)
    # layout.addWidget(input5_edit, 6, 1, 1, 2)

    # Button to perform calculation
    # button1 = QPushButton("Tính toán bài đếm số")
    # button1.setObjectName("calculate_count_button")
    # layout.addWidget(button1, 7, 0, 1, 3)

    # groupbox.setLayout(layout)
    # return groupbox

# Assuming the same pattern for create_draw_groupbox and create_result_display
# Continue to define them similarly with proper QObject names


# def create_draw_groupbox():
#     groupbox = QGroupBox("Bài Toán Rút Thẻ")
#     layout = QGridLayout()

#     # Input fields for the draw problem
#     input6_spinbox = QSpinBox()
#     layout.addWidget(QLabel("Từ thẻ:"), 0, 0)
#     layout.addWidget(input6_spinbox, 0, 1)

#     input7_spinbox = QSpinBox()
#     layout.addWidget(QLabel("Đến thẻ:"), 1, 0)
#     layout.addWidget(input7_spinbox, 1, 1)

#     input8_edit = QLineEdit()
#     layout.addWidget(QLabel("Nhập các thẻ (ví dụ: 1,2,...,17):"), 2, 0)
#     layout.addWidget(input8_edit, 2, 1, 1, 2)

#     # Checkboxes for conditions
#     checkbox3_1 = QCheckBox("Số thẻ được rút")
#     layout.addWidget(checkbox3_1, 3, 0)
#     checkbox3_2 = QCheckBox("Tổng chia hết cho")
#     layout.addWidget(checkbox3_2, 3, 1)
#     checkbox3_3 = QCheckBox("Số thẻ chẵn")
#     layout.addWidget(checkbox3_3, 3, 2)
#     checkbox3_4 = QCheckBox("Tích chia hết cho")
#     layout.addWidget(checkbox3_4, 4, 0)

#     # Button to perform calculation
#     button2 = QPushButton("Tính toán bài rút thẻ")
#     layout.addWidget(button2, 5, 0, 1, 3)

#     groupbox.setLayout(layout)
#     return groupbox

# def create_result_display(self):
#     layout = QHBoxLayout()
#     result_label = QLabel("Số lượng số thỏa mãn: ")
#     self.result_output = QLineEdit()  # Lưu như một thuộc tính của lớp
#     self.result_output.setObjectName("result_output")
#     self.result_output.setReadOnly(True)
#     layout.addWidget(result_label)
#     layout.addWidget(self.result_output)
#     return layout
