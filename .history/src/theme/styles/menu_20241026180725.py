def get_menu_styles(colors):
    return f"""
        QMenuBar {{
            background-color: {colors.SURFACE};
            color: {colors.TEXT_PRIMARY};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 2px 10px;
            spacing: 5px;
        }}
        QMenuBar::item {{
            padding: 5px 10px;
            border-radius: 4px;
        }}
        QMenuBar::item:selected {{
            background-color: rgba(128, 128, 128, 0.1);
        }}
        QMenu {{
            background-color: {colors.SURFACE};
            color: {colors.TEXT_PRIMARY};
            border: 1px solid {colors.SURFACE_LIGHT};
            border-radius: 4px;
            padding: 5px;
        }}
        QMenu::item {{
            padding: 5px 30px 5px 20px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: rgba(128, 128, 128, 0.1);
        }}
    """