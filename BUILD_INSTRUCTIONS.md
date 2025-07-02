# Building Automatron Executable

## Quick Build

### Windows
1. Double-click `build_exe.bat`
2. Wait for the build to complete (5-10 minutes)
3. Run `Automatron.exe`

### Linux/Mac
1. Run `./build_exe.sh`
2. Wait for the build to complete
3. Run `./Automatron`

## Manual Build Process

If the automated scripts don't work, follow these steps:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build Executable
```bash
pyinstaller --clean Automatron.spec
```

### 3. Find Executable
- **Windows**: `dist/Automatron.exe`
- **Linux/Mac**: `dist/Automatron`

## Troubleshooting

### Common Issues

**ModuleNotFoundError during build:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Update pip: `pip install --upgrade pip`

**Build fails with CustomTkinter errors:**
- Install latest version: `pip install --upgrade customtkinter`
- Clear build cache: `pyinstaller --clean Automatron.spec`

**Executable doesn't start:**
- Run from command line to see error messages
- Check Windows Defender / antivirus (may block the exe)
- Ensure Chrome browser is installed (required for web scraping)

**Large executable size:**
- This is normal - the exe includes Python interpreter and all libraries
- Typical size: 150-300 MB

### Build Requirements

- **Python 3.8+**
- **Chrome Browser** (for Selenium WebDriver)
- **Internet Connection** (to download dependencies)
- **Disk Space**: 1GB+ for build process

### Distribution

The built executable is self-contained and can be distributed to other machines without Python installed. However, the target machine still needs:

- Chrome browser (for web scraping)
- Internet connection (for email and scraping)
- Windows Defender / antivirus exceptions (may flag as suspicious)

## File Structure After Build

```
Automatron/
├── Automatron.exe          # Main executable (Windows)
├── Automatron              # Main executable (Linux/Mac)
├── src/                    # Source code
├── build_exe.bat           # Windows build script
├── build_exe.sh            # Linux/Mac build script
├── Automatron.spec         # PyInstaller configuration
├── app_icon.ico            # Application icon
├── requirements.txt        # Python dependencies
└── README.md               # User documentation
```

## Security Notes

- Antivirus software may flag the executable as suspicious (false positive)
- Add exception for the executable in Windows Defender
- The executable is safe - it's your own code packaged with Python
- Source code is available for inspection in the `src/` folder