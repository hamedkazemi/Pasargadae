def get_search_styles(colors):
    return {
        "SEARCH_CONTAINER": f"""
            QWidget {{
                background-color: {colors.SURFACE_LIGHT};
                border: none;
                border-radius: 20px;
            }}
            QWidget:focus-within {{
                background-color: {colors.SURFACE};
                border: 1px solid rgba(128, 128, 128, 0.1);
            }}
        """,
        "SEARCH": f"""
            QLineEdit {{
                background-color: transparent;
                color: {colors.TEXT_PRIMARY};
                border: none;
                padding: 8px 35px;
                font-size: 13px;
            }}
        """
    }
