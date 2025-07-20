
import os

# Change directory to backend and run FastAPI server
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
os.system("uvicorn main:app --host=0.0.0.0 --port=8000 --reload")
