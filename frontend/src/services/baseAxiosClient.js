import axios from 'axios'

// A client with no extra headers.

export default axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-type': 'application/json'
  }
})


