def get_search_styles(colors):
    return f"""
        SearchContainer {{
            background-color: {colors.SURFACE_LIGHT};
            border: none;
            border-radius: 18px;
        }}
        
        SearchContainer:focus-within {{
            background-color: {colors.SURFACE};
            border: 1px solid rgba(128, 128, 128, 0.2);
        }}
        
        SearchBar {{
            background-color: transparent;
            color: {colors.TEXT_PRIMARY};
            border: none;
            padding: 8px 35px;
            font-size: 13px;
        }}
        
        SearchBar::placeholder {{
            color: {colors.TEXT_SECONDARY};
        }}
        
        SearchBar:focus {{
            border: none;
            outline: none;
        }}
        
        SearchBar:hover {{
            background-color: transparent;
        }}
        
        SearchBar::clear-button {{
            image: url(src/assets/icons/close.svg);
        }}
        
        SearchBar::clear-button:hover {{
            image: url(src/assets/icons/close.svg);
        }}
    """
