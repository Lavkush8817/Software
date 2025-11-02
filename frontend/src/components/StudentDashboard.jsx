import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { applicationsAPI } from '../services/api'
import './Dashboard.css'

function StudentDashboard() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadApplications()
  }, [])

  const loadApplications = async () => {
    try {
      const res = await applicationsAPI.getMyApplications()
      setApplications(res.data)
    } catch (error) {
      console.error('Failed to load applications:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const statusClass = {
      pending: 'status-pending',
      approved: 'status-approved',
      rejected: 'status-rejected'
    }[status] || 'status-pending'

    return <span className={`status-badge ${statusClass}`}>{status}</span>
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>Student Dashboard</h1>
        <div>
          <Link to="/jobs" className="btn btn-primary">
            Browse Jobs
          </Link>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>My Applications</h2>
        {applications.length === 0 ? (
          <div className="card">
            <p>You haven't applied for any jobs yet.</p>
            <Link to="/jobs" className="btn btn-primary" style={{ marginTop: '20px', display: 'inline-block' }}>
              Browse Available Jobs
            </Link>
          </div>
        ) : (
          <div className="applications-list">
            {applications.map(app => (
              <div key={app.id} className="application-card">
                <div className="application-header">
                  <h3>{app.job?.title || 'Job'}</h3>
                  {getStatusBadge(app.status)}
                </div>
                <div className="application-details">
                  <div><strong>Company:</strong> {app.job?.company_name || 'N/A'}</div>
                  <div><strong>Applied:</strong> {new Date(app.applied_at).toLocaleDateString()}</div>
                  {app.cover_letter && (
                    <div className="cover-letter">
                      <strong>Cover Letter:</strong>
                      <p>{app.cover_letter}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default StudentDashboard

