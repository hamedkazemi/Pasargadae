def get_scrollbar_styles(colors):
    return f"""
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {colors.TEXT_SECONDARY};
            min-height: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {colors.PRIMARY};
        }}
        QScrollBar::add-line:vertical {{
            height: 0px;
        }}
        QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: transparent;
            height: 8px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {colors.TEXT_SECONDARY};
            min-width: 30px;
            border-radius: 4px;
            margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {colors.PRIMARY};
        }}
        QScrollBar::add-line:horizontal {{
            width: 0px;
        }}
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
    """
