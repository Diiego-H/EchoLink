import axios from 'axios'

export default axios.create({
  baseURL: process.env.PLAYWRIGHT_BACKEND_URL || 'http://localhost:8000',
  headers: {
    'Content-type': 'application/json'
  }
})

