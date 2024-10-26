def get_progress_styles(colors):
    return f"""
        QProgressBar {{
            border: none;
            background-color: rgba(128, 128, 128, 0.1);
            height: 4px;
            border-radius: 2px;
        }}
        QProgressBar::chunk {{
            background: {colors.GRADIENT_PRIMARY};
            border-radius: 2px;
        }}
    """
