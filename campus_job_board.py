import json
import os
from enum import Enum
import datetime

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
        
        # Validate and fix data integrity issues
        self.validate_data_integrity()
        
        print(f"🚀 JobBoard initialized with {len(self.users)} users, {len(self.jobs)} jobs, {len(self.applications)} applications")
    
    def _load_json(self, filename, default):
        """Load data from JSON file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded {len(data) if isinstance(data, list) else 'data'} items from {filename}")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                print(f"❌ Error loading {filename}: {e}")
                return default
        else:
            print(f"📁 File {filename} not found, using default data")
        return default
    
    def _save_json(self, filename, data):
        """Save data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(data) if isinstance(data, list) else 'data'} items to {filename}")
            return True
        except IOError as e:
            print(f"❌ Error saving {filename}: {e}")
            return False
    
    def save_data(self):
        """Save all data to JSON files"""
        print("🔄 Saving all data to JSON files...")
        success = True
        success &= self._save_json(self.users_file, self.users)
        success &= self._save_json(self.jobs_file, self.jobs)
        success &= self._save_json(self.applications_file, self.applications)
        
        if success:
            print("✅ All data saved successfully!")
        else:
            print("⚠️ Some data may not have been saved properly")
        return success
    
    def _initialize_default_data(self):
        """Initialize with default admin and sample data"""
        print("🔧 Initializing default data...")
        
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
    
    def add_user(self, user_data):
        """Add a new user and auto-save"""
        print(f"🔍 ADD_USER DEBUG: Adding user data: {user_data}")
        print(f"🔐 ADD_USER DEBUG: Password field present: {'password' in user_data}")
        
        # Validate required fields
        if 'email' not in user_data or 'password' not in user_data:
            print(f"❌ ADD_USER ERROR: Missing required fields in user_data")
            return False
        
        self.users.append(user_data)
        success = self._save_json(self.users_file, self.users)
        
        if success:
            print(f"👤 Added new user: {user_data.get('email', 'Unknown')}")
            # Verify the save by reading back
            saved_data = self._load_json(self.users_file, [])
            saved_user = next((u for u in saved_data if u['email'] == user_data['email']), None)
            if saved_user and 'password' in saved_user:
                print(f"✅ ADD_USER VERIFY: User saved correctly with password field")
            else:
                print(f"❌ ADD_USER ERROR: User saved but password field missing!")
        else:
            print(f"❌ ADD_USER ERROR: Failed to save user data")
        
        return success
    
    def add_job(self, job_data):
        """Add a new job and auto-save"""
        self.jobs.append(job_data)
        self._save_json(self.jobs_file, self.jobs)
        print(f"💼 Added new job: {job_data.get('title', 'Unknown')}")
    
    def add_application(self, app_data):
        """Add a new application and auto-save"""
        self.applications.append(app_data)
        self._save_json(self.applications_file, self.applications)
        print(f"📝 Added new application for job ID: {app_data.get('job_id', 'Unknown')}")
    
    def update_user(self, user_id, updates):
        """Update user data and auto-save"""
        for user in self.users:
            if user['id'] == user_id:
                user.update(updates)
                self._save_json(self.users_file, self.users)
                print(f"👤 Updated user: {user.get('email', 'Unknown')}")
                return True
        return False
    
    def update_job(self, job_id, updates):
        """Update job data and auto-save"""
        for job in self.jobs:
            if job['id'] == job_id:
                job.update(updates)
                self._save_json(self.jobs_file, self.jobs)
                print(f"💼 Updated job: {job.get('title', 'Unknown')}")
                return True
        return False
    
    def update_application(self, app_id, updates):
        """Update application data and auto-save"""
        for app in self.applications:
            if app['id'] == app_id:
                app.update(updates)
                self._save_json(self.applications_file, self.applications)
                print(f"📝 Updated application ID: {app_id}")
                return True
        return False
    
    def get_next_user_id(self):
        """Get the next available user ID"""
        return max([user['id'] for user in self.users], default=0) + 1
    
    def get_next_job_id(self):
        """Get the next available job ID"""
        return max([job['id'] for job in self.jobs], default=0) + 1
    
    def get_next_application_id(self):
        """Get the next available application ID"""
        return max([app['id'] for app in self.applications], default=0) + 1
    
    def backup_data(self):
        """Create backup files with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_files = [
            (self.users_file, f"users_backup_{timestamp}.json"),
            (self.jobs_file, f"jobs_backup_{timestamp}.json"),
            (self.applications_file, f"applications_backup_{timestamp}.json")
        ]
        
        for original, backup in backup_files:
            if os.path.exists(original):
                try:
                    with open(original, 'r', encoding='utf-8') as src:
                        data = json.load(src)
                    with open(backup, 'w', encoding='utf-8') as dst:
                        json.dump(data, dst, indent=2, ensure_ascii=False)
                    print(f"📦 Created backup: {backup}")
                except Exception as e:
                    print(f"❌ Failed to create backup {backup}: {e}")
        
        print("✅ Data backup completed!")
    
    def fix_users_without_passwords(self):
        """Fix users that are missing password fields"""
        print("🔧 Checking for users without passwords...")
        fixed_count = 0
        
        for user in self.users:
            if 'password' not in user or user['password'] is None:
                print(f"⚠️ Found user without password: {user['email']} (ID: {user['id']})")
                # Set a temporary password - user will need to reset
                user['password'] = 'temp123'
                fixed_count += 1
                print(f"🔧 Set temporary password for user: {user['email']}")
        
        if fixed_count > 0:
            self._save_json(self.users_file, self.users)
            print(f"✅ Fixed {fixed_count} users with missing passwords")
        else:
            print("✅ All users have passwords")
        
        return fixed_count
    
    def validate_data_integrity(self):
        """Validate data integrity and fix issues"""
        print("🔍 Validating data integrity...")
        
        # Check users
        users_fixed = self.fix_users_without_passwords()
        
        # Check for duplicate IDs
        user_ids = [user['id'] for user in self.users]
        if len(user_ids) != len(set(user_ids)):
            print("⚠️ Duplicate user IDs found!")
        
        job_ids = [job['id'] for job in self.jobs]
        if len(job_ids) != len(set(job_ids)):
            print("⚠️ Duplicate job IDs found!")
        
        app_ids = [app['id'] for app in self.applications]
        if len(app_ids) != len(set(app_ids)):
            print("⚠️ Duplicate application IDs found!")
        
        print("✅ Data integrity validation completed")
        return users_fixed

