from typing import Dict, List, Optional
from models import Job, SortField, SortOrder

class Database:
    def __init__(self):
        self.jobs: Dict[int, Job] = {}
        self.current_id = 0

    def get_jobs(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        sort_by: Optional[SortField] = None,
        sort_order: SortOrder = SortOrder.asc
    ) -> dict:
        jobs = list(self.jobs.values())
        
        # Apply search filter
        if search:
            search = search.lower()
            jobs = [
                job for job in jobs
                if (search in job.title.lower() or 
                    search in job.description.lower() or
                    search in job.region.lower())
            ]
        
        # Apply sorting
        if sort_by:
            reverse = sort_order == SortOrder.desc
            jobs.sort(key=lambda job: getattr(job, sort_by.value), reverse=reverse)
        
        # Calculate pagination
        total_jobs = len(jobs)
        total_pages = (total_jobs + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_jobs = jobs[start:end]
        
        return {
            "jobs": paginated_jobs,
            "total": total_jobs,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }

    def get_job(self, job_id: int):
        return self.jobs.get(job_id)

    def create_job(self, job_data: dict):
        self.current_id += 1
        job = Job(id=self.current_id, **job_data)
        self.jobs[job.id] = job
        return job

    def update_job(self, job_id: int, job_update):
        if job_id not in self.jobs:
            return None
        job = self.jobs[job_id]
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        return job

    def delete_job(self, job_id: int):
        if job_id not in self.jobs:
            return False
        del self.jobs[job_id]
        return True

# Initialize the database
db = Database()