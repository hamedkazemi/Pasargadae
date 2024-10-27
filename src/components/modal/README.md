# Modal Window Component

A reusable modal window component that provides a frameless, draggable dialog with customizable content and action buttons.

## Features

- Frameless window with custom styling
- Draggable by title bar
- Customizable title
- Configurable size
- Support for action buttons
- Theme-aware (supports both light and dark themes)
- Custom content area

## Usage

### Basic Usage

```python
from components.modal.modal_window import ModalWindow
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

# Create a custom modal
class MyModal(ModalWindow):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            title="My Modal",
            width=400,
            height=300
        )
        
        # Create content
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.addWidget(QLabel("Your content here"))
        
        # Set the content
        self.set_content(content)
        
        # Add action buttons
        self.add_action_button("Cancel", self.close)
        self.add_action_button("Confirm", self.on_confirm, primary=True)
    
    def on_confirm(self):
        # Handle confirmation
        self.close()

# Show the modal
modal = MyModal(parent_widget)
modal.exec()
```

### API Reference

#### ModalWindow

Main modal window class that provides the base functionality.

**Constructor Parameters:**
- `parent`: Parent widget (optional)
- `title`: Modal window title (default: "")
- `width`: Modal width in pixels (default: 400)
- `height`: Modal height in pixels (default: 300)

**Methods:**
- `set_content(widget)`: Set the main content widget
- `add_action_button(text, callback, primary=False)`: Add an action button
- `update_theme(is_dark)`: Update the modal's theme

## Styling

The modal automatically adapts to the application's theme (light/dark). You can customize the appearance by subclassing and overriding the `update_style` method.
