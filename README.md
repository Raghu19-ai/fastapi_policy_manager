# Employee Policy Management API

## Overview
Backend API using FastAPI + MongoDB to manage:
- Employees
- Policies
- Assignment of policies to employees

## Tech Stack
- FastAPI
- MongoDB (via `motor`)
- Pydantic
- Uvicorn
- python-dotenv

## Setup

```bash
git clone <your-repo-url>
cd fastapi_policy_manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install deps
pip install -r requirements.txt
