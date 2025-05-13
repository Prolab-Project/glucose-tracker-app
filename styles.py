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
            padding: 10px;
            font-size: 16px;
            background-color: #2980b9;
            color: white;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #1abc9c;
        }
        """

    @staticmethod
    def get_modern_card_style():
        return """
        QFrame {
            background-color: white;
            border-radius: 15px;
            border: 1px solid #dcdde1;
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
    def get_modern_button_style(color="#3498db"):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #2980b9;
        }}
        QPushButton:pressed {{
            background-color: #1f618d;
        }}
        """

    @staticmethod
    def get_success_button_style():
        return """
        QPushButton {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 0px;
            font-size: 16px;
            font-weight: bold;
            min-height: 50px;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QPushButton:pressed {
            background-color: #16a085;
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
        }
        QLineEdit:focus {
            border-color: #3498db;
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