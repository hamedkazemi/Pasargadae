def get_tree_styles(colors):
    return f"""
        QTreeWidget {{
            background-color: {colors.SURFACE};
            border: none;
            border-radius: 8px;
            padding: 5px;
            color: {colors.TEXT_PRIMARY};
            outline: none;
        }}
        QTreeWidget::item {{
            padding: 6px;
            border-radius: 4px;
            color: {colors.TEXT_PRIMARY};
        }}
        QTreeWidget::item:selected {{
            background: rgba(255, 255, 255, 0.1);
        }}
        QTreeWidget::item:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}
        QTreeWidget::branch:has-children:!has-siblings:closed,
        QTreeWidget::branch:closed:has-children:has-siblings {{
            image: url(src/assets/icons/chevron_right.svg);
        }}
        QTreeWidget::branch:open:has-children:!has-siblings,
        QTreeWidget::branch:open:has-children:has-siblings {{
            image: url(src/assets/icons/chevron_down.svg);
        }}
        QTreeWidget::branch:!has-children {{
            border: none;
            background: none;
        }}
        QTreeWidget::branch {{
            background: transparent;
            padding-left: 5px;
        }}
        QTreeWidget::branch:selected {{
            background: transparent;
        }}
    """
