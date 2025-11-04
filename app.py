from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from campus_job_board import JobBoard, UserRole, JobType, ApplicationStatus
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

job_board = JobBoard()

# Session management (simple in-memory for demo, use JWT in production)
sessions = {}

def get_current_user():
    """Get current user from session"""
    session_id = request.headers.get('Authorization')
    if session_id and session_id in sessions:
        user_id = sessions[session_id]
        for user in job_board.users:
            if user['id'] == user_id:
                return user
    return None

# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    print(f"🔍 REGISTER DEBUG: Received data: {data}")
    
    # Validate required fields
    if not data.get('email') or not data.get('password') or not data.get('role'):
        print(f"❌ REGISTER ERROR: Missing required fields - email: {data.get('email')}, password: {'***' if data.get('password') else None}, role: {data.get('role')}")
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    existing_user = next((user for user in job_board.users if user['email'] == data['email']), None)
    if existing_user:
        print(f"❌ REGISTER ERROR: User already exists with email: {data['email']}")
        return jsonify({'error': 'User with this email already exists'}), 400
    
    user_data = {
        'id': job_board.get_next_user_id(),
        'email': data['email'],
        'password': data['password'],  # In real app, hash this!
        'role': data['role'],
        'created_at': datetime.datetime.now().isoformat()
    }
    
    # Add role-specific fields
    if data['role'] == UserRole.STUDENT.value:
        user_data['name'] = data.get('name', '')
        user_data['college'] = data.get('college', '')
        user_data['graduation_year'] = data.get('graduation_year', '')
    elif data['role'] == UserRole.COMPANY.value:
        user_data['company_name'] = data.get('company_name', '')
        user_data['company_description'] = data.get('company_description', '')
        user_data['verified'] = False
    
    print(f"✅ REGISTER DEBUG: Creating user with ID {user_data['id']} and email {user_data['email']}")
    print(f"🔐 REGISTER DEBUG: Password field present: {'password' in user_data}")
    
    # Add user and save
    job_board.add_user(user_data)
    
    # Verify user was saved by reloading data
    job_board.users = job_board._load_json(job_board.users_file, [])
    saved_user = next((user for user in job_board.users if user['email'] == data['email']), None)
    if saved_user:
        print(f"✅ REGISTER SUCCESS: User saved successfully. Password field in saved data: {'password' in saved_user}")
    else:
        print(f"❌ REGISTER ERROR: User not found after saving!")
    
    # Remove password from response
    response_user = user_data.copy()
    response_user.pop('password', None)
    return jsonify({'message': 'Registration successful', 'user': response_user}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    print(f"🔍 LOGIN DEBUG: Attempting login for email: {email}")
    print(f"🔍 LOGIN DEBUG: Total users in memory: {len(job_board.users)}")
    
    # Reload users from file to ensure we have latest data
    job_board.users = job_board._load_json(job_board.users_file, [])
    print(f"🔄 LOGIN DEBUG: Reloaded {len(job_board.users)} users from file")
    
    # Debug: Show all users (without passwords)
    for i, user in enumerate(job_board.users):
        has_password = 'password' in user and user['password'] is not None
        print(f"👤 LOGIN DEBUG: User {i+1}: {user['email']} (ID: {user['id']}, Role: {user['role']}, Has Password: {has_password})")
    
    # Find user by email
    target_user = None
    for user in job_board.users:
        if user['email'] == email:
            target_user = user
            break
    
    if not target_user:
        print(f"❌ LOGIN ERROR: No user found with email: {email}")
        return jsonify({'error': 'Invalid email or password'}), 401
    
    print(f"✅ LOGIN DEBUG: Found user with email: {email}")
    print(f"🔐 LOGIN DEBUG: User has password field: {'password' in target_user}")
    
    if 'password' not in target_user:
        print(f"❌ LOGIN ERROR: User {email} has no password field in database!")
        return jsonify({'error': 'Account data corrupted. Please contact admin.'}), 500
    
    if target_user['password'] != password:
        print(f"❌ LOGIN ERROR: Password mismatch for user: {email}")
        return jsonify({'error': 'Invalid email or password'}), 401
    
    print(f"✅ LOGIN SUCCESS: Authentication successful for user: {email}")
    
    # Create session (in production, use JWT)
    session_id = f"session_{target_user['id']}_{datetime.datetime.now().timestamp()}"
    sessions[session_id] = target_user['id']
    
    # Remove password from response
    user_response = {k: v for k, v in target_user.items() if k != 'password'}
    return jsonify({
        'message': 'Login successful',
        'user': user_response,
        'session_id': session_id
    }), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session_id = request.headers.get('Authorization')
    if session_id and session_id in sessions:
        del sessions[session_id]
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/me', methods=['GET'])
def get_current_user_info():
    """Get current user info"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_response = {k: v for k, v in user.items() if k != 'password'}
    return jsonify(user_response), 200

@app.route('/api/debug/users', methods=['GET'])
def debug_users():
    """Debug endpoint to check user data (remove in production)"""
    # Only allow in development or for admin users
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    debug_info = {
        'total_users': len(job_board.users),
        'users_summary': []
    }
    
    for user in job_board.users:
        user_info = {
            'id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'has_password': 'password' in user and user['password'] is not None,
            'created_at': user.get('created_at', 'Unknown')
        }
        debug_info['users_summary'].append(user_info)
    
    return jsonify(debug_info), 200

# Job endpoints
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all approved jobs"""
    approved_jobs = [job for job in job_board.jobs if job['status'] == 'approved']
    return jsonify(approved_jobs), 200

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Post a new job (company users only)"""
    user = get_current_user()
    if not user or user['role'] != UserRole.COMPANY.value:
        return jsonify({'error': 'Only company users can post jobs'}), 403
    
    if not user.get('verified', False):
        return jsonify({'error': 'Company account needs to be verified'}), 403
    
    data = request.json
    
    job_data = {
        'id': job_board.get_next_job_id(),
        'company_id': user['id'],
        'company_name': user['company_name'],
        'title': data.get('title'),
        'type': data.get('type'),
        'description': data.get('description'),
        'requirements': data.get('requirements'),
        'location': data.get('location'),
        'deadline': data.get('deadline'),
        'status': 'pending',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    job_board.add_job(job_data)
    
    return jsonify({'message': 'Job posted successfully', 'job': job_data}), 201

@app.route('/api/jobs/my', methods=['GET'])
def get_my_jobs():
    """Get company's own jobs"""
    user = get_current_user()
    if not user or user['role'] != UserRole.COMPANY.value:
        return jsonify({'error': 'Access denied'}), 403
    
    my_jobs = [job for job in job_board.jobs if job['company_id'] == user['id']]
    return jsonify(my_jobs), 200

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job"""
    job = next((j for j in job_board.jobs if j['id'] == job_id), None)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job), 200

# Application endpoints
@app.route('/api/applications', methods=['POST'])
def create_application():
    """Apply for a job (student users only)"""
    user = get_current_user()
    if not user or user['role'] != UserRole.STUDENT.value:
        return jsonify({'error': 'Only students can apply for jobs'}), 403
    
    data = request.json
    job_id = data.get('job_id')
    
    # Find job
    job = next((j for j in job_board.jobs if j['id'] == job_id), None)
    if not job or job['status'] != 'approved':
        return jsonify({'error': 'Job not found or not approved'}), 404
    
    # Check if already applied
    existing = next(
        (app for app in job_board.applications 
         if app['job_id'] == job_id and app['student_id'] == user['id']), 
        None
    )
    if existing:
        return jsonify({'error': 'You have already applied for this job'}), 400
    
    application = {
        'id': job_board.get_next_application_id(),
        'job_id': job_id,
        'student_id': user['id'],
        'student_name': user['name'],
        'status': ApplicationStatus.PENDING.value,
        'cover_letter': data.get('cover_letter', ''),
        'applied_at': datetime.datetime.now().isoformat()
    }
    
    job_board.add_application(application)
    
    return jsonify({'message': 'Application submitted successfully', 'application': application}), 201

@app.route('/api/applications/my', methods=['GET'])
def get_my_applications():
    """Get student's own applications"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if user['role'] == UserRole.STUDENT.value:
        my_applications = [app for app in job_board.applications 
                          if app['student_id'] == user['id']]
        # Enrich with job details
        for app in my_applications:
            job = next((j for j in job_board.jobs if j['id'] == app['job_id']), None)
            app['job'] = job
        return jsonify(my_applications), 200
    elif user['role'] == UserRole.COMPANY.value:
        # Get applications for company's jobs
        my_job_ids = [job['id'] for job in job_board.jobs if job['company_id'] == user['id']]
        job_applications = [app for app in job_board.applications if app['job_id'] in my_job_ids]
        # Enrich with job details
        for app in job_applications:
            job = next((j for j in job_board.jobs if j['id'] == app['job_id']), None)
            app['job'] = job
        return jsonify(job_applications), 200
    else:
        return jsonify({'error': 'Invalid role'}), 403

@app.route('/api/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    """Update application status (company users only)"""
    user = get_current_user()
    if not user or user['role'] != UserRole.COMPANY.value:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    status = data.get('status')
    application = next((a for a in job_board.applications if a['id'] == app_id), None)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    # Verify job belongs to company
    job = next((j for j in job_board.jobs if j['id'] == application['job_id']), None)
    if not job or job['company_id'] != user['id']:
        return jsonify({'error': 'Access denied'}), 403
    
    job_board.update_application(app_id, {'status': status})
    
    return jsonify({'message': 'Application status updated', 'application': application}), 200

# Admin endpoints
@app.route('/api/admin/companies', methods=['GET'])
def get_unverified_companies():
    """Get unverified companies"""
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    unverified = [u for u in job_board.users 
                  if u['role'] == UserRole.COMPANY.value and not u.get('verified', False)]
    for company in unverified:
        company.pop('password', None)
    return jsonify(unverified), 200

@app.route('/api/admin/companies/<int:company_id>/verify', methods=['POST'])
def verify_company(company_id):
    """Verify a company"""
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    company = next((u for u in job_board.users if u['id'] == company_id), None)
    if not company or company['role'] != UserRole.COMPANY.value:
        return jsonify({'error': 'Company not found'}), 404
    
    job_board.update_user(company_id, {'verified': True})
    
    company.pop('password', None)
    return jsonify({'message': 'Company verified', 'company': company}), 200

@app.route('/api/admin/jobs', methods=['GET'])
def get_pending_jobs():
    """Get pending jobs"""
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    pending = [job for job in job_board.jobs if job['status'] == 'pending']
    return jsonify(pending), 200

@app.route('/api/admin/jobs/<int:job_id>/approve', methods=['POST'])
def approve_job(job_id):
    """Approve a job"""
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    job = next((j for j in job_board.jobs if j['id'] == job_id), None)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.json
    if data.get('action') == 'approve':
        job['status'] = 'approved'
    elif data.get('action') == 'reject':
        job['status'] = 'rejected'
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    job_board.update_job(job_id, {'status': job['status']})
    return jsonify({'message': 'Job status updated', 'job': job}), 200

@app.route('/api/admin/applications', methods=['GET'])
def get_all_applications():
    """Get all applications (admin only)"""
    user = get_current_user()
    if not user or user['role'] != UserRole.ADMIN.value:
        return jsonify({'error': 'Access denied'}), 403
    
    # Enrich with job details
    apps = job_board.applications.copy()
    for app in apps:
        job = next((j for j in job_board.jobs if j['id'] == app['job_id']), None)
        app['job'] = job
    return jsonify(apps), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    
    # Use production server for Render
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)
