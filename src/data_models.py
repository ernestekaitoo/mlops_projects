from pydantic import BaseModel, Field

class PredictionDataset(BaseModel):
    """
    This is the 'Input Schema'. 
    It defines exactly what names and numbers the user must provide.
    We use 'alias' to match the exact names in your CSV.
    """
    marital_status: int = Field(alias="Marital status")
    application_mode: int = Field(alias="Application mode")
    application_order: int = Field(alias="Application order")
    course: int = Field(alias="Course")
    attendance: int = Field(alias="Daytime/evening attendance\t")
    previous_qualification: int = Field(alias="Previous qualification")
    gdp: float = Field(alias="GDP")
    unemployment_rate: float = Field(alias="Unemployment rate")
    inflation_rate: float = Field(alias="Inflation rate")
    # Add any other columns your model needs here!

    class Config:
        # This allows the API to accept the "Pretty Names" with spaces
        populate_by_name = True

class PredictionResponse(BaseModel):
    """
    This is the 'Output Schema'.
    It defines how the result will look when it's sent back to the user.
    """
    predicted_academic_success_score: str