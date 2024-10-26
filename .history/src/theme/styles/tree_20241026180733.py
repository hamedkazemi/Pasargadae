def get_tree_styles(colors):
    return f"""
        QTreeWidget {{
            background-color: {colors.SURFACE};
            border: none;
            border-radius: 8px;
            padding: 5px;
            color: {colors.TEXT_PRIMARY};
        }}
        QTreeWidget::item {{
            padding: 4px;
            border-radius: 4px;
            color: {colors.TEXT_PRIMARY};
        }}
        QTreeWidget::item:selected {{
            background: rgba(128, 128, 128, 0.1);
        }}
        QTreeWidget::item:hover {{
            background: rgba(128, 128, 128, 0.05);
        }}
        QTreeWidget::branch {{
            background: transparent;
        }}
    """
