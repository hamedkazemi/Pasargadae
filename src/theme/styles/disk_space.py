def get_disk_space_styles(colors):
    return f"""
        QWidget#diskSpace {{
            background-color: {colors.SURFACE};
            border-radius: 8px;
            padding: 15px;
        }}
        QLabel#diskTitle {{
            color: {colors.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: bold;
        }}
        QLabel#diskPath {{
            color: {colors.TEXT_SECONDARY};
            font-size: 12px;
        }}
        QPushButton#diskCleaner {{
            background: {colors.GRADIENT_PRIMARY};
            color: white;
            border: none;
            border-radius: 15px;
            padding: 8px 15px;
            font-weight: bold;
        }}
        QPushButton#diskCleaner:hover {{
            background: {colors.GRADIENT_HOVER};
        }}
    """
