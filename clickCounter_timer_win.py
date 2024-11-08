import sys
import csv
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QTextEdit, QFileDialog,
                             QMessageBox)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont
import mouse


class GlobalClickMonitor(QThread):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        # Hook the mouse click event
        mouse.on_click(self.click_handler)
        # Keep the thread running
        while self.running:
            self.msleep(100)  # Sleep to prevent high CPU usage

    def click_handler(self):
        if self.running:
            self.clicked.emit()

    def stop(self):
        self.running = False
        mouse.unhook_all()


class ClickCounter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.seconds = 0
        self.is_counting = False
        self.output_folder = ""

        # Initialize timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Initialize click monitor
        self.click_monitor = GlobalClickMonitor()
        self.click_monitor.clicked.connect(self.increment_counter)

        self.initUI()

        # Start the click monitor thread
        self.click_monitor.start()

        # Check if we're on macOS and show permission instructions if needed
        if sys.platform == 'darwin':
            QTimer.singleShot(500, self.show_mac_instructions)

    def show_mac_instructions(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Accessibility Permissions Required")
        msg.setText("This app needs accessibility permissions to count clicks.")

        instructions = (
            "Please follow these steps for macOS:\n\n"
            "1. Click the Apple menu () in the top-left corner\n"
            "2. Select 'System Settings'\n"
            "3. Click 'Privacy & Security' in the left sidebar\n"
            "4. Scroll down and click 'Accessibility'\n"
            "5. Click the '+' button\n"
            "6. Navigate to and add:\n"
            "   • If using Terminal: Applications → Utilities → Terminal\n"
            "   • If using PyCharm: Applications → PyCharm\n"
            "7. Ensure the checkbox next to the added app is checked\n"
            "8. Restart this application\n\n"
            "The app will continue to run, but click counting won't work "
            "until permissions are granted."
        )

        msg.setInformativeText(instructions)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_windows_instructions(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Running as Administrator Required")
        msg.setText("This app needs to be run as administrator to count global clicks.")

        instructions = (
            "Please follow these steps for Windows:\n\n"
            "1. Right-click on your Python IDE (PyCharm, VS Code, etc.)\n"
            "2. Select 'Run as administrator'\n"
            "3. Run the application again\n\n"
            "The app will continue to run, but click counting might not work "
            "until it's run with administrator privileges."
        )

        msg.setInformativeText(instructions)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    # ... [rest of the previous ClickCounter class implementation remains exactly the same] ...


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont("Helvetica", 10)
    app.setFont(font)

    counter = ClickCounter()
    counter.show()

    # Show Windows-specific instructions if needed
    if sys.platform == 'win32':
        QTimer.singleShot(500, counter.show_windows_instructions)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()