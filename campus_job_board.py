import json
import os
from enum import Enum

class UserRole(Enum):
    STUDENT = "student"
    COMPANY = "company"
    ADMIN = "admin"

class JobType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"

class ApplicationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class JobBoard:
    def __init__(self):
        self.users_file = "users.json"
        self.jobs_file = "jobs.json"
        self.applications_file = "applications.json"
        
        # Initialize data storage
        self.users = self._load_json(self.users_file, [])
        self.jobs = self._load_json(self.jobs_file, [])
        self.applications = self._load_json(self.applications_file, [])
        
        # Initialize with default admin if no users exist
        if not self.users:
            self._initialize_default_data()
    
    def _load_json(self, filename, default):
        """Load data from JSON file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return default
        return default
    
    def _save_json(self, filename, data):
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving {filename}: {e}")
    
    def save_data(self):
        """Save all data to JSON files"""
        self._save_json(self.users_file, self.users)
        self._save_json(self.jobs_file, self.jobs)
        self._save_json(self.applications_file, self.applications)
    
    def _initialize_default_data(self):
        """Initialize with default admin and sample data"""
        import datetime
        
        # Default admin user
        admin_user = {
            'id': 1,
            'email': 'admin@campus.edu',
            'password': 'admin123',
            'role': UserRole.ADMIN.value,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Default verified company
        company_user = {
            'id': 2,
            'email': 'techcorp@example.com',
            'password': 'company123',
            'role': UserRole.COMPANY.value,
            'company_name': 'Tech Corp',
            'company_description': 'Leading technology company',
            'verified': True,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Default student user
        student_user = {
            'id': 3,
            'email': 'student@campus.edu',
            'password': 'student123',
            'role': UserRole.STUDENT.value,
            'name': 'John Doe',
            'college': 'Campus University',
            'graduation_year': '2024',
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self.users = [admin_user, company_user, student_user]
        self.jobs = []
        self.applications = []
        
        self.save_data()

