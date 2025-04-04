from typing import Optional
from pydantic import BaseModel
from enum import Enum

class JobBase(BaseModel):
    title: str
    description: str
    region: str
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True

class SortField(str, Enum):
    title = "title"
    region = "region"
    min_salary = "min_salary"
    max_salary = "max_salary"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"