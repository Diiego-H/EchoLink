import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv'

// Load environment variables from .env file
dotenv.config()

// Filter and extract all VITE_ prefixed environment variables
const viteEnvVariables = Object.keys(process.env)
  .filter(key => key.startsWith('VITE_'))
  .reduce((env, key) => {
    env[key] = process.env[key]
    return env
  }, {})

export default defineConfig({
  plugins: [vue()],
  test: {
    include: ['src/tests/**/*.test.js'], // Adjust this pattern to match your test files
    globals: true,
    environment: 'jsdom',
  },
  // Spread the VITE_ prefixed variables into the config
  ...viteEnvVariables
});