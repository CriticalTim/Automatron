# Freelancer AutoApply

A modern desktop application for automated job application to FreelancerMap.de projects.

## Features

- **Modern GUI**: Clean, dark-themed interface built with CustomTkinter
- **PDF Profile Upload**: Parse your CV/resume to extract skills and experience
- **Smart Web Scraping**: Automated scraping of FreelancerMap.de projects
- **Intelligent Matching**: AI-powered matching of projects to your profile
- **Email Integration**: Automated email generation and sending (supports web.de, Gmail, etc.)
- **Application History**: Track all applications with SQLite database
- **Scheduled Scraping**: Weekly automated project discovery

## Installation & Usage

### 🚀 **Quick Start (Recommended)**

#### Option 1: Use Pre-built Executable
1. **Download/clone** this repository
2. **Build executable**:
   ```bash
   # Windows
   build_exe.bat
   
   # Linux/Mac
   ./build_exe.sh
   ```
3. **Run**: Double-click `Automatron.exe` (Windows) or `./Automatron` (Linux/Mac)

#### Option 2: Run from Source
1. **Install Python 3.8+** and **Chrome browser**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   python run.py
   ```

### 📋 **How to Use**

1. **Upload your profile**:
   - Click "Upload PDF Profile" and select your CV/resume
   - The app will extract your skills, experience, and qualifications

2. **Configure email**:
   - Enter your email credentials (web.de, Gmail, etc.)
   - Click "Login" to authenticate

3. **Scrape projects**:
   - Click "Scrape Now" to find matching projects
   - Projects are automatically scored based on your profile

4. **Apply to projects**:
   - Select projects you want to apply to
   - Click "Apply to Selected" and confirm
   - Professional emails are sent automatically

5. **View history**:
   - Switch to "History" tab to see all past applications
   - Prevents duplicate applications

## Project Structure

```
src/
├── main.py           # Main application GUI
├── database.py       # SQLite database operations
├── scraper.py        # FreelancerMap.de web scraper
├── profile_parser.py # PDF CV parsing
├── matcher.py        # Project matching algorithm
├── email_handler.py  # Email sending functionality
└── __init__.py
```

## Configuration

The app automatically detects email providers and configures SMTP settings for:
- web.de
- Gmail
- Outlook/Hotmail
- Yahoo
- GMX
- T-Online

## Security Notes

- Email credentials are stored in memory only during session
- No credentials are saved to disk
- All email communication uses TLS encryption
- Web scraping respects rate limits and robots.txt

## Troubleshooting

**Chrome Driver Issues**:
- The app automatically downloads ChromeDriver
- Ensure Chrome browser is installed and up-to-date

**Email Login Issues**:
- Enable "Less secure app access" for Gmail
- Use app-specific passwords for 2FA accounts
- Check firewall/antivirus blocking SMTP connections

**Scraping Issues**:
- FreelancerMap.de may update their layout
- Check your internet connection
- Some projects may not have email addresses

## Legal Notice

This tool is for legitimate job seeking purposes only. Please:
- Respect FreelancerMap.de's terms of service
- Don't spam or send inappropriate emails
- Only apply to relevant projects
- Follow ethical web scraping practices

## License

This project is for educational and personal use only.