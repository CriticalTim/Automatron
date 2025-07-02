import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import json
import os
from datetime import datetime
import threading
import schedule
import time

from database import Database
from scraper import FreelancerMapScraper
from email_handler import EmailHandler
from profile_parser import ProfileParser
from matcher import ProjectMatcher


class FreelancerApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Freelancer AutoApply")
        self.root.geometry("1200x800")
        
        self.db = Database()
        self.scraper = FreelancerMapScraper()
        self.email_handler = EmailHandler()
        self.profile_parser = ProfileParser()
        self.matcher = ProjectMatcher()
        
        self.user_profile = None
        self.scraped_projects = []
        self.selected_projects = []
        
        self.setup_ui()
        self.setup_scheduler()
        
    def setup_ui(self):
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.setup_main_tab()
        self.setup_history_tab()
        
    def setup_main_tab(self):
        main_tab = self.notebook.add("Main")
        
        # Profile section
        profile_frame = ctk.CTkFrame(main_tab)
        profile_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(profile_frame, text="Profile Management", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        upload_frame = ctk.CTkFrame(profile_frame)
        upload_frame.pack(fill="x", padx=10, pady=5)
        
        self.profile_label = ctk.CTkLabel(upload_frame, text="No profile uploaded")
        self.profile_label.pack(side="left", padx=10)
        
        ctk.CTkButton(upload_frame, text="Upload PDF Profile", command=self.upload_profile).pack(side="right", padx=10, pady=5)
        
        # Email login section
        email_frame = ctk.CTkFrame(main_tab)
        email_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(email_frame, text="Email Configuration", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        login_frame = ctk.CTkFrame(email_frame)
        login_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(login_frame, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ctk.CTkEntry(login_frame, width=200)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(login_frame, width=200, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkButton(login_frame, text="Login", command=self.login_email).grid(row=0, column=2, rowspan=2, padx=10, pady=5)
        
        # Scraping section
        scraping_frame = ctk.CTkFrame(main_tab)
        scraping_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scraping_frame, text="Project Scraping", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        button_frame = ctk.CTkFrame(scraping_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(button_frame, text="Scrape Now", command=self.scrape_projects).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Apply to Selected", command=self.apply_to_projects).pack(side="right", padx=5)
        
        # Projects list
        self.projects_frame = ctk.CTkScrollableFrame(scraping_frame)
        self.projects_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def setup_history_tab(self):
        history_tab = self.notebook.add("History")
        
        ctk.CTkLabel(history_tab, text="Application History", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # History list
        self.history_frame = ctk.CTkScrollableFrame(history_tab)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_history()
        
    def upload_profile(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF Profile",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            try:
                self.user_profile = self.profile_parser.parse_pdf(file_path)
                self.profile_label.configure(text=f"Profile loaded: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Profile uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to parse profile: {str(e)}")
                
    def login_email(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
            
        try:
            self.email_handler.login(email, password)
            messagebox.showinfo("Success", "Email login successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Email login failed: {str(e)}")
            
    def scrape_projects(self):
        if not self.user_profile:
            messagebox.showerror("Error", "Please upload your profile first")
            return
            
        def scrape_thread():
            try:
                projects = self.scraper.scrape_projects()
                matched_projects = self.matcher.match_projects(projects, self.user_profile)
                
                self.root.after(0, lambda: self.display_projects(matched_projects))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Scraping failed: {str(e)}"))
                
        threading.Thread(target=scrape_thread, daemon=True).start()
        
    def display_projects(self, projects):
        # Clear previous projects
        for widget in self.projects_frame.winfo_children():
            widget.destroy()
            
        self.scraped_projects = projects
        self.selected_projects = []
        
        for i, project in enumerate(projects):
            project_frame = ctk.CTkFrame(self.projects_frame)
            project_frame.pack(fill="x", padx=5, pady=5)
            
            var = tk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                project_frame,
                text="",
                variable=var,
                command=lambda idx=i, v=var: self.toggle_project_selection(idx, v.get())
            )
            checkbox.pack(side="left", padx=10, pady=10)
            
            info_frame = ctk.CTkFrame(project_frame)
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            
            title_label = ctk.CTkLabel(info_frame, text=project['title'], font=ctk.CTkFont(size=14, weight="bold"))
            title_label.pack(anchor="w", padx=10, pady=2)
            
            desc_label = ctk.CTkLabel(info_frame, text=project['description'][:200] + "...")
            desc_label.pack(anchor="w", padx=10, pady=2)
            
            match_label = ctk.CTkLabel(info_frame, text=f"Match Score: {project['match_score']:.1%}", 
                                     text_color="green" if project['match_score'] > 0.7 else "orange")
            match_label.pack(anchor="w", padx=10, pady=2)
            
    def toggle_project_selection(self, index, selected):
        if selected and index not in self.selected_projects:
            self.selected_projects.append(index)
        elif not selected and index in self.selected_projects:
            self.selected_projects.remove(index)
            
    def apply_to_projects(self):
        if not self.selected_projects:
            messagebox.showwarning("Warning", "Please select projects to apply to")
            return
            
        if not self.email_handler.is_logged_in():
            messagebox.showerror("Error", "Please login to your email first")
            return
            
        # Confirmation dialog
        selected_count = len(self.selected_projects)
        if not messagebox.askyesno("Confirm", f"Apply to {selected_count} selected projects?"):
            return
            
        def apply_thread():
            success_count = 0
            for idx in self.selected_projects:
                project = self.scraped_projects[idx]
                
                # Check if already applied
                if self.db.check_already_applied(project['url']):
                    continue
                    
                try:
                    email_content = self.generate_application_email(project)
                    self.email_handler.send_email(project['contact_email'], 
                                                project['title'], email_content)
                    
                    # Save to database
                    self.db.save_application(project, email_content)
                    success_count += 1
                    
                except Exception as e:
                    print(f"Failed to apply to {project['title']}: {str(e)}")
                    
            self.root.after(0, lambda: self.show_application_results(success_count))
            self.root.after(0, self.load_history)
            
        threading.Thread(target=apply_thread, daemon=True).start()
        
    def generate_application_email(self, project):
        # Simple email template - can be enhanced with AI
        return f"""Dear Hiring Manager,

I am interested in your project "{project['title']}" on FreelancerMap.

Based on my experience in {', '.join(self.user_profile['skills'][:3])}, I believe I can deliver excellent results for this project.

I would be happy to discuss the details further.

Best regards,
{self.user_profile.get('name', 'Your Name')}"""
        
    def show_application_results(self, success_count):
        messagebox.showinfo("Results", f"Successfully applied to {success_count} projects!")
        
    def load_history(self):
        # Clear previous history
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        applications = self.db.get_application_history()
        
        for app in applications:
            app_frame = ctk.CTkFrame(self.history_frame)
            app_frame.pack(fill="x", padx=5, pady=5)
            
            title_label = ctk.CTkLabel(app_frame, text=app['title'], font=ctk.CTkFont(size=14, weight="bold"))
            title_label.pack(anchor="w", padx=10, pady=2)
            
            date_label = ctk.CTkLabel(app_frame, text=f"Applied: {app['applied_date']}")
            date_label.pack(anchor="w", padx=10, pady=2)
            
            email_preview = app['email_content'][:100] + "..."
            email_label = ctk.CTkLabel(app_frame, text=email_preview)
            email_label.pack(anchor="w", padx=10, pady=2)
            
    def setup_scheduler(self):
        schedule.every().week.do(self.scheduled_scrape)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(3600)  # Check every hour
                
        threading.Thread(target=run_scheduler, daemon=True).start()
        
    def scheduled_scrape(self):
        if self.user_profile and self.email_handler.is_logged_in():
            self.scrape_projects()
            
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FreelancerApp()
    app.run()