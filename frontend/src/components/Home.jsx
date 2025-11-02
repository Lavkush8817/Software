import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Home.css'

function Home() {
  const { user } = useAuth()

  return (
    <div className="home-container">
      <div className="home-hero">
        <h1>Welcome to Campus Job Board</h1>
        <p className="home-subtitle">
          Connect students with opportunities and help companies find the best talent
        </p>
        
        {!user ? (
          <div className="home-actions">
            <Link to="/register" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/jobs" className="btn btn-outline">
              Browse Jobs
            </Link>
          </div>
        ) : (
          <div className="home-actions">
            {user.role === 'student' && (
              <Link to="/student/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            )}
            {user.role === 'company' && (
              <Link to="/company/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            )}
            {user.role === 'admin' && (
              <Link to="/admin/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            )}
            <Link to="/jobs" className="btn btn-outline">
              Browse Jobs
            </Link>
          </div>
        )}
      </div>

      <div className="home-features">
        <div className="feature-card">
          <div className="feature-icon">🎓</div>
          <h3>For Students</h3>
          <p>Find internships and job opportunities tailored for students</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">🏢</div>
          <h3>For Companies</h3>
          <p>Post jobs and connect with talented students from top colleges</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon">✅</div>
          <h3>Verified</h3>
          <p>All companies and jobs are verified by our admin team</p>
        </div>
      </div>
    </div>
  )
}

export default Home

