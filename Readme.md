# 8.1D Fullstack ML Project

This project integrates a machine learning backend with a SvelteKit frontend dashboard.

## Project Structure
- `/backend`: Python server handling API requests and model inference.
- `/frontend`: SvelteKit (Node.js) web application.
- `/models`: Serialized machine learning models (`.pkl`).
- `/virtuals`: Python virtual environment (ignored in git).

## Prerequisites
* Python 3.9+
* Node.js v18+ & npm

## Setup Instructions

### 1. Backend Setup
Navigate to the root directory and set up your Python environment:

```bash
# Create and activate the virtual environment
python -m venv virtuals
source virtuals/bin/activate  

# Install dependencies
pip install -r requirements.txt

# Run the backend server 
cd backend
python main.py
```

### 2. Frontend Setup (SvelteKit)
The frontend is a SvelteKit application built with Vite and TypeScript.

Open a new terminal window and navigate to the frontend directory:

```bash
cd frontend

# Install Node dependencies 
npm install

# Start the Vite development server
npm run dev
```