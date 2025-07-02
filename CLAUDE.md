# Automatron - Claude Code Memory

## Project Overview
Automatron is a Python GUI application for automated freelancer job applications. It uses web scraping, email automation, and PDF processing to help freelancers apply to jobs automatically.

## Architecture
- **Main Entry**: `run.py` - Application entry point
- **Core Logic**: `src/main.py` - Main FreelancerApp class
- **GUI**: CustomTkinter-based interface
- **Dependencies**: Web scraping (Selenium), email (SMTP), PDF processing (PyPDF2)

## Key Files
- `run.py` - Entry point, imports from src/main.py
- `src/main.py` - Main application class
- `src/scraper.py` - Web scraping functionality
- `src/email_handler.py` - Email automation
- `src/database.py` - Data persistence
- `src/matcher.py` - Job matching logic
- `src/profile_parser.py` - Profile parsing
- `Automatron.spec` - PyInstaller build configuration
- `requirements.txt` - Python dependencies
- `build_exe.bat` - Windows build script

## Dependencies (requirements.txt)
```
customtkinter==5.2.2
requests==2.31.0
beautifulsoup4==4.12.3
PyPDF2==3.0.1
schedule==1.2.1
selenium==4.15.2
webdriver-manager==4.0.1
python-dotenv==1.0.0
pyinstaller>=6.10.0
pillow>=10.2.0
```

## Python Version Compatibility
- **Python 3.13**: Requires PyInstaller 6.10.0+ and Pillow 10.2.0+
- **Python 3.12**: Compatible with PyInstaller 6.3.0+
- **Python 3.8-3.11**: Compatible with original versions

## Build Process
**Windows**: Run `build_exe.bat` - Creates `Automatron.exe`
**Linux/Mac**: Run `build_exe.sh` - Creates `Automatron` binary

### Build Fixes Applied
1. **PyInstaller spec improvements**:
   - Added error handling for missing dependencies during collection
   - Added comprehensive hidden imports including: bs4, dotenv, python_dotenv, PIL submodules
   - Added safe collection functions to prevent build failures

2. **Build script improvements**:
   - Added pip upgrade step before dependency installation
   - Added fallback individual package installation if batch install fails
   - Better error handling and reporting

## Common Issues & Solutions
- **"No module named 'customtkinter'"**: Install with `pip install customtkinter==5.2.2`
- **BeautifulSoup import errors**: Spec includes both `bs4` and `beautifulsoup4`
- **Dotenv import errors**: Added both `python_dotenv` and `dotenv` to hidden imports
- **Large exe size**: Normal (150-300MB) due to Python interpreter + libraries
- **Antivirus blocking**: Add Windows Defender exception for the exe

## Testing
- Requires Chrome browser for Selenium WebDriver
- Test by running: `python3 run.py` or `python run.py`
- Built exe should be self-contained

## Security Notes
- This is a legitimate automation tool for freelancers
- Uses web scraping and email automation for job applications
- No malicious functionality detected
- Source code available for inspection

## Last Updated
Built with PyInstaller 6.3.0, CustomTkinter 5.2.2, Selenium 4.15.2