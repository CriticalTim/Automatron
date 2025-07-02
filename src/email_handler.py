import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import re


class EmailHandler:
    def __init__(self):
        self.smtp_server = None
        self.email = None
        self.password = None
        self.is_connected = False
        
        # Email server configurations
        self.email_configs = {
            'web.de': {
                'smtp_server': 'smtp.web.de',
                'port': 587,
                'use_tls': True
            },
            'gmail.com': {
                'smtp_server': 'smtp.gmail.com',
                'port': 587,
                'use_tls': True
            },
            'outlook.com': {
                'smtp_server': 'smtp-mail.outlook.com',
                'port': 587,
                'use_tls': True
            },
            'hotmail.com': {
                'smtp_server': 'smtp-mail.outlook.com',
                'port': 587,
                'use_tls': True
            },
            'yahoo.com': {
                'smtp_server': 'smtp.mail.yahoo.com',
                'port': 587,
                'use_tls': True
            },
            'gmx.de': {
                'smtp_server': 'mail.gmx.net',
                'port': 587,
                'use_tls': True
            },
            't-online.de': {
                'smtp_server': 'smtp.t-online.de',
                'port': 587,
                'use_tls': True
            }
        }
        
    def login(self, email: str, password: str) -> bool:
        """Login to email account"""
        try:
            self.email = email
            self.password = password
            
            # Determine email provider
            domain = email.split('@')[1].lower()
            
            if domain not in self.email_configs:
                raise Exception(f"Email provider {domain} not supported")
                
            config = self.email_configs[domain]
            
            # Test connection
            context = ssl.create_default_context()
            
            with smtplib.SMTP(config['smtp_server'], config['port']) as server:
                if config['use_tls']:
                    server.starttls(context=context)
                    
                server.login(email, password)
                
            self.is_connected = True
            return True
            
        except Exception as e:
            self.is_connected = False
            raise Exception(f"Email login failed: {str(e)}")
            
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.is_connected and self.email is not None
        
    def send_email(self, to_email: str, subject: str, body: str, 
                   html_body: Optional[str] = None) -> bool:
        """Send email"""
        try:
            if not self.is_logged_in():
                raise Exception("Not logged in to email account")
                
            # Validate recipient email
            if not self.is_valid_email(to_email):
                raise Exception(f"Invalid recipient email: {to_email}")
                
            domain = self.email.split('@')[1].lower()
            config = self.email_configs[domain]
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email
            message["To"] = to_email
            
            # Add text part
            text_part = MIMEText(body, "plain", "utf-8")
            message.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, "html", "utf-8")
                message.attach(html_part)
                
            # Send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(config['smtp_server'], config['port']) as server:
                if config['use_tls']:
                    server.starttls(context=context)
                    
                server.login(self.email, self.password)
                server.sendmail(self.email, to_email, message.as_string())
                
            return True
            
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
            
    def send_application_email(self, project: Dict, user_profile: Dict) -> bool:
        """Send application email for a specific project"""
        try:
            # Generate email content
            subject = self.generate_subject(project)
            body = self.generate_application_body(project, user_profile)
            html_body = self.generate_html_body(project, user_profile)
            
            # Send email
            return self.send_email(
                to_email=project.get('contact_email', ''),
                subject=subject,
                body=body,
                html_body=html_body
            )
            
        except Exception as e:
            raise Exception(f"Failed to send application email: {str(e)}")
            
    def generate_subject(self, project: Dict) -> str:
        """Generate email subject line"""
        project_title = project.get('title', 'Project')
        
        # Keep subject concise and professional
        if len(project_title) > 50:
            project_title = project_title[:47] + "..."
            
        return f"Bewerbung für: {project_title}"
        
    def generate_application_body(self, project: Dict, user_profile: Dict) -> str:
        """Generate plain text email body"""
        name = user_profile.get('name', 'Freelancer')
        skills = user_profile.get('skills', [])
        experience_years = user_profile.get('experience_years', 0)
        
        # Top matching skills
        top_skills = skills[:5] if skills else []
        
        body = f"""Sehr geehrte Damen und Herren,

mit großem Interesse habe ich Ihr Projekt "{project.get('title', '')}" auf FreelancerMap gelesen.

Als erfahrener Freelancer mit {experience_years} Jahren Berufserfahrung bringe ich folgende Qualifikationen mit:

Technische Kompetenzen:
{self.format_skills_list(top_skills)}

Warum bin ich der richtige Partner für Ihr Projekt:
- Umfangreiche Erfahrung in den geforderten Technologien
- Zuverlässige und termingerechte Projektumsetzung
- Klare Kommunikation und regelmäßige Updates
- Fokus auf Qualität und Kundenzufriedenheit

Gerne stehe ich Ihnen für ein unverbindliches Gespräch zur Verfügung, um Details zu besprechen und Ihnen zu zeigen, wie ich Ihr Projekt erfolgreich umsetzen kann.

Mit freundlichen Grüßen
{name}

E-Mail: {user_profile.get('email', self.email)}
{f"Telefon: {user_profile.get('phone')}" if user_profile.get('phone') else ""}"""

        return body
        
    def generate_html_body(self, project: Dict, user_profile: Dict) -> str:
        """Generate HTML email body"""
        name = user_profile.get('name', 'Freelancer')
        skills = user_profile.get('skills', [])
        experience_years = user_profile.get('experience_years', 0)
        
        # Top matching skills
        top_skills = skills[:5] if skills else []
        skills_html = "".join([f"<li>{skill}</li>" for skill in top_skills])
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Bewerbung für: {project.get('title', '')}</h2>
                
                <p>Sehr geehrte Damen und Herren,</p>
                
                <p>mit großem Interesse habe ich Ihr Projekt auf FreelancerMap gelesen.</p>
                
                <p>Als erfahrener Freelancer mit <strong>{experience_years} Jahren Berufserfahrung</strong> bringe ich folgende Qualifikationen mit:</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 15px 0;">
                    <h3 style="margin-top: 0; color: #007bff;">Technische Kompetenzen:</h3>
                    <ul>
                        {skills_html}
                    </ul>
                </div>
                
                <h3 style="color: #28a745;">Warum bin ich der richtige Partner für Ihr Projekt:</h3>
                <ul>
                    <li>Umfangreiche Erfahrung in den geforderten Technologien</li>
                    <li>Zuverlässige und termingerechte Projektumsetzung</li>
                    <li>Klare Kommunikation und regelmäßige Updates</li>
                    <li>Fokus auf Qualität und Kundenzufriedenheit</li>
                </ul>
                
                <p>Gerne stehe ich Ihnen für ein unverbindliches Gespräch zur Verfügung, um Details zu besprechen und Ihnen zu zeigen, wie ich Ihr Projekt erfolgreich umsetzen kann.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p><strong>Mit freundlichen Grüßen<br>{name}</strong></p>
                    <p>
                        E-Mail: <a href="mailto:{user_profile.get('email', self.email)}">{user_profile.get('email', self.email)}</a><br>
                        {f"Telefon: {user_profile.get('phone')}<br>" if user_profile.get('phone') else ""}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
        
    def format_skills_list(self, skills: list) -> str:
        """Format skills list for plain text email"""
        if not skills:
            return "- Siehe angehängtes Profil für Details"
            
        formatted_skills = []
        for skill in skills:
            formatted_skills.append(f"- {skill}")
            
        return "\n".join(formatted_skills)
        
    def is_valid_email(self, email: str) -> bool:
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def test_connection(self) -> bool:
        """Test email connection without sending"""
        try:
            if not self.email or not self.password:
                return False
                
            domain = self.email.split('@')[1].lower()
            
            if domain not in self.email_configs:
                return False
                
            config = self.email_configs[domain]
            context = ssl.create_default_context()
            
            with smtplib.SMTP(config['smtp_server'], config['port']) as server:
                if config['use_tls']:
                    server.starttls(context=context)
                    
                server.login(self.email, self.password)
                
            return True
            
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
            
    def logout(self):
        """Logout from email account"""
        self.email = None
        self.password = None
        self.is_connected = False