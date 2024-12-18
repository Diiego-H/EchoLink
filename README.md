# EchoLink

University project: Music based Social Media. Final university project involving all the process from the conception of a software product. Introduction to Agile methodologies (SCRUM & KANBAN). This repository is a copy of the one hosted by the university's GitHub Classroom, so the Product Backlog, Sprint Backlog... All the SCRUM documentation is not present.

## Introduction

EchoLink is a full-stack application featuring a FastAPI backend, a Vue.js frontend powered by Vite, and a PostgreSQL database managed with PgAgent. This README provides instructions on how to set up and run the project, as well as guidelines for contributing to the codebase.

## Table of Contents

- [Project Overview](#project-overview)
- [Clone the Repository](#clone-the-repository)
- [Running the Application with Docker Compose](#running-the-application-with-docker-compose)
- [Accessing PgAgent](#accessing-pgagent)
- [Running Frontend and Backend Separately](#running-frontend-and-backend-separately)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running Tests](#running-tests)
  - [Backend Tests](#backend-tests)
  - [Frontend Tests](#frontend-tests)
- [Working Flow](#working-flow)

## Project Overview

EchoLink is designed to provide a seamless user experience with a robust backend and a dynamic frontend. The project leverages FastAPI for its backend services, Vue.js with Vite for the frontend, and PostgreSQL for data storage.

## Clone the Repository

To get started with EchoLink, clone the repository from GitHub:

```bash
git clone https://github.com/UB-ES-2024-F3/EchoLink.git
cd EchoLink
```

## Running the Application with Docker Compose

To build and run the entire application using Docker Compose:

1. **Ensure Docker and Docker Compose are installed on your machine.**

2. **Navigate to the root directory of the project:**

   ```bash
   cd EchoLink
   ```

3. **Build and start the containers:**

   ```bash
   docker-compose up --build
   ```

4. **Access the application:**

   - The frontend will be available at `http://localhost:80`
   - The backend API will be available at `http://localhost:8000`
   - Access pgAdmin for database management at `http://localhost:8001`
     - **Login Credentials:**
       - Email: `admin@admin.com`
       - Password: `admin`

## Accessing PgAgent

If the server does not appear in pgAdmin, you can manually add it by following these steps:

1. **Click on "Add Server":**

2. **In the "General" tab:**
   - Set the **Name** field to `EchoLink`.

3. **In the "Connection" tab:**
   - **Host name/address**: `postgres`
   - **Username**: `user`
   - **Password**: `password`
   - Activate the **Save password** option.

4. **Click "Save"** to add the server.

## Running Frontend and Backend Separately

> [!WARNING]
> When running the frontend and backend separately, you are running them locally and not within Docker containers. 
> This approach is **not recommended** due to potential configuration issues and discrepancies between development and production environments. 
> It is preferable to use Docker Compose to ensure consistency and proper environment setup.

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Navigate to the app folder:**

   ```bash
   cd app
   ```

4. **Change to the local path for the database at database/config.py:**

   ```bash
   URL_DATABASE_LOCAL = "postgresql://user:password@localhost:5432/Echolink"
   ```

   Reminder changing it back when running in docker, the database should be running in docker.

5. **Run the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install the dependencies:**

   ```bash
   npm install
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   ```

## Running Tests

During the application's build process, all tests are automatically executed within the Dockerfiles to ensure integrity. The build will not be complete unless all tests pass successfully. However, if you wish to run the tests during development, you can follow these instructions.

### Backend Tests

For detailed instructions on defining backend unit tests, refer to the `test_dummy.py` file located in the `backend/app/tests` directory or consult the Pytest documentation.

#### Option 1: Running Tests Using Docker UI

1. **Access the Docker Dashboard:**

   Open the Docker Desktop application on your machine. This provides a graphical user interface to manage your Docker containers.

2. **Locate the Backend Container:**

   In the Docker Dashboard, find the container running the backend service. It should be listed among the active containers.

3. **Open a Terminal Session:**

   Use the Docker UI to open a terminal session within the backend container. This option is usually available as a "CLI" or "Terminal" button in the container's details view.

4. **Run Pytest:**

   Once inside the container's terminal, navigate to the directory containing the tests, if needed, and execute Pytest:

   ```bash
   pytest ./tests
   ```

#### Option 2: Running Tests Using Docker Exec

1. **Identify the Backend Container:**

   Start by listing the running containers to find the backend container's ID or name:

   ```bash
   docker ps
   ```

2. **Execute Pytest from Your Host Machine:**

   Use `docker exec` to run Pytest directly from your host machine without entering the container:

   ```bash
   docker exec -it <container_id_or_name> pytest ./tests
   ```

### Frontend Tests

For detailed instructions on defining frontend unit tests, refer to the `dummy.test.js` file located in the `frontend/src/tests` directory or consult the Vitest documentation.

1. **Navigate to the Frontend Directory:**

   Open a terminal and navigate to the frontend directory of your project:

   ```bash
   cd frontend
   ```

2. **Run the Tests:**

   Execute the following command to run the frontend tests:

   ```bash
   npm run test
   ```

### End-to-End Tests

We have used Playwright to implement end-to-end tests, with an example located in `src/playwright/dummy.specs.js`.

#### Running Tests Locally

1. **Set Up Environment Variables:**

   Before running the tests, ensure that your `.env` file in the frontend directory has the following configuration:

   ```env
   VITE_API_URL="http://localhost:8000"
   PLAYWRIGHT_URL="http://frontend:80"
   PLAYWRIGHT_BACKEND_URL="http://backend:8000"
   ```

2. **Navigate to the Frontend Directory:**

   ```bash
   cd frontend
   ```

3. **Run Tests with UI:**

   You can run the tests with a UI to visualize the results:

   ```bash
   npx playwright test --ui
   ```

4. **Run Tests Without UI (Pure Terminal):**

   Alternatively, you can run the tests in the terminal without a UI:

   ```bash
   npx playwright test
   ```

#### Running Tests in Docker

To make the tests work in Docker at the building stage, change the `.env` file in the frontend directory to:

```env
VITE_API_URL="http://backend:8000"
PLAYWRIGHT_URL="http://frontend:80"
PLAYWRIGHT_BACKEND_URL="http://backend:8000"
```


To run the tests using Docker, simply run the container named `e2e-tests`. Use the following command:

```bash
docker-compose up e2e-tests
```



## Working Flow

### 1. **Branching Strategy**

- **Branch Naming Convention:**
  - For each issue, create a branch named using the format `task_issuenumber_brief_description`. If the assignee is John, the issue number is 42, and the issue name is "create dummy page", the branch name should be `task_42_dummy_page`.

- **Branch Assignment:**
  - Assign the newly created branch to the corresponding issue in your project management tool to maintain clear traceability.

### 2. **Development Process**

- **Working on Issues:**
  - Develop the feature or fix the bug in the respective branch created for the issue.
  - Ensure that all changes are committed with meaningful messages.

- **Commit Message Format:**
  - Start each commit message with `#issuenumber` followed by a brief description of the changes. For the previous example it would be,`#42 Added initial layout for dummy page`.

- **Pushing Changes:**
  - Once the task is completed, push the development branch to the remote repository (see [How to merge to dev](#4-merging-a-branch-into-dev)).

### 3. **Healthy Branches**

There are three main branches: `dev`, `testing`, and `master`.

- **Development Branch (`dev`):**
  - This branch receives all new features from the smaller issue branches.
  - Code in this branch must pass unit tests and be free of lint errors.
  - If all checks pass, the code is automatically merged into the `testing` branch.

- **Testing Branch (`testing`):**
  - This branch contains code that has passed all unit tests.
  - QA teams perform end-to-end testing on this branch.
  - Automated end-to-end tests are executed using tools like Playwright.

- **Production Branch (`master`):**
  - This is the production-ready branch.
  - Code here has passed all types of tests, including QA and Product Owner reviews.
  - Changes in this branch are automatically deployed to production, updating the live website in real-time.

### 4. Merging a Branch into `dev`

To merge a feature branch into the `dev` branch, follow these steps:

1. **Ensure Your Local Repository is Up-to-Date:**
   - First, switch to the `dev` branch and pull the latest changes to ensure your local copy is up-to-date.
     ```bash
     git checkout dev
     git pull origin dev
     ```

2. **Merge the Feature Branch:**
   - Now, merge your feature branch into the `dev` branch. Replace `feature_branch_name` with the actual name of your branch.
     ```bash
     git merge feature_branch_name
     ```
   - If you want to ensure a merge commit is created even if the merge could be fast-forwarded, use the `--no-ff` option:
     ```bash
     git merge --no-ff feature_branch_name
     ```

3. **Resolve Any Merge Conflicts:**
   - If there are any conflicts, Git will notify you. Open the files with conflicts, resolve them, and then mark them as resolved.

4. **Run Tests and Linting:**
   - Before pushing the merged code, run all test containers to ensure the code is stable and meets quality standards.
   - Use the following commands to run the test containers:
     ```bash
     docker compose up backend-test frontend-test e2e-test
     ```

5. **Push the Changes:**
   - Once everything is verified, push the changes to the remote `dev` branch:
     ```bash
     git push origin dev
     ```


### Automatic Project Kanban

The Automatic Project Kanban system is designed to streamline the workflow and ensure that issues are automatically tracked and updated through various stages of development. Here's how it functions:

1. **Branch Push to `task_*`:**
   - When a push is made to any branch starting with `task_`, the system automatically reviews all commits since the last push to the branch.
   - It detects any commit messages containing the pattern `** #NUMBER **` and identifies these as issues.
   - These identified issues are then automatically moved to the **IN PROGRESS** state.

2. **Branch Push to `dev`:**
   - On pushing to the `dev` branch, the system runs unit tests and lint checks.
   - End-to-end (e2e) tests are also executed to prevent non-functional code from entering the testing phase.

3. **Branch Push to `testing`:**
   - Pushing to the `testing` branch triggers all tests again, including unit tests, lint checks, and e2e tests.
   - If all tests pass, the system automatically updates the status of the related issues to **READY TO TEST**.

4. **Branch Push to `master`:**
   - When changes are pushed to the `master` branch, all tests (unit, lint, and e2e) are rerun.
   - Upon successful completion of these tests, an automatic deployment is initiated.
   - If the deployment is successful, all commits since the last push to the branch are reviewed, and the corresponding issues are moved to **DONE**.

> [!CAUTION]
> The system reviews commits made between the last push to the branch and the current push. All commits associated with the task within this interval shall be moved to the new state. **Exercise caution when merging branches and avoid reversing the natural order**, lest you disrupt the harmony of issue state transitions.

