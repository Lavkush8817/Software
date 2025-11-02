import React, { useState, useEffect } from 'react'
import { adminAPI, jobsAPI } from '../services/api'
import './Dashboard.css'

function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('companies')
  const [unverifiedCompanies, setUnverifiedCompanies] = useState([])
  const [pendingJobs, setPendingJobs] = useState([])
  const [allApplications, setAllApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    loadData()
  }, [activeTab])

  const loadData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'companies') {
        const res = await adminAPI.getUnverifiedCompanies()
        setUnverifiedCompanies(res.data)
      } else if (activeTab === 'jobs') {
        const res = await adminAPI.getPendingJobs()
        setPendingJobs(res.data)
      } else if (activeTab === 'applications') {
        const res = await adminAPI.getAllApplications()
        setAllApplications(res.data)
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load data' })
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyCompany = async (companyId) => {
    try {
      await adminAPI.verifyCompany(companyId)
      setMessage({ type: 'success', text: 'Company verified successfully' })
      loadData()
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to verify company' })
    }
  }

  const handleApproveJob = async (jobId, action) => {
    try {
      await adminAPI.approveJob(jobId, action)
      setMessage({ type: 'success', text: `Job ${action === 'approve' ? 'approved' : 'rejected'} successfully` })
      loadData()
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to update job status' })
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

  return (
    <div className="container">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="tabs">
        <button
          className={activeTab === 'companies' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('companies')}
        >
          Verify Companies
        </button>
        <button
          className={activeTab === 'jobs' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('jobs')}
        >
          Approve Jobs
        </button>
        <button
          className={activeTab === 'applications' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('applications')}
        >
          All Applications
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          {activeTab === 'companies' && (
            <div className="dashboard-section">
              <h2>Companies Pending Verification</h2>
              {unverifiedCompanies.length === 0 ? (
                <div className="card">
                  <p>No companies pending verification.</p>
                </div>
              ) : (
                <div className="companies-list">
                  {unverifiedCompanies.map(company => (
                    <div key={company.id} className="card">
                      <div className="company-header">
                        <h3>{company.company_name}</h3>
                        <button
                          onClick={() => handleVerifyCompany(company.id)}
                          className="btn btn-success"
                        >
                          Verify Company
                        </button>
                      </div>
                      <div className="company-details">
                        <div><strong>Email:</strong> {company.email}</div>
                        <div><strong>Description:</strong> {company.company_description}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'jobs' && (
            <div className="dashboard-section">
              <h2>Jobs Pending Approval</h2>
              {pendingJobs.length === 0 ? (
                <div className="card">
                  <p>No jobs pending approval.</p>
                </div>
              ) : (
                <div className="jobs-list">
                  {pendingJobs.map(job => (
                    <div key={job.id} className="job-card">
                      <div className="job-header">
                        <h3>{job.title}</h3>
                        {getStatusBadge(job.status)}
                      </div>
                      <div className="job-details">
                        <div><strong>Company:</strong> {job.company_name}</div>
                        <div><strong>Type:</strong> {job.type}</div>
                        <div><strong>Location:</strong> {job.location}</div>
                        <div><strong>Deadline:</strong> {job.deadline}</div>
                        <div><strong>Description:</strong> {job.description}</div>
                        <div><strong>Requirements:</strong> {job.requirements}</div>
                      </div>
                      <div className="job-actions">
                        <button
                          onClick={() => handleApproveJob(job.id, 'approve')}
                          className="btn btn-success"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => handleApproveJob(job.id, 'reject')}
                          className="btn btn-danger"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'applications' && (
            <div className="dashboard-section">
              <h2>All Applications</h2>
              {allApplications.length === 0 ? (
                <div className="card">
                  <p>No applications yet.</p>
                </div>
              ) : (
                <div className="applications-list">
                  {allApplications.map(app => (
                    <div key={app.id} className="application-card">
                      <div className="application-header">
                        <h3>{app.job?.title || 'Job'}</h3>
                        {getStatusBadge(app.status)}
                      </div>
                      <div className="application-details">
                        <div><strong>Company:</strong> {app.job?.company_name || 'N/A'}</div>
                        <div><strong>Student:</strong> {app.student_name}</div>
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
          )}
        </>
      )}
    </div>
  )
}

export default AdminDashboard

