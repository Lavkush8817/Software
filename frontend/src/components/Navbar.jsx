import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  const getDashboardLink = () => {
    if (!user) return null
    
    switch (user.role) {
      case 'student':
        return <Link to="/student/dashboard">Student Dashboard</Link>
      case 'company':
        return <Link to="/company/dashboard">Company Dashboard</Link>
      case 'admin':
        return <Link to="/admin/dashboard">Admin Dashboard</Link>
      default:
        return null
    }
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          🎓 Campus Job Board
        </Link>
        <div className="navbar-links">
          <Link to="/jobs">Browse Jobs</Link>
          {user ? (
            <>
              {getDashboardLink()}
              <span className="navbar-user">Welcome, {user.name || user.company_name || user.email}!</span>
              <button onClick={handleLogout} className="btn btn-outline">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

