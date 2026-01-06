from pydantic import BaseModel

class PredictionDataset(BaseModel):
    # These names must match the column names in your CSV exactly
    Course: int
    Previous_qualification_grade: float
    GDP: float
    # Add other columns here that your model uses, for example:
    # Age_at_enrollment: int
    # Scholarship_holder: int
    
    class Config:
        # This allows the API to accept both "Course" and "course" 
        # (helpful if your HTML form uses lowercase)
        populate_by_name = True