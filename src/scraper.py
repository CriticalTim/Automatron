import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re


class FreelancerMapScraper:
    def __init__(self):
        self.base_url = "https://www.freelancermap.de"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
        
    def scrape_projects(self, max_pages=5):
        projects = []
        driver = None
        
        try:
            driver = self.setup_driver()
            
            # Navigate to project search page
            search_url = f"{self.base_url}/projektboerse"
            driver.get(search_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "project-item"))
            )
            
            for page in range(1, max_pages + 1):
                print(f"Scraping page {page}...")
                
                # Get project links from current page
                project_links = self.extract_project_links(driver)
                
                # Scrape details for each project
                for link in project_links[:10]:  # Limit to 10 projects per page
                    try:
                        project_data = self.scrape_project_details(driver, link)
                        if project_data:
                            projects.append(project_data)
                            
                        # Random delay to avoid rate limiting
                        time.sleep(random.uniform(1, 3))
                        
                    except Exception as e:
                        print(f"Error scraping project {link}: {str(e)}")
                        continue
                        
                # Try to go to next page
                if not self.go_to_next_page(driver):
                    break
                    
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            
        finally:
            if driver:
                driver.quit()
                
        return projects
        
    def extract_project_links(self, driver):
        links = []
        try:
            # Find all project containers
            project_elements = driver.find_elements(By.CSS_SELECTOR, ".project-item a, .project-title a, [href*='/projekt/']")
            
            for element in project_elements:
                href = element.get_attribute('href')
                if href and '/projekt/' in href:
                    if href.startswith('/'):
                        href = self.base_url + href
                    links.append(href)
                    
        except Exception as e:
            print(f"Error extracting project links: {str(e)}")
            
        return list(set(links))  # Remove duplicates
        
    def scrape_project_details(self, driver, project_url):
        try:
            driver.get(project_url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract project data
            project_data = {
                'url': project_url,
                'title': self.safe_get_text(driver, "h1, .project-title, .title"),
                'description': self.safe_get_text(driver, ".project-description, .description, .content"),
                'company': self.safe_get_text(driver, ".company-name, .client-name, .company"),
                'location': self.safe_get_text(driver, ".location, .project-location"),
                'budget': self.safe_get_text(driver, ".budget, .price, .rate"),
                'duration': self.safe_get_text(driver, ".duration, .project-duration"),
                'posted_date': self.safe_get_text(driver, ".posted-date, .date"),
                'skills': self.extract_skills(driver),
                'contact_email': self.extract_contact_info(driver),
                'match_score': 0.0  # Will be calculated by matcher
            }
            
            # Basic validation
            if not project_data['title'] or len(project_data['title']) < 5:
                return None
                
            return project_data
            
        except Exception as e:
            print(f"Error scraping project details from {project_url}: {str(e)}")
            return None
            
    def safe_get_text(self, driver, selector):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return elements[0].text.strip()
        except:
            pass
        return ""
        
    def extract_skills(self, driver):
        skills = []
        try:
            # Common selectors for skills/tags
            skill_selectors = [
                ".skills .skill, .tags .tag",
                ".skill-item, .tag-item",
                ".skills span, .tags span",
                "[class*='skill'], [class*='tag']"
            ]
            
            for selector in skill_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and len(text) < 30:  # Reasonable skill name length
                        skills.append(text)
                        
                if skills:  # If we found skills with this selector, stop
                    break
                    
        except Exception as e:
            print(f"Error extracting skills: {str(e)}")
            
        return list(set(skills))  # Remove duplicates
        
    def extract_contact_info(self, driver):
        try:
            # Look for email patterns in the page
            page_source = driver.page_source
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, page_source)
            
            # Filter out common non-contact emails
            excluded_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'google.com', 'freelancermap.de']
            valid_emails = [email for email in emails if not any(domain in email for domain in excluded_domains)]
            
            return valid_emails[0] if valid_emails else ""
            
        except Exception as e:
            print(f"Error extracting contact info: {str(e)}")
            return ""
            
    def go_to_next_page(self, driver):
        try:
            # Look for next page button
            next_selectors = [
                "a[rel='next']",
                ".pagination .next",
                ".pager .next",
                "a:contains('Weiter')",
                "a:contains('Nächste')"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if next_button.is_enabled():
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(3)  # Wait for page to load
                        return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"Error navigating to next page: {str(e)}")
            return False
            
    def search_projects_by_keywords(self, keywords, location="", max_results=50):
        """Search for projects with specific keywords"""
        projects = []
        driver = None
        
        try:
            driver = self.setup_driver()
            
            # Build search URL
            search_params = {
                'q': ' '.join(keywords),
                'location': location
            }
            
            search_url = f"{self.base_url}/projektboerse/suche"
            driver.get(search_url)
            
            # Fill search form
            try:
                search_input = driver.find_element(By.CSS_SELECTOR, "input[name='q'], input[type='search']")
                search_input.clear()
                search_input.send_keys(' '.join(keywords))
                
                if location:
                    location_input = driver.find_element(By.CSS_SELECTOR, "input[name='location']")
                    location_input.clear()
                    location_input.send_keys(location)
                    
                # Submit search
                search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .search-button")
                search_button.click()
                
                time.sleep(3)  # Wait for results
                
            except Exception as e:
                print(f"Could not perform search: {str(e)}")
                
            # Extract results
            project_links = self.extract_project_links(driver)
            
            for link in project_links[:max_results]:
                try:
                    project_data = self.scrape_project_details(driver, link)
                    if project_data:
                        projects.append(project_data)
                        
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error in keyword search: {str(e)}")
            
        finally:
            if driver:
                driver.quit()
                
        return projects