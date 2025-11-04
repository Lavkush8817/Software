import axios from 'axios'

const API_URL = 'https://software-5hmy.onrender.com/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const sessionId = localStorage.getItem('session_id')
  if (sessionId) {
    config.headers.Authorization = sessionId
  }
  return config
})

export const authAPI = {
  login: (email, password) => 
    api.post('/login', { email, password }),
  
  register: (userData) => 
    api.post('/register', userData),
  
  logout: () => 
    api.post('/logout'),
  
  getCurrentUser: () => 
    api.get('/me')
}

export const jobsAPI = {
  getJobs: () => 
    api.get('/jobs'),
  
  getJob: (id) => 
    api.get(`/jobs/${id}`),
  
  createJob: (jobData) => 
    api.post('/jobs', jobData),
  
  getMyJobs: () => 
    api.get('/jobs/my')
}

export const applicationsAPI = {
  createApplication: (applicationData) => 
    api.post('/applications', applicationData),
  
  getMyApplications: () => 
    api.get('/applications/my'),
  
  updateApplicationStatus: (appId, status) => 
    api.put(`/applications/${appId}/status`, { status })
}

export const adminAPI = {
  getUnverifiedCompanies: () => 
    api.get('/admin/companies'),
  
  verifyCompany: (companyId) => 
    api.post(`/admin/companies/${companyId}/verify`),
  
  getPendingJobs: () => 
    api.get('/admin/jobs'),
  
  approveJob: (jobId, action) => 
    api.post(`/admin/jobs/${jobId}/approve`, { action }),
  
  getAllApplications: () => 
    api.get('/admin/applications')
}

export default api

