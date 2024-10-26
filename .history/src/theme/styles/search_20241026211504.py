def get_search_styles(colors):
    return f"""
        /* Container styles */
        #search_container {{
            background-color: {colors.SURFACE};
            border: none;
            border-radius: 20px;
        }}
        #search_container:focus-within {{
            background-color: {colors.SURFACE};
            border: 1px solid rgba(128, 128, 128, 0.1);
        }}
        
        /* Search bar styles */
        QLineEdit {{
            background-color: transparent;
            color: {colors.TEXT_PRIMARY};
            border: none;
            padding: 8px 35px;
            font-size: 13px;
        }}
    """
