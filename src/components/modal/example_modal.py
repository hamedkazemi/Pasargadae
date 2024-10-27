from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .modal_window import ModalWindow

class ExampleModal(ModalWindow):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title="Example Modal",
            width=400,
            height=300
        )
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.addWidget(QLabel("This is an example modal content."))
        
        # Set the content
        self.set_content(content)
        
        # Add action buttons
        self.add_action_button("Cancel", self.close)
        self.add_action_button("Confirm", self.on_confirm, primary=True)
    
    def on_confirm(self):
        # Handle confirm action
        print("Confirmed!")
        self.close()
