def get_search_styles(colors):
    return f"""
        #search_container {{
            border: none;
            border-radius: 18px;
            min-height: 36px;
            max-height: 36px;
        }}
        
        #search_container:focus-within {{
            border: 1px solid rgba(128, 128, 128, 0.1);
        }}
        
        QLineEdit {{
            background-color: transparent;
            color: {colors.TEXT_PRIMARY};
            border: none;
            padding: 8px 35px;
            font-size: 13px;
            min-height: 36px;
            max-height: 36px;
        }}
    """
