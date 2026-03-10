from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import analyzer
import datetime

app = FastAPI(title="AI Code Analyzer API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"message": "AI Code Analyzer API running"}

@app.post("/analyze")
def analyze_code_endpoint(request: AnalyzeRequest):
    """
    Analyzes Python code provided as a string in the JSON payload.
    """
    if not request.code:
        raise HTTPException(status_code=400, detail="Code string is empty")
        
    issues = analyzer.analyze_code(request.code)
    
    return generate_report([("inline_code.py", issues)])

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts a Python file upload, reads its contents, and analyzes it.
    """
    if not file.filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Only Python (.py) files are supported")
        
    contents = await file.read()
    
    try:
        code_str = contents.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File could not be decoded. Ensure it is UTF-8 encoded text.")
        
    issues = analyzer.analyze_code(code_str)
    
    # Generate the structured report
    return generate_report([(file.filename, issues)])


def generate_report(results: list) -> dict:
    """
    Formats the analysis results into a structured security report.
    results is a list of tuples: [(filename, issues_list)]
    """
    all_issues = []
    total_files = len(results)
    
    for filename, issues in results:
        for issue in issues:
            # Add the filename to each issue for the report
            issue_with_file = issue.copy()
            issue_with_file["file"] = filename
            all_issues.append(issue_with_file)
            
    return {
        "report_generated_at": datetime.datetime.utcnow().isoformat(),
        "files_scanned": total_files,
        "issues_found": len(all_issues),
        "issues": all_issues
    }
