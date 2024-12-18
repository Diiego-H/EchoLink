# Use the official Node.js image as the base image for building and testing
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Separate stage for running tests
FROM node:18-alpine AS test

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Run tests
CMD ["npm", "run", "lint-test"]

# Use the official Playwright Docker image
FROM mcr.microsoft.com/playwright:v1.48.2-jammy   AS playwright

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Run tests
CMD ["npx", "playwright", "test"]

# Use Caddy to serve the static files
FROM caddy:alpine

# Copy the built files from the build stage
COPY --from=build /app/dist /usr/share/caddy

# Copy the Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Expose port 80
EXPOSE 80

# Start Caddy server
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]