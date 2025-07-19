from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for functions
deployed_functions = []

# ----------------------------
# File upload deploy endpoint
# ----------------------------
@app.post("/deploy")
async def deploy_function(
    function_name: str = Form(...),
    language: str = Form(...),
    timeout: int = Form(...),
    file: UploadFile = File(...)
):
    temp_dir = "uploaded_functions"
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    deployed_functions.append({
        "id": len(deployed_functions) + 1,
        "name": function_name,
        "language": language,
        "timeout": timeout,
        "file": file.filename,
        "code": None,
        "virtualization_type": "docker"
    })

    return {"message": f"Function '{function_name}' deployed successfully."}

# ----------------------------
# Deploy via Text (JSON input)
# ----------------------------
class FunctionPayload(BaseModel):
    name: str
    code: str
    language: str
    timeout: int
    virtualization_type: str

@app.post("/functions/")
async def deploy_from_text(payload: FunctionPayload):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
    
    deployed_functions.append({
        "id": len(deployed_functions) + 1,
        "name": payload.name,
        "language": payload.language,
        "timeout": payload.timeout,
        "code": payload.code,
        "virtualization_type": payload.virtualization_type,
        "file": None
    })

    return {"message": f"Function '{payload.name}' deployed successfully via text."}

# ----------------------------
# List deployed functions
# ----------------------------
@app.get("/functions/")
async def list_functions():
    return deployed_functions

# ----------------------------
# Simulate run function with runtime
# ----------------------------
class RuntimeRequest(BaseModel):
    runtime: str

@app.post("/run/{func_id}")
async def run_function(func_id: int, req: RuntimeRequest):
    for func in deployed_functions:
        if func["id"] == func_id:
            runtime_used = req.runtime
            return {
                "output": f"Function '{func['name']}' ran successfully on **{runtime_used}** (simulated)."
            }
    raise HTTPException(status_code=404, detail="Function not found.")

# ----------------------------
# Monitoring Summary
# ----------------------------


@app.get("/monitor/summary")
async def monitor_summary():
    summary = {
        "total_functions": len(deployed_functions),
        "languages": list(set(func["language"] for func in deployed_functions)),
        "execution_times": [round(1 + i * 0.5, 2) for i in range(len(deployed_functions))],  # fake exec times
    }
    return summary

