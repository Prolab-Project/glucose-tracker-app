class Styles:
    @staticmethod
    def get_input_style():
        return """
        QLineEdit {
            padding: 12px;
            border: 2px solid #2980b9;
            border-radius: 10px;
            font-size: 16px;
            background-color: #fdfefe;
        }
        QLineEdit:focus {
            border-color: #1abc9c;
        }
        """

    @staticmethod
    def get_button_style():
        return """
        QPushButton {
            padding: 12px;
            font-size: 16px;
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2980b9);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
        }
        QPushButton:pressed {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #27ae60, stop:1 #2ecc71);
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
        """

    @staticmethod
    def get_modern_card_style():
        return """
        QFrame {
            background-color: white;
            border-radius: 15px;
            border: 1px solid #dcdde1;
            padding: 20px;
        }
        """

    @staticmethod
    def get_inner_card_style():
        return """
        QFrame {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #eaeaea;
            margin: 10px 5px;
        }
        """

    @staticmethod
    def get_title_style():
        return """
        font-size: 24px; 
        font-weight: bold; 
        color: #2c3e50; 
        margin-bottom: 10px;
        """

    @staticmethod
    def get_subtitle_style():
        return """
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
        """

    @staticmethod
    def get_modern_button_style(color="#3498db", text_color="white"):
        return f"""
        QPushButton {{
            background-color: {color};
            color: {text_color};
            border: none;
            border-radius: 8px;
            padding: 12px 15px;
            font-size: 14px;
            font-weight: bold;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {color}, stop:1 #2980b9);
        }}
        QPushButton:pressed {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2980b9, stop:1 {color});
        }}
        QPushButton:disabled {{
            background-color: #bdc3c7;
            color: #7f8c8d;
        }}
        """

    @staticmethod
    def get_success_button_style():
        return """
        QPushButton {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 0px;
            font-size: 16px;
            font-weight: bold;
            min-height: 50px;
        }
        QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #27ae60, stop:1 #2ecc71);
        }
        QPushButton:pressed {
            background-color: #16a085;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
        """

    @staticmethod
    def get_modern_input_style():
        return """
        QLineEdit {
            border: 2px solid #dfe4ea;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            font-size: 14px;
            min-height: 20px;
        }
        QLineEdit:focus {
            border-color: #3498db;
            background-color: #ecf0f1;
        }
        """

    @staticmethod
    def get_modern_spinbox_style():
        return """
        QSpinBox {
            border: 2px solid #dfe4ea;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            font-size: 18px;
            color: #e74c3c;
            font-weight: bold;
            min-height: 40px;
        }
        QSpinBox:focus {
            border-color: #3498db;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            width: 25px;
            border-radius: 4px;
            background-color: #ecf0f1;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #bdc3c7;
        }
        """

    @staticmethod
    def get_modern_combobox_style():
        return """
        QComboBox {
            border: 2px solid #dfe4ea;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            font-size: 14px;
            min-height: 40px;
        }
        QComboBox:hover {
            border-color: #3498db;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left: 1px solid #dfe4ea;
        }
        """

    @staticmethod
    def get_modern_dateedit_style():
        return """
        QDateEdit {
            border: 2px solid #dfe4ea;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            font-size: 14px;
            min-height: 40px;
        }
        QDateEdit:hover {
            border-color: #3498db;
        }
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left: 1px solid #dfe4ea;
        }
        """

    @staticmethod
    def get_modern_timeedit_style():
        return """
        QTimeEdit {
            border: 2px solid #dfe4ea;
            border-radius: 8px;
            padding: 10px;
            background-color: white;
            font-size: 14px;
            min-height: 40px;
        }
        QTimeEdit:hover {
            border-color: #3498db;
        }
        QTimeEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left: 1px solid #dfe4ea;
        }
        """

    @staticmethod
    def get_label_style(color="#34495e", size=14):
        return f"""
        color: {color};
        font-size: {size}px;
        """

    @staticmethod
    def get_modern_profile_image_style():
        return """
        border: 3px solid #3498db;
        border-radius: 75px;
        background-color: #f0f0f0;
        """

    @staticmethod
    def get_shadow_style():
        return """
        QFrame, QPushButton {
            border: none;
        }
        """

    @staticmethod
    def get_modern_list_style():
        return """
        QListWidget {
            border: 1px solid #dfe4ea;
            border-radius: 10px;
            background-color: white;
            font-size: 16px;
            padding: 10px;
            outline: none;
        }
        QListWidget::item {
            border-bottom: 1px solid #f1f2f6;
            padding: 10px;
            border-radius: 5px;
        }
        QListWidget::item:selected {
            background-color: #ecf0f1;
            color: #2c3e50;
            border-left: 3px solid #3498db;
        }
        QListWidget::item:hover {
            background-color: #f5f6fa;
        }
        """
        
    @staticmethod
    def get_doctor_panel_style():
        return """
        QWidget {
            background-color: #f5f6fa;
        }
        QLabel {
            color: #2c3e50;
        }
        QPushButton {
            padding: 12px;
            font-size: 15px;
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2980b9);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
        }
        QPushButton:pressed {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #27ae60, stop:1 #2ecc71);
        }
        QFrame {
            background-color: white;
            border-radius: 15px;
            border: 1px solid #dcdde1;
        }
        """ 