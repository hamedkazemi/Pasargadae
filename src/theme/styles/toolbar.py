def get_toolbar_styles(colors):
    return f"""
        QToolBar {{
            background-color: {colors.SURFACE};
            border: none;
            padding: 5px;
            spacing: 5px;
        }}
        QToolButton {{
            background-color: transparent;
            color: {colors.TEXT_PRIMARY};
            border: none;
            border-radius: 4px;
            padding: 5px;
            icon-size: 20px;
        }}
        QToolButton:hover {{
            background-color: rgba(128, 128, 128, 0.1);
        }}
        QToolButton:pressed {{
            background-color: rgba(128, 128, 128, 0.15);
        }}
    """
