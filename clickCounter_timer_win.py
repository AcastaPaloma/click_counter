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
        mouse.on_click(self.click_handler)
        while self.running:
            self.msleep(100)  

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.click_monitor = GlobalClickMonitor()
        self.click_monitor.clicked.connect(self.increment_counter)

        self.initUI()

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

    def update_timer(self):
        self.seconds += 1
        self.timer_label.setText(f"Elapsed Time: {self.seconds} seconds")

    def increment_counter(self):
        self.click_count += 1
        self.click_count_label.setText(f"Click Count: {self.click_count}")

    def initUI(self):
        self.setWindowTitle("Click Counter")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.timer_label = QLabel("Elapsed Time: 0 seconds", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        self.click_count_label = QLabel("Click Count: 0", self)
        self.click_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.click_count_label)

        self.start_button = QPushButton("Start Counting", self)
        self.start_button.clicked.connect(self.start_counting)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Counting", self)
        self.stop_button.clicked.connect(self.stop_counting)
        layout.addWidget(self.stop_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_counting(self):
        if not self.is_counting:
            self.is_counting = True
            self.timer.start(1000)  # Update every second

    def save_click_data(self, output_folder, filename, elapsed_time, click_count):
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)
        file_exists = os.path.isfile(filepath)

        with open(filepath, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Elapsed Time (seconds)", "Click Count"])
            writer.writerow([elapsed_time, click_count])
    
    def stop_counting(self):
        if self.is_counting:
            self.is_counting = False
            self.timer.stop()

        
        self.output_folder = os.path.join(os.getcwd(), "output")
        self.save_click_data(self.output_folder, "click_data.csv", self.seconds, self.click_count)

        
        self.click_monitor.stop()
        self.close()
    # ... [rest of the previous ClickCounter class implementation remains exactly the same] ...


def main():
    app = QApplication(sys.argv)

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