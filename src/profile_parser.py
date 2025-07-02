import PyPDF2
import re
from typing import Dict, List, Optional


class ProfileParser:
    def __init__(self):
        self.skill_keywords = [
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'sass', 'less',
            
            # Frameworks and libraries
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel', 'symfony',
            'rails', 'asp.net', 'node.js', 'jquery', 'bootstrap', 'tailwind', 'tensorflow', 'pytorch',
            'keras', 'pandas', 'numpy', 'opencv', 'scikit-learn',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            'dynamodb', 'cassandra', 'neo4j',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'git',
            'github', 'gitlab', 'bitbucket', 'travis', 'circleci', 'terraform', 'ansible',
            
            # Tools and platforms
            'linux', 'windows', 'macos', 'ubuntu', 'centos', 'nginx', 'apache', 'jira', 'confluence',
            'slack', 'trello', 'asana', 'figma', 'sketch', 'photoshop', 'illustrator',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd', 'microservices',
            'rest api', 'graphql', 'soap', 'microservices', 'machine learning', 'deep learning',
            'artificial intelligence', 'data science', 'big data', 'blockchain', 'iot',
            
            # German technical terms
            'softwareentwicklung', 'webentwicklung', 'datenbank', 'programmierung', 'testing',
            'qualitätssicherung', 'projektmanagement', 'beratung', 'analyse', 'konzeption'
        ]
        
        self.experience_patterns = [
            r'(\d+)\s*(?:jahre?|years?)\s*(?:erfahrung|experience)',
            r'(?:seit|since)\s*(\d{4})',
            r'(\d{4})\s*-\s*(?:\d{4}|heute|today|present)',
            r'(\d+)\+\s*(?:jahre?|years?)'
        ]
        
    def parse_pdf(self, file_path: str) -> Dict:
        """Parse PDF and extract profile information"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                    
            return self.parse_text(text)
            
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
            
    def parse_text(self, text: str) -> Dict:
        """Parse text and extract profile information"""
        text_lower = text.lower()
        
        profile = {
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text_lower),
            'experience_years': self.extract_experience_years(text_lower),
            'education': self.extract_education(text),
            'certifications': self.extract_certifications(text),
            'languages': self.extract_languages(text_lower),
            'projects': self.extract_projects(text),
            'summary': self.extract_summary(text),
            'raw_text': text
        }
        
        return profile
        
    def extract_name(self, text: str) -> str:
        """Extract name from text"""
        lines = text.split('\n')
        
        # Name is often in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line) < 50:
                # Check if it looks like a name (no numbers, reasonable length)
                if not re.search(r'\d', line) and not re.search(r'[@.]', line):
                    return line
                    
        return ""
        
    def extract_email(self, text: str) -> str:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
        
    def extract_phone(self, text: str) -> str:
        """Extract phone number"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,15}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
                
        return ""
        
    def extract_skills(self, text_lower: str) -> List[str]:
        """Extract technical skills"""
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill in text_lower:
                # Check if it's a whole word match
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    found_skills.append(skill.title())
                    
        return list(set(found_skills))  # Remove duplicates
        
    def extract_experience_years(self, text_lower: str) -> int:
        """Extract years of experience"""
        max_years = 0
        
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = int(match)
                    if years > max_years and years < 50:  # Reasonable range
                        max_years = years
                except ValueError:
                    continue
                    
        return max_years
        
    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'diploma', 'degree',
            'university', 'college', 'school', 'institut', 'universität',
            'studium', 'ausbildung', 'abschluss'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                if len(line.strip()) > 10 and len(line.strip()) < 200:
                    education.append(line.strip())
                    
        return education[:3]  # Limit to 3 entries
        
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        cert_keywords = [
            'certified', 'certification', 'certificate', 'zertifikat', 'zertifizierung',
            'aws', 'azure', 'google cloud', 'microsoft', 'oracle', 'cisco', 'pmp',
            'scrum master', 'agile', 'itil'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in cert_keywords):
                if len(line.strip()) > 5 and len(line.strip()) < 150:
                    certifications.append(line.strip())
                    
        return certifications[:5]  # Limit to 5 entries
        
    def extract_languages(self, text_lower: str) -> List[str]:
        """Extract spoken languages"""
        languages = []
        language_keywords = [
            'deutsch', 'german', 'englisch', 'english', 'französisch', 'french',
            'spanisch', 'spanish', 'italienisch', 'italian', 'russisch', 'russian',
            'chinesisch', 'chinese', 'japanisch', 'japanese', 'arabisch', 'arabic',
            'portugiesisch', 'portuguese', 'niederländisch', 'dutch', 'polnisch', 'polish'
        ]
        
        for lang in language_keywords:
            if lang in text_lower:
                languages.append(lang.title())
                
        return list(set(languages))
        
    def extract_projects(self, text: str) -> List[str]:
        """Extract project descriptions"""
        projects = []
        project_keywords = [
            'projekt', 'project', 'entwicklung', 'development', 'implementierung',
            'implementation', 'realisierung', 'system', 'anwendung', 'application'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                if len(line.strip()) > 20 and len(line.strip()) < 300:
                    projects.append(line.strip())
                    
        return projects[:5]  # Limit to 5 entries
        
    def extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        lines = text.split('\n')
        
        # Look for summary sections
        summary_keywords = [
            'zusammenfassung', 'summary', 'profil', 'profile', 'über mich', 'about me',
            'qualifikationen', 'qualifications', 'skills', 'kompetenzen'
        ]
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in summary_keywords):
                # Take the next few lines as summary
                summary_lines = []
                for j in range(i + 1, min(i + 10, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and len(next_line) > 10:
                        summary_lines.append(next_line)
                    elif len(summary_lines) > 0:  # Stop at empty line
                        break
                        
                if summary_lines:
                    return ' '.join(summary_lines)[:500]  # Limit length
                    
        # If no summary section found, take first substantial paragraph
        for line in lines[:20]:
            if len(line.strip()) > 50:
                return line.strip()[:500]
                
        return ""
        
    def get_skill_categories(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills"""
        categories = {
            'Programming Languages': [],
            'Frameworks': [],
            'Databases': [],
            'Cloud & DevOps': [],
            'Tools': [],
            'Other': []
        }
        
        programming_langs = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust']
        frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel']
        databases = ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite']
        cloud_devops = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git']
        tools = ['linux', 'windows', 'nginx', 'apache', 'jira', 'confluence', 'figma', 'photoshop']
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(lang in skill_lower for lang in programming_langs):
                categories['Programming Languages'].append(skill)
            elif any(fw in skill_lower for fw in frameworks):
                categories['Frameworks'].append(skill)
            elif any(db in skill_lower for db in databases):
                categories['Databases'].append(skill)
            elif any(cd in skill_lower for cd in cloud_devops):
                categories['Cloud & DevOps'].append(skill)
            elif any(tool in skill_lower for tool in tools):
                categories['Tools'].append(skill)
            else:
                categories['Other'].append(skill)
                
        return categories