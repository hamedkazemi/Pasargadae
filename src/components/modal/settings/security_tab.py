from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCheckBox, QLineEdit,
    QPushButton, QDialog, QTextEdit,
    QMessageBox
)
import subprocess
import shlex
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class CommandTestDialog(QDialog):
    def __init__(self, command: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Command Test Result")
        self.setMinimumSize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Command display
        cmd_label = QLabel("Executing command:")
        layout.addWidget(cmd_label)
        
        cmd_display = QLineEdit(command)
        cmd_display.setReadOnly(True)
        layout.addWidget(cmd_display)
        
        # Output display
        output_label = QLabel("Output:")
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        # Run the command
        try:
            args = shlex.split(command)
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=10)
            
            if stdout:
                self.output_text.append("Output:\n" + stdout)
            if stderr:
                self.output_text.append("\nErrors:\n" + stderr)
            
            if process.returncode == 0:
                self.output_text.append("\nCommand executed successfully.")
            else:
                self.output_text.append(f"\nCommand failed with return code {process.returncode}")
                
        except subprocess.TimeoutExpired:
            self.output_text.append("Error: Command timed out after 10 seconds")
        except Exception as e:
            self.output_text.append(f"Error executing command: {str(e)}")

class CommandWidget(QWidget):
    def __init__(self, initial_command: str = "", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.command_edit = QLineEdit(initial_command)
        self.command_edit.setPlaceholderText("Enter command to execute")
        
        test_btn = QPushButton()
        test_btn.setIcon(IconProvider.get_icon("check"))
        test_btn.setFixedSize(28, 28)
        test_btn.clicked.connect(self.test_command)
        
        layout.addWidget(self.command_edit)
        layout.addWidget(test_btn)
    
    def test_command(self):
        command = self.command_edit.text().strip()
        if not command:
            QMessageBox.warning(
                self,
                "Invalid Command",
                "Please enter a command to test."
            )
            return
        
        dialog = CommandTestDialog(command, self)
        dialog.exec()
    
    def get_command(self) -> str:
        return self.command_edit.text()

class SecurityTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "security", parent)
    
    def _setup_ui(self):
        # Antivirus Section
        antivirus_section = self.add_section("Antivirus Integration")
        
        self.av_enabled = QCheckBox()
        self.av_enabled.setChecked(
            self.get_nested_setting("antivirus_scanning", default=True)
        )
        self.add_field(
            antivirus_section,
            "Enable Scanning:",
            self.av_enabled,
            "Automatically scan downloaded files for viruses"
        )
        
        # Custom Commands Section
        commands_section = self.add_section("Custom Commands")
        
        # Help text
        help_text = QLabel(
            "Enter commands to execute on downloaded files.\n"
            "Use {file} as a placeholder for the file path.\n"
            "Example: clamscan {file} --database=/path/to/db"
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: gray;")
        commands_section.addWidget(help_text)
        
        # Pre-scan command
        self.pre_scan = CommandWidget(
            self.get_nested_setting("pre_scan_command", default="")
        )
        self.add_field(
            commands_section,
            "Pre-Download Scan:",
            self.pre_scan,
            "Command to run before starting download"
        )
        
        # Post-scan command
        self.post_scan = CommandWidget(
            self.get_nested_setting("post_scan_command", default="")
        )
        self.add_field(
            commands_section,
            "Post-Download Scan:",
            self.post_scan,
            "Command to run after download completes"
        )
        
        # Custom scan command
        self.custom_scan = CommandWidget(
            self.get_nested_setting("custom_commands", default="")
        )
        self.add_field(
            commands_section,
            "Custom Command:",
            self.custom_scan,
            "Additional custom command to execute"
        )
        
        # Update enabled states
        self.av_enabled.stateChanged.connect(self.update_commands_enabled)
        self.update_commands_enabled(self.av_enabled.isChecked())
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
            }
            
            QLineEdit {
                padding: 4px;
                border: 1px solid palette(mid);
                border-radius: 4px;
            }
            
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.1);
            }
            
            QCheckBox {
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
    
    def update_commands_enabled(self, enabled: bool):
        self.pre_scan.setEnabled(enabled)
        self.post_scan.setEnabled(enabled)
        self.custom_scan.setEnabled(enabled)
    
    def save_settings(self):
        self.set_nested_setting(self.av_enabled.isChecked(), "antivirus_scanning")
        self.set_nested_setting(self.pre_scan.get_command(), "pre_scan_command")
        self.set_nested_setting(self.post_scan.get_command(), "post_scan_command")
        self.set_nested_setting(self.custom_scan.get_command(), "custom_commands")
