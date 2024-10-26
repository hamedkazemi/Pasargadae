def get_tree_styles(colors):
    return f"""
        QTreeWidget {{
            background-color: {colors.SURFACE};
            border: none;
            border-radius: 8px;
            padding: 5px;
            color: {colors.TEXT_PRIMARY};
            outline: none;
            selection-background-color: transparent;
        }}
        QTreeWidget::item {{
            padding: 6px;
            color: {colors.TEXT_PRIMARY};
        }}
        QTreeWidget::item:hover,
        QTreeWidget::item:selected {{
            background: {colors.SURFACE_LIGHT};
        }}

        QTreeWidget::branch {{
            background: transparent;
            padding-left: 5px;
        }}
        QTreeWidget::branch:selected {{
            background: transparent;
        }}
        QTreeWidget::branch:has-children {{
            border-image: none;
            padding-left: 0px;
        }}
    """
