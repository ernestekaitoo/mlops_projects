# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# 1. Install dependencies first (to use Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the source code
# This includes src/train.py, src/logger.py, etc.
COPY ./src ./src

# 3. Copy the ARTIFACTS created by your script
# Your script saves these to the 'models' folder on your Mac
COPY ./models/model.joblib ./models/model.joblib
COPY ./models/transformers/preprocessor.joblib ./models/transformers/preprocessor.joblib
COPY ./models/transformers/label_encoder.joblib ./models/transformers/label_encoder.joblib

# 4. Copy the API and supporting files
COPY ./src/main.py .
COPY data_models.py .
COPY params.yaml .
COPY static/ ./static/

# 5. Expose port and start the app
EXPOSE 8000

# We use app:app because your entry point file is named app.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]