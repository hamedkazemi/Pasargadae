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
            border-radius: 4px;
            color: {colors.TEXT_PRIMARY};
            padding-top: 6px;
            padding-bottom: 6px;
            padding-right: 6px;
            margin: 0px;
        }}

        QTreeWidget::item::first{{
            background: {colors.SURFACE_LIGHT};
        }}

        QTreeWidget::item:hover,
        QTreeWidget::item:selected {{
            background: {colors.SURFACE_LIGHT};
        }}
        QTreeWidget::branch {{
            background: transparent;
        }
}
        QTreeWidget::branch:selected {{
            background: transparent;
        }}
        QTreeWidget::branch:has-children {{
            border-image: none;
            image: none;
            padding: 0px;
        }}
    """
