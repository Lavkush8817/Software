# Campus Job Board

A full-stack job board application connecting students with job opportunities from verified companies.

## Features

### For Students
- Browse available jobs
- Apply for jobs with cover letters
- Track application status
- View application history

### For Companies
- Post job listings (after admin verification)
- View applications for posted jobs
- Approve or reject applications
- Manage job listings

### For Admins
- Verify company accounts
- Approve or reject job postings
- View all applications
- Manage platform content

## Tech Stack

### Backend
- Python 3.x
- Flask (REST API)
- JSON file storage

### Frontend
- React 18
- React Router
- Vite
- Axios

## Project Structure

```
RO/
├── campus_job_board.py    # Core backend logic
├── app.py                 # Flask REST API wrapper
├── requirements.txt       # Python dependencies
├── users.json            # User data storage
├── jobs.json             # Job listings storage
├── applications.json     # Applications storage
└── frontend/             # React frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── contexts/     # React contexts
    │   ├── services/     # API services
    │   └── App.jsx       # Main app component
    └── package.json      # Node dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask API server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### Default Accounts

The system comes with sample accounts:

**Admin:**
- Email: `admin@campus.edu`
- Password: `admin123`

**Company:**
- Email: `techcorp@example.com`
- Password: `company123`

**Student:**
- Email: `student@campus.edu`
- Password: `student123`

### Workflow

1. **Company Registration**: Companies register and wait for admin verification
2. **Admin Verification**: Admin verifies company accounts
3. **Job Posting**: Verified companies can post jobs
4. **Job Approval**: Admin approves/rejects job postings
5. **Student Applications**: Students browse and apply for approved jobs
6. **Application Review**: Companies review and approve/reject applications

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/me` - Get current user info

### Jobs
- `GET /api/jobs` - Get all approved jobs
- `GET /api/jobs/:id` - Get specific job
- `POST /api/jobs` - Create new job (company only)
- `GET /api/jobs/my` - Get company's jobs

### Applications
- `POST /api/applications` - Apply for job (student only)
- `GET /api/applications/my` - Get user's applications
- `PUT /api/applications/:id/status` - Update application status (company only)

### Admin
- `GET /api/admin/companies` - Get unverified companies
- `POST /api/admin/companies/:id/verify` - Verify company
- `GET /api/admin/jobs` - Get pending jobs
- `POST /api/admin/jobs/:id/approve` - Approve/reject job
- `GET /api/admin/applications` - Get all applications

## Development

### Running in Development Mode

Backend:
```bash
python app.py
```

Frontend:
```bash
cd frontend
npm run dev
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

## Notes

- Passwords are stored in plain text (for demo purposes). In production, use proper password hashing.
- Session management uses simple in-memory storage. In production, use JWT tokens or proper session management.
- Data is stored in JSON files. For production, use a proper database.

## License

This project is for educational purposes.

