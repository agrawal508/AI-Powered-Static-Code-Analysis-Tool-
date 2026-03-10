# AI-Powered Static Code Analysis Tool

This project is an AI-powered static code analysis tool that analyzes source code to detect security vulnerabilities such as SQL Injection, unsafe function usage, and hardcoded secrets.

## Project Structure

```text
ai-code-analyzer
│
├── backend/          # Python FastAPI application
│   ├── main.py       # FastAPI server entry point
│   ├── analyzer.py   # Code analysis logic
│   ├── rules/        # Rules for vulnerability detection
│   ├── models/       # Data models
│   └── utils/        # Utility functions
│
├── frontend/         # React application (future use)
│
├── docker/           # Docker configurations
│
└── README.md         # Project documentation
```

## Setup and Running the Backend

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **(Optional but recommended) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Test the server:**
   Open your browser and navigate to `http://127.0.0.1:8000/`. You should see the message `"AI Code Analyzer API running"`. 

   You can also view the automatically generated interactive API documentation at `http://127.0.0.1:8000/docs`.
