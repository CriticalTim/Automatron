import re
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


class ProjectMatcher:
    def __init__(self):
        self.skill_synonyms = {
            'javascript': ['js', 'javascript', 'ecmascript'],
            'typescript': ['ts', 'typescript'],
            'python': ['python', 'py'],
            'react': ['react', 'reactjs', 'react.js'],
            'angular': ['angular', 'angularjs', 'angular.js'],
            'vue': ['vue', 'vuejs', 'vue.js'],
            'node.js': ['node', 'nodejs', 'node.js'],
            'c++': ['c++', 'cpp', 'c plus plus'],
            'c#': ['c#', 'csharp', 'c sharp'],
            'asp.net': ['asp.net', 'aspnet', 'asp net'],
            'mysql': ['mysql', 'my sql'],
            'postgresql': ['postgresql', 'postgres', 'pgsql'],
            'mongodb': ['mongodb', 'mongo'],
            'aws': ['aws', 'amazon web services'],
            'gcp': ['gcp', 'google cloud platform', 'google cloud'],
            'docker': ['docker', 'containerization'],
            'kubernetes': ['kubernetes', 'k8s'],
            'machine learning': ['machine learning', 'ml', 'maschinelles lernen'],
            'artificial intelligence': ['artificial intelligence', 'ai', 'künstliche intelligenz'],
            'data science': ['data science', 'datenwissenschaft'],
            'web development': ['web development', 'webentwicklung', 'web dev'],
            'mobile development': ['mobile development', 'mobile dev', 'app development'],
        }
        
    def match_projects(self, projects: List[Dict], user_profile: Dict) -> List[Dict]:
        """Match projects against user profile and calculate scores"""
        matched_projects = []
        
        user_skills = [skill.lower() for skill in user_profile.get('skills', [])]
        user_keywords = self.extract_keywords_from_profile(user_profile)
        
        for project in projects:
            match_score = self.calculate_match_score(project, user_skills, user_keywords, user_profile)
            
            if match_score > 0.3:  # Only include projects with reasonable match
                project['match_score'] = match_score
                project['match_reasons'] = self.get_match_reasons(project, user_skills, user_keywords)
                matched_projects.append(project)
                
        # Sort by match score (highest first)
        matched_projects.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matched_projects
        
    def calculate_match_score(self, project: Dict, user_skills: List[str], 
                            user_keywords: List[str], user_profile: Dict) -> float:
        """Calculate match score between project and user profile"""
        total_score = 0.0
        max_score = 100.0
        
        # Skill matching (40% weight)
        skill_score = self.calculate_skill_match(project, user_skills)
        total_score += skill_score * 0.4
        
        # Keyword matching in description (30% weight)
        keyword_score = self.calculate_keyword_match(project, user_keywords)
        total_score += keyword_score * 0.3
        
        # Experience level matching (20% weight)
        experience_score = self.calculate_experience_match(project, user_profile)
        total_score += experience_score * 0.2
        
        # Language matching (10% weight)
        language_score = self.calculate_language_match(project, user_profile)
        total_score += language_score * 0.1
        
        return min(total_score / max_score, 1.0)
        
    def calculate_skill_match(self, project: Dict, user_skills: List[str]) -> float:
        """Calculate skill-based match score"""
        project_skills = [skill.lower() for skill in project.get('skills', [])]
        project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
        
        matched_skills = 0
        total_project_skills = len(project_skills) if project_skills else 1
        
        # Direct skill matching
        for user_skill in user_skills:
            if self.skill_matches(user_skill, project_skills + [project_text]):
                matched_skills += 1
                
        # Extract skills from project text if no explicit skills
        if not project_skills:
            inferred_skills = self.extract_skills_from_text(project_text)
            for user_skill in user_skills:
                if self.skill_matches(user_skill, inferred_skills):
                    matched_skills += 1
                    
            total_project_skills = max(len(inferred_skills), 1)
            
        return min((matched_skills / len(user_skills)) * 100, 100.0)
        
    def calculate_keyword_match(self, project: Dict, user_keywords: List[str]) -> float:
        """Calculate keyword-based match score"""
        project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
        
        matched_keywords = 0
        for keyword in user_keywords:
            if keyword.lower() in project_text:
                matched_keywords += 1
                
        if not user_keywords:
            return 50.0  # Neutral score if no keywords
            
        return (matched_keywords / len(user_keywords)) * 100
        
    def calculate_experience_match(self, project: Dict, user_profile: Dict) -> float:
        """Calculate experience level match"""
        user_experience = user_profile.get('experience_years', 0)
        project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
        
        # Look for experience requirements in project
        experience_patterns = [
            r'(\d+)\s*(?:jahre?|years?)\s*(?:erfahrung|experience)',
            r'(?:mindestens|minimum|at least)\s*(\d+)\s*(?:jahre?|years?)',
            r'(\d+)\+\s*(?:jahre?|years?)',
            r'(?:senior|experienced|expert)',
            r'(?:junior|entry|beginner|einsteiger)'
        ]
        
        required_experience = 0
        is_senior = False
        is_junior = False
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, project_text)
            if matches:
                try:
                    exp = int(matches[0]) if matches[0].isdigit() else 0
                    required_experience = max(required_experience, exp)
                except:
                    pass
                    
        if 'senior' in project_text or 'expert' in project_text:
            is_senior = True
        elif 'junior' in project_text or 'entry' in project_text or 'einsteiger' in project_text:
            is_junior = True
            
        # Score based on experience match
        if is_senior and user_experience >= 5:
            return 100.0
        elif is_junior and user_experience <= 3:
            return 100.0
        elif required_experience > 0:
            if user_experience >= required_experience:
                return 100.0
            elif user_experience >= required_experience * 0.7:
                return 70.0
            else:
                return 30.0
        else:
            return 70.0  # Neutral score if no clear requirements
            
    def calculate_language_match(self, project: Dict, user_profile: Dict) -> float:
        """Calculate language requirement match"""
        user_languages = [lang.lower() for lang in user_profile.get('languages', [])]
        project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
        
        # Common language requirements
        language_keywords = {
            'deutsch': ['deutsch', 'german'],
            'englisch': ['englisch', 'english'],
            'französisch': ['französisch', 'french'],
            'spanisch': ['spanisch', 'spanish']
        }
        
        required_languages = []
        for lang, keywords in language_keywords.items():
            if any(keyword in project_text for keyword in keywords):
                required_languages.append(lang)
                
        if not required_languages:
            return 80.0  # Neutral score if no language requirements
            
        matched_languages = 0
        for req_lang in required_languages:
            if any(req_lang in user_lang for user_lang in user_languages):
                matched_languages += 1
                
        return (matched_languages / len(required_languages)) * 100
        
    def skill_matches(self, user_skill: str, project_skills: List[str]) -> bool:
        """Check if user skill matches any project skill"""
        user_skill_lower = user_skill.lower()
        
        # Direct matching
        for project_skill in project_skills:
            if user_skill_lower in project_skill.lower():
                return True
                
        # Synonym matching
        for skill, synonyms in self.skill_synonyms.items():
            if user_skill_lower in synonyms:
                for project_skill in project_skills:
                    if any(syn in project_skill.lower() for syn in synonyms):
                        return True
                        
        return False
        
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from project text"""
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'php', 'laravel', 'django', 'flask', 'mysql', 'postgresql',
            'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'html', 'css',
            'bootstrap', 'jquery', 'rest', 'api', 'json', 'xml', 'sql', 'nosql'
        ]
        
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill)
                
        return found_skills
        
    def extract_keywords_from_profile(self, user_profile: Dict) -> List[str]:
        """Extract relevant keywords from user profile"""
        keywords = []
        
        # Add skills as keywords
        keywords.extend(user_profile.get('skills', []))
        
        # Extract keywords from summary
        summary = user_profile.get('summary', '')
        if summary:
            # Simple keyword extraction - can be enhanced
            words = re.findall(r'\b\w{4,}\b', summary.lower())
            keywords.extend(words[:10])  # Limit to top 10 words
            
        # Add project-related keywords
        projects = user_profile.get('projects', [])
        for project in projects:
            words = re.findall(r'\b\w{4,}\b', project.lower())
            keywords.extend(words[:5])  # Limit words per project
            
        return list(set(keywords))  # Remove duplicates
        
    def get_match_reasons(self, project: Dict, user_skills: List[str], 
                         user_keywords: List[str]) -> List[str]:
        """Get reasons why project matches user profile"""
        reasons = []
        
        project_skills = [skill.lower() for skill in project.get('skills', [])]
        project_text = (project.get('title', '') + ' ' + project.get('description', '')).lower()
        
        # Skill matches
        matched_skills = []
        for user_skill in user_skills:
            if self.skill_matches(user_skill, project_skills + [project_text]):
                matched_skills.append(user_skill)
                
        if matched_skills:
            reasons.append(f"Matching skills: {', '.join(matched_skills[:3])}")
            
        # Keyword matches
        matched_keywords = []
        for keyword in user_keywords[:10]:  # Check top keywords
            if keyword.lower() in project_text:
                matched_keywords.append(keyword)
                
        if matched_keywords:
            reasons.append(f"Relevant keywords: {', '.join(matched_keywords[:3])}")
            
        return reasons