# Shortcut Launcher

A cross-platform GUI to organize and execute custom commands through a clean, tree-structured interface. 

Ideal for managing complex commands, launching applications with specific parameters, or consolidating frequently used tools.

<img width="272" alt="image" src="https://github.com/user-attachments/assets/14c994b6-5bf0-4ba7-945d-bd16e6712e3a">

## Additional Features

- Dark/Light theme support
- Execute commands in separate terminal windows
- Persistent storage for shortcuts and settings
- Comprehensive error logging and handling

## Requirements

- Python 3.8+
- PyQt6

## Installation

Windows users, you can just download the [compiled executable](https://github.com/sm18lr88/Shortcut_launcher/releases/download/alpha_0.1/ShortcutLauncher.exe) if you'd like.

### One-Line Installation (Conda/Miniconda + Git)
```bash
conda create -n shortcuts && conda activate shortcuts && pip install pyqt6 pyside6 && git clone https://github.com/sm18lr88/Shortcut_launcher.git && cd Shortcut_launcher && python run.py
```

### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sm18lr88/Shortcut_launcher.git
   cd shortcut-launcher
   ```

2. (Optional) Create and activate a virtual environment:
   - **Windows:** `venv\Scripts\activate`
   - **Unix:** `source venv/bin/activate`

   ```bash
   python -m venv venv
   ```

3. Install dependencies:
   ```bash
   pip install PyQt6 pyside6
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## Usage

1. **Managing Shortcuts:**
   - Add categories via "Add Category."
   - Add shortcuts within a category using "Add Shortcut."
   - Execute shortcuts by double-clicking them.
   - Access editing and deletion options via right-click.

### Tips

Don't try to change terminal locations through the shortcut command, like `E: && cd E:\path\to\folder\ && conda activate base && python run.py`

Instead, do `conda activate base && python E:\path\to\folder\run.py`

2. **Automatic Persistence:** Shortcuts and settings save automatically.

## Configuration

- Shortcuts: `data/shortcuts.json`
- Settings: `data/settings.json`
- Logs: `logs/`

## Theme Customization

- Default: Dark mode (Light mode available).
- Modify themes by editing QSS files in `app/styles`.

## Error Handling

- General logs: `logs/app.log`
- Error logs: `logs/error.log`
- Errors trigger user notifications.

## To compile the app into executable for your platform:

### Windows
```bash
pyinstaller --name ShortcutLauncher ^
            --add-data "app/styles;app/styles" ^
            --add-data "data;data" ^
            --hidden-import PyQt6 ^
            --noconsole ^
            --onefile ^
            --clean ^
            run.py
```

### Linux
```bash
pyinstaller --name ShortcutLauncher \
            --add-data "app/styles:app/styles" \
            --add-data "data:data" \
            --hidden-import PyQt6 \
            --noconsole \
            --onefile \
            --clean \
            run.py
```

### Mac:
```bash
# First, generate a spec file
pyi-makespec --name ShortcutLauncher \
             --add-data "app/styles:app/styles" \
             --add-data "data:data" \
             --hidden-import PyQt6 \
             --noconsole \
             --onefile \
             run.py

# Then edit the spec file to add macOS-specific options and build using:
pyinstaller ShortcutLauncher.spec
```


## Roadmap

- [ ] Drag-and-drop shortcuts across categories
- [ ] Custom app icon
- [ ] Visually select starting location for shortcut command
- [ ] Subcategories
- [ ] Description fields
- [ ] Improved commands textbox

Here's a preview:

<img width="524" alt="image" src="https://github.com/user-attachments/assets/99dcfde8-5720-41b4-8efe-168360d6f76a">


## License

[MIT License](LICENSE)
