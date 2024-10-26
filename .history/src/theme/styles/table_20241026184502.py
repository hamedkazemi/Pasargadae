def get_table_styles(colors):
    return f"""
        QTableWidget {{
            background-color: {colors.SURFACE};
            border: none;
            border-radius: 8px;
            gridline-color: transparent;
            color: {colors.TEXT_PRIMARY};
        }}
        QTableWidget::item {{
            padding: 8px;
            border-radius: 4px;
            color: {colors.TEXT_PRIMARY};
        }}
        QTableWidget::item:selected {{
            background: rgba(128, 128, 128, 0.05);
        }}
        QHeaderView::section {{
            background-color: {colors.SURFACE};
            color: {colors.TEXT_SECONDARY};
            padding: 8px;
            border: none;
            font-size: 12px;
        }}
        QHeaderView::section:hover {{
            background-color: rgba(128, 128, 128, 0.1);
        }}
        QHeaderView::up-arrow {{
            image: url(src/assets/icons/sort_up.svg);
            width: 10px;
            height: 10px;
            margin-left: 5px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QHeaderView::down-arrow {{
            image: url(src/assets/icons/sort_down.svg);
            width: 10px;
            height: 10px;
            margin-left: 5px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QTableWidget QCheckBox {{
            padding: 6px;
        }}
        QTableWidget QProgressBar {{
            border: none;
            background-color: rgba(128, 128, 128, 0.1);
            height: 4px;
            border-radius: 2px;
        }}
        QTableWidget QProgressBar::chunk {{
            background: {colors.GRADIENT_PRIMARY};
            border-radius: 2px;
        }}
    """
