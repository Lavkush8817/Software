import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { jobsAPI, applicationsAPI } from '../services/api'
import './JobsList.css'

function JobsList() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [applyingJobId, setApplyingJobId] = useState(null)
  const [coverLetter, setCoverLetter] = useState('')
  const [showApplyModal, setShowApplyModal] = useState(false)
  const [selectedJob, setSelectedJob] = useState(null)
  const [message, setMessage] = useState({ type: '', text: '' })
  
  const { user } = useAuth()

  useEffect(() => {
    loadJobs()
  }, [])

  const loadJobs = async () => {
    try {
      const res = await jobsAPI.getJobs()
      setJobs(res.data)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load jobs' })
    } finally {
      setLoading(false)
    }
  }

  const handleApply = async () => {
    if (!user || user.role !== 'student') {
      setMessage({ type: 'error', text: 'Only students can apply for jobs' })
      return
    }

    setApplyingJobId(selectedJob.id)
    setMessage({ type: '', text: '' })

    try {
      await applicationsAPI.createApplication({
        job_id: selectedJob.id,
        cover_letter: coverLetter
      })
      setMessage({ type: 'success', text: 'Application submitted successfully!' })
      setShowApplyModal(false)
      setCoverLetter('')
      setSelectedJob(null)
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.error || 'Failed to submit application' })
    } finally {
      setApplyingJobId(null)
    }
  }

  const openApplyModal = (job) => {
    setSelectedJob(job)
    setShowApplyModal(true)
    setCoverLetter('')
    setMessage({ type: '', text: '' })
  }

  if (loading) {
    return <div className="loading">Loading jobs...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1>Available Jobs</h1>
        {user && user.role === 'student' && (
          <Link to="/student/dashboard" className="btn btn-primary">
            View My Applications
          </Link>
        )}
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {jobs.length === 0 ? (
        <div className="card">
          <p>No jobs available at the moment. Check back later!</p>
        </div>
      ) : (
        <div className="jobs-grid">
          {jobs.map(job => (
            <div key={job.id} className="job-card">
              <div className="job-header">
                <h2>{job.title}</h2>
                <span className={`job-type ${job.type}`}>{job.type}</span>
              </div>
              <div className="job-company">{job.company_name}</div>
              <div className="job-location">📍 {job.location}</div>
              <p className="job-description">{job.description}</p>
              <div className="job-details">
                <div><strong>Requirements:</strong> {job.requirements}</div>
                <div><strong>Deadline:</strong> {job.deadline}</div>
              </div>
              {user && user.role === 'student' && (
                <button
                  onClick={() => openApplyModal(job)}
                  className="btn btn-primary"
                >
                  Apply Now
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {showApplyModal && (
        <div className="modal-overlay" onClick={() => setShowApplyModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Apply for {selectedJob?.title}</h2>
            <div className="input-group">
              <label>Cover Letter (optional)</label>
              <textarea
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                placeholder="Tell us why you're interested in this position..."
              />
            </div>
            <div className="modal-actions">
              <button
                onClick={handleApply}
                className="btn btn-primary"
                disabled={applyingJobId === selectedJob?.id}
              >
                {applyingJobId === selectedJob?.id ? 'Submitting...' : 'Submit Application'}
              </button>
              <button
                onClick={() => setShowApplyModal(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default JobsList

