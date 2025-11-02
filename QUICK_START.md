# 🚀 Quick Start Guide

## How to Run the Application

You need to run **TWO servers** - one for the backend (Flask API) and one for the frontend (React app).

---

## Step-by-Step Instructions

### Terminal 1: Start the Backend (Flask API)

1. Open a terminal window
2. Navigate to the project root:
   ```bash
   cd /Users/lavkushkumardubey/Desktop/RO
   ```

3. Start the Flask server:
   ```bash
   python3 app.py
   ```

   You should see output like:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

   ✅ **Backend is running on http://localhost:5000**

---

### Terminal 2: Start the Frontend (React App)

1. Open a **NEW** terminal window (keep the backend terminal running!)
2. Navigate to the frontend directory:
   ```bash
   cd /Users/lavkushkumardubey/Desktop/RO/frontend
   ```

3. Start the React development server:
   ```bash
   npm run dev
   ```

   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:3000/
   ```

   ✅ **Frontend is running on http://localhost:3000**

---

## Access the Application

Open your web browser and go to:

**http://localhost:3000**

You should see the Campus Job Board homepage!

---

## Default Login Accounts

### Admin
- **Email:** `admin@campus.edu`
- **Password:** `admin123`

### Company (Verified)
- **Email:** `techcorp@example.com`
- **Password:** `company123`

### Student
- **Email:** `student@campus.edu`
- **Password:** `student123`

---

## What to Expect

1. **Homepage** - Welcome page with features overview
2. **Register** - Create a new account (Student/Company/Admin)
3. **Login** - Sign in with existing account
4. **Browse Jobs** - View all approved job listings (available to all users)
5. **Dashboards** - Role-specific dashboards after login:
   - **Student**: View your applications
   - **Company**: Post jobs, view applications
   - **Admin**: Verify companies, approve jobs

---

## Troubleshooting

### Backend won't start?
- Make sure port 5000 is not in use
- Check if Flask is installed: `pip3 list | grep Flask`

### Frontend won't start?
- Make sure port 3000 is not in use
- Try deleting `node_modules` and reinstalling: 
  ```bash
  rm -rf node_modules
  npm install
  ```

### Can't connect to backend?
- Make sure the Flask server is running in Terminal 1
- Check that it's running on port 5000
- Make sure CORS is enabled (it should be by default)

---

## Development Mode

Both servers run in **development mode** with hot-reload:
- Backend: Auto-restarts on code changes
- Frontend: Auto-refreshes browser on code changes

Just keep both terminals open and start coding! 🎉










## Quick Command Reference

### One-Line Commands

**Backend (Terminal 1):**
```bash
cd /Users/lavkushkumardubey/Desktop/RO && python3 app.py
```

**Frontend (Terminal 2):**
```bash
cd /Users/lavkushkumardubey/Desktop/RO/frontend && npm run dev
```

### Run Both in Background

If you want to run both servers in the background:

```bash
# Backend in background
cd /Users/lavkushkumardubey/Desktop/RO && python3 app.py &

# Frontend in background  
cd /Users/lavkushkumardubey/Desktop/RO/frontend && npm run dev &
```

**Note:** It's recommended to run them in separate terminal windows so you can see the logs from both servers.