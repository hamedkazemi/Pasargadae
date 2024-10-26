def get_window_styles(colors):
    return f"""
        QMainWindow {{
            background-color: {colors.BACKGROUND};
            color: {colors.TEXT_PRIMARY};
            border-radius: 10px;
        }}
        QWidget#centralWidget {{
            background-color: {colors.BACKGROUND};
            border-radius: 10px;
        }}
        QLabel {{
            color: {colors.TEXT_PRIMARY};
        }}
    """
