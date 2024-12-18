import { defineConfig } from '@playwright/test';

// Read the base URL and backend URL from environment variables
const baseURL = process.env.PLAYWRIGHT_URL || 'http://localhost';

export default defineConfig({
  testDir: './src/playwright', // Directory where your tests are located
  timeout: 30000, // Maximum time one test can run for
  retries: 2, // Retry failed tests

  use: {
    headless: true, // Run tests in headless mode
    baseURL: baseURL, // Use the environment variable for the base URL
    viewport: { width: 1280, height: 720 }, // Default viewport size
  },
  projects: [
    {
      name: 'Chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'Firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'WebKit',
      use: { browserName: 'webkit' },
    },
  ],
});