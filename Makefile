# 1. Create a virtual environment and install tools
install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

# Add this to your Makefile
# Note: Your dvc.lock shows you use a ZIP file, so we ensure the directory exists
get_data:
	mkdir -p data/raw/Zipped
	curl -o data/raw/Zipped/playground-series-s4e6.zip https://media.geeksforgeeks.org/wp-content/uploads/20240731192821/data.csv

# 2. Run the training
# Since you have a DVC pipeline, 'dvc repro' is the correct way to run your training scripts
train:
	dvc repro

trainn:
	python3 src/train.py

# 3. Start the FastAPI server
# Based on your Docker needs, ensure main.py is in the 'src' folder
run:
	uvicorn src.main:app --reload

# 4. Clean up temporary files
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf .pytest_cache

# 5. Do everything at once
all: install train run

# --- Separated Docker Section ---
IMAGE_NAME = academic-success-predictor

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -p 8000:8000 $(IMAGE_NAME)