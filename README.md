# Global Click Counter

A cross-platform application that counts mouse clicks globally across your system, with timing and data export capabilities.

## Features

- Global click counting (works anywhere on screen)
- Timer functionality
- Start/Stop capabilities
- CSV export with timestamps
- Comment section for notes
- Cross-platform support (Windows, macOS, Linux)
- Visual feedback with color indicators
- Auto-saving capability

## Installation

### Prerequisites

```bash
# Install required packages
pip install PyQt6
```

Additional platform-specific requirements:

#### For macOS:
```bash
pip install pyobjc-framework-Quartz
```

#### For Windows:
```bash
pip install pywin32
```

#### For Linux:
```bash
# Install xinput using your package manager
sudo apt-get install xinput  # For Debian/Ubuntu
sudo dnf install xinput      # For Fedora
```

## Platform-Specific Setup

### macOS
1. Grant Accessibility permissions:
   - Open System Settings
   - Go to Privacy & Security
   - Click on Accessibility
   - Click the '+' button
   - Add your Terminal.app or IDE (e.g., PyCharm)
   - Ensure the checkbox is checked

### Windows
1. Run your Python IDE or Command Prompt as Administrator

### Linux
1. Ensure xinput is installed
2. Run the application with appropriate permissions

## Usage

1. Launch the application:
```bash
python click_counter.py
```

2. Features:
   - Click "Start Counting" to begin monitoring clicks
   - The timer will start automatically
   - Add comments in the text box if needed
   - Set an output folder for CSV files
   - Click "Save to CSV" to export the data

3. Data Export:
   - Data is saved in CSV format with the following columns:
     - Timestamp
     - Click Count
     - Duration (seconds)
     - Comments

## File Structure

```
click_counter/
│
├── click_counter.py     # Main application file
├── requirements.txt     # Package dependencies
└── README.md           # Documentation
```

## Requirements

- Python 3.6+
- PyQt6
- Platform-specific requirements (see Installation section)

## CSV Output Format

The application generates CSV files with the following structure:

```csv
Timestamp,Clicks,Duration (seconds),Comments
2024-11-08 15:30:45,42,67,"User comments here"
```

## Troubleshooting

### macOS
- If clicks aren't being registered, check Accessibility permissions
- Restart the application after granting permissions
- Make sure you're using the latest version of Python and PyQt

### Windows
- Run as Administrator if clicks aren't being captured
- Check if antivirus software is blocking the application
- Verify pywin32 is properly installed

### Linux
- Ensure xinput is installed and accessible
- Check system permissions
- Verify X11 is running (not Wayland)

## Known Issues

1. macOS Ventura/Sonoma:
   - May need to grant additional permissions
   - Might require application restart after permission changes

2. Windows:
   - Some antivirus software may block global input monitoring
   - UAC might interfere with administrator privileges

3. Linux:
   - Wayland sessions may not support global input monitoring
   - Different distributions might require different setup steps

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt6 for the GUI framework
- Platform-specific libraries for input monitoring
- The Python community for various helpful packages

## Version History

- 1.0.0
  - Initial release
  - Basic click counting and timing
  - CSV export capability

## Contact

For support or questions, please open an issue in the repository.