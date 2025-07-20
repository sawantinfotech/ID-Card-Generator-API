
import os

# Ensure the working directory is correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run FastAPI from the backend folder using Uvicorn
os.system("uvicorn backend.main:app --host=0.0.0.0 --port=8000 --reload")
