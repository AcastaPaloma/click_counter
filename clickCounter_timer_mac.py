import sys
import csv
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QTextEdit, QFileDialog,
                             QMessageBox)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont
import Quartz


class GlobalClickMonitor(QThread):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True

        # Create event tap
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,  # Tap point
            Quartz.kCGHeadInsertEventTap,  # Place at start of chain
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseDown),
            self.callback,
            None
        )

        if tap is None:
            print("Failed to create event tap. Make sure accessibility permissions are granted.")
            return

        # Create a run loop source
        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
        # Add to current run loop
        Quartz.CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(),
            run_loop_source,
            Quartz.kCFRunLoopDefaultMode
        )
        # Enable the tap
        Quartz.CGEventTapEnable(tap, True)
        # Start the run loop
        while self.running:
            Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)

    def callback(self, proxy, type_, event, refcon):
        if self.running:
            self.clicked.emit()
        return event

    def stop(self):
        self.running = False


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

    def initUI(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create title label
        title_label = QLabel('Global Click Counter')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24pt;
                color: #2c3e50;
                margin: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create display labels with larger font and better styling
        self.click_label = QLabel('Clicks: 0')
        self.click_label.setStyleSheet("""
            QLabel {
                font-size: 20pt;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
        """)

        self.time_label = QLabel('Time: 0 seconds')
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 20pt;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
        """)

        # Status indicator
        self.status_label = QLabel('Status: Ready')
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                color: #7f8c8d;
                margin-top: 5px;
            }
        """)

        # Create buttons with improved styling
        self.start_stop_button = QPushButton('Start Counting')
        self.start_stop_button.clicked.connect(self.toggle_counting)
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 15px;
                font-size: 16pt;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.start_stop_button.setMinimumHeight(60)

        self.folder_button = QPushButton('Set Output Folder')
        self.folder_button.clicked.connect(self.set_output_folder)
        self.folder_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 12pt;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.save_button = QPushButton('Save to CSV')
        self.save_button.clicked.connect(self.save_to_csv)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 10px;
                font-size: 12pt;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)

        # Create comment text area with better styling
        self.comment_label = QLabel('Comments:')
        self.comment_label.setStyleSheet("QLabel { font-size: 12pt; color: #2c3e50; }")
        self.comment_box = QTextEdit()
        self.comment_box.setStyleSheet("""
            QTextEdit {
                font-size: 12pt;
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
        """)
        self.comment_box.setMinimumHeight(100)

        # Folder label
        self.folder_label = QLabel('Output Folder: Not Set')
        self.folder_label.setStyleSheet("""
            QLabel {
                font-size: 10pt;
                color: #7f8c8d;
                padding: 5px;
                background-color: #f8f9f9;
                border-radius: 3px;
            }
        """)
        self.folder_label.setWordWrap(True)

        # Add widgets to layout with spacing
        layout.addWidget(title_label)
        layout.addSpacing(10)
        layout.addWidget(self.click_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        layout.addSpacing(20)
        layout.addWidget(self.start_stop_button)
        layout.addSpacing(10)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addSpacing(10)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_box)
        layout.addWidget(self.save_button)

        # Set window properties
        self.setGeometry(300, 300, 500, 700)
        self.setWindowTitle('Global Click Counter')
        self.setStyleSheet("background-color: white;")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

    def increment_counter(self):
        if self.is_counting:
            self.click_count += 1
            self.click_label.setText(f'Clicks: {self.click_count}')

    def toggle_counting(self):
        self.is_counting = not self.is_counting
        if self.is_counting:
            self.start_stop_button.setText('Stop Counting')
            self.start_stop_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 15px;
                    font-size: 16pt;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            self.timer.start(1000)
            self.status_label.setText('Status: Counting')
            self.status_label.setStyleSheet("QLabel { color: #27ae60; font-size: 12pt; }")
        else:
            self.start_stop_button.setText('Start Counting')
            self.start_stop_button.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    padding: 15px;
                    font-size: 16pt;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
            self.timer.stop()
            self.status_label.setText('Status: Paused')
            self.status_label.setStyleSheet("QLabel { color: #e67e22; font-size: 12pt; }")

    def update_timer(self):
        self.seconds += 1
        self.time_label.setText(f'Time: {self.seconds} seconds')

    def set_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.output_folder = folder
            display_path = folder
            if len(folder) > 40:
                display_path = folder[:20] + "..." + folder[-17:]
            self.folder_label.setText(f'Output Folder: {display_path}')

    def save_to_csv(self):
        if not self.output_folder:
            self.set_output_folder()
            if not self.output_folder:
                return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.output_folder, f'click_data_{timestamp}.csv')

        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Clicks', 'Duration (seconds)', 'Comments'])
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    self.click_count,
                    self.seconds,
                    self.comment_box.toPlainText()
                ])
            self.reset_counter()

            # Show success message
            QMessageBox.information(
                self,
                "Success",
                f"Data saved successfully to:\n{filename}",
                QMessageBox.StandardButton.Ok
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving file: {str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def reset_counter(self):
        self.click_count = 0
        self.seconds = 0
        self.is_counting = False
        self.click_label.setText('Clicks: 0')
        self.time_label.setText('Time: 0 seconds')
        self.comment_box.clear()
        self.start_stop_button.setText('Start Counting')
        self.start_stop_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 15px;
                font-size: 16pt;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.timer.stop()
        self.status_label.setText('Status: Ready')
        self.status_label.setStyleSheet("QLabel { color: #7f8c8d; font-size: 12pt; }")

    def closeEvent(self, event):
        self.click_monitor.stop()
        self.click_monitor.wait()
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont("Helvetica", 10)
    app.setFont(font)

    counter = ClickCounter()
    counter.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()