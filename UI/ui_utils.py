from PyQt6.QtWidgets import QLineEdit, QCheckBox, QPushButton, QLabel

def create_labeled_checkbox_input(layout, label_text, checkbox_name, input_name, placeholder_text, row, col, input_row, input_col):
    """Create a checkbox with a linked input field that is enabled/disabled based on checkbox state"""
    checkbox = QCheckBox(label_text)
    checkbox.setObjectName(checkbox_name)
    layout.addWidget(checkbox, row, col)
    
    input_field = QLineEdit()
    input_field.setObjectName(input_name)
    input_field.setPlaceholderText(placeholder_text)
    input_field.setEnabled(False)
    layout.addWidget(input_field, input_row, input_col)
    
    checkbox.toggled.connect(lambda checked: input_field.setEnabled(checked))
    
    return checkbox, input_field

def create_checkbox(layout, label_text, object_name, row, col):
    """Create a simple checkbox"""
    checkbox = QCheckBox(label_text)
    checkbox.setObjectName(object_name)
    layout.addWidget(checkbox, row, col)
    return checkbox

def create_calculation_button(text, object_name):
    """Create a styled calculation button"""
    button = QPushButton(text)
    button.setObjectName(object_name)
    button.setStyleSheet("""
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
    return button

def create_progress_button(text, object_name):
    """Create a styled progress calculation button"""
    button = QPushButton(text)
    button.setObjectName(object_name)
    button.setStyleSheet("""
        QPushButton {
            background-color: qlineargradient(
                spread:pad, 
                x1:0.034, y1:0.034, 
                x2:0.924, y2:0.920, 
                stop:0 rgba(41, 128, 185, 255), 
                stop:1 rgba(52, 152, 219, 255)
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
                stop:0 rgba(52, 152, 219, 255), 
                stop:1 rgba(41, 128, 185, 255)
            );
        }
        QPushButton:disabled {
            background-color: gray;
        }
    """)
    return button
