def get_search_styles(colors):
    return f"""
        QLineEdit {{
            background-color: {colors.SURFACE_LIGHT};
            color: {colors.TEXT_PRIMARY};
            border: none;
            border-radius: 20px;
            padding: 8px 35px;
            font-size: 13px;
        }}
        QLineEdit:focus {{
            background-color: {colors.SURFACE};
            border: 1px solid rgba(128, 128, 128, 0.1);
        }}
    """
