import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { jobsAPI, applicationsAPI } from '../services/api'
import './Dashboard.css'

function CompanyDashboard() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('jobs')
  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [showJobForm, setShowJobForm] = useState(false)
  const [jobForm, setJobForm] = useState({
    title: '',
    type: 'internship',
    description: '',
    requirements: '',
    location: '',
    deadline: ''
  })
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    if (activeTab === 'jobs') {
      loadJobs()
    } else {
      loadApplications()
    }
  }, [activeTab])

  const loadJobs = async () => {
    try {
      const res = await jobsAPI.getMyJobs()
      setJobs(res.data)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load jobs' })
    } finally {
      setLoading(false)
    }
  }

  const loadApplications = async () => {
    try {
      const res = await applicationsAPI.getMyApplications()
      setApplications(res.data)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load applications' })
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitJob = async (e) => {
    e.preventDefault()
    setMessage({ type: '', text: '' })

    if (!user?.verified) {
      setMessage({ type: 'error', text: 'Your company account needs to be verified by admin before posting jobs!' })
      return
    }

    try {
      await jobsAPI.createJob(jobForm)
      setMessage({ type: 'success', text: 'Job posted successfully! Waiting for admin approval.' })
      setJobForm({
        title: '',
        type: 'internship',
        description: '',
        requirements: '',
        location: '',
        deadline: ''
      })
      setShowJobForm(false)
      loadJobs()
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to post job' })
    }
  }

  const handleUpdateApplicationStatus = async (appId, status) => {
    try {
      await applicationsAPI.updateApplicationStatus(appId, status)
      setMessage({ type: 'success', text: 'Application status updated' })
      loadApplications()
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to update status' })
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

  if (!user?.verified) {
    return (
      <div className="container">
        <div className="card">
          <h2>Account Verification Required</h2>
          <p>Your company account needs to be verified by an admin before you can post jobs. Please wait for verification.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>Company Dashboard</h1>
        <button onClick={() => setShowJobForm(!showJobForm)} className="btn btn-primary">
          {showJobForm ? 'Cancel' : 'Post New Job'}
        </button>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {showJobForm && (
        <div className="card">
          <h2>Post New Job</h2>
          <form onSubmit={handleSubmitJob}>
            <div className="input-group">
              <label>Job Title</label>
              <input
                type="text"
                value={jobForm.title}
                onChange={(e) => setJobForm({ ...jobForm, title: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label>Job Type</label>
              <select
                value={jobForm.type}
                onChange={(e) => setJobForm({ ...jobForm, type: e.target.value })}
                required
              >
                <option value="internship">Internship</option>
                <option value="fulltime">Full Time</option>
                <option value="parttime">Part Time</option>
              </select>
            </div>
            <div className="input-group">
              <label>Description</label>
              <textarea
                value={jobForm.description}
                onChange={(e) => setJobForm({ ...jobForm, description: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label>Requirements</label>
              <textarea
                value={jobForm.requirements}
                onChange={(e) => setJobForm({ ...jobForm, requirements: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label>Location</label>
              <input
                type="text"
                value={jobForm.location}
                onChange={(e) => setJobForm({ ...jobForm, location: e.target.value })}
                required
              />
            </div>
            <div className="input-group">
              <label>Deadline (YYYY-MM-DD)</label>
              <input
                type="text"
                value={jobForm.deadline}
                onChange={(e) => setJobForm({ ...jobForm, deadline: e.target.value })}
                placeholder="2024-12-31"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Post Job
            </button>
          </form>
        </div>
      )}

      <div className="tabs">
        <button
          className={activeTab === 'jobs' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('jobs')}
        >
          My Jobs
        </button>
        <button
          className={activeTab === 'applications' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('applications')}
        >
          Applications
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          {activeTab === 'jobs' && (
            <div className="dashboard-section">
              <h2>My Posted Jobs</h2>
              {jobs.length === 0 ? (
                <div className="card">
                  <p>You haven't posted any jobs yet.</p>
                </div>
              ) : (
                <div className="jobs-list">
                  {jobs.map(job => (
                    <div key={job.id} className="job-card">
                      <div className="job-header">
                        <h3>{job.title}</h3>
                        {getStatusBadge(job.status)}
                      </div>
                      <div className="job-details">
                        <div><strong>Type:</strong> {job.type}</div>
                        <div><strong>Location:</strong> {job.location}</div>
                        <div><strong>Deadline:</strong> {job.deadline}</div>
                        <div><strong>Status:</strong> {job.status}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'applications' && (
            <div className="dashboard-section">
              <h2>Applications for My Jobs</h2>
              {applications.length === 0 ? (
                <div className="card">
                  <p>No applications for your jobs yet.</p>
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
                        <div><strong>Applicant:</strong> {app.student_name}</div>
                        <div><strong>Applied:</strong> {new Date(app.applied_at).toLocaleDateString()}</div>
                        {app.cover_letter && (
                          <div className="cover-letter">
                            <strong>Cover Letter:</strong>
                            <p>{app.cover_letter}</p>
                          </div>
                        )}
                      </div>
                      {app.status === 'pending' && (
                        <div className="application-actions">
                          <button
                            onClick={() => handleUpdateApplicationStatus(app.id, 'approved')}
                            className="btn btn-success"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleUpdateApplicationStatus(app.id, 'rejected')}
                            className="btn btn-danger"
                          >
                            Reject
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default CompanyDashboard

