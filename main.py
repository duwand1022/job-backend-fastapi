from fastapi import FastAPI, HTTPException, status, Query
from models import JobCreate, Job, SortField, SortOrder
from database import db
from typing import Optional

app = FastAPI(
    title="Job Listing API",
    description="API for managing job listings with pagination, sorting and filtering",
    version="1.0.0"
)

@app.post("/jobs/", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate):
    """
    Create a new job listing
    """
    job_data = job.dict()
    return db.create_job(job_data)

@app.get("/jobs/", response_model=dict)
def list_jobs(
    page: int = Query(1, gt=0, description="Page number"),
    per_page: int = Query(10, gt=0, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search keyword"),
    sort_by: Optional[SortField] = Query(None, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.asc, description="Sort order")
):
    return db.get_jobs(
        page=page,
        per_page=per_page,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: int):
    """
    Get a specific job by ID
    """
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, job_update: JobCreate):
    """
    Update a job listing
    """
    job = db.update_job(job_id, job_update)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int):
    """
    Delete a job listing
    """
    if not db.delete_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return None