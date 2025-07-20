from fastapi import FastAPI
from backend import auth, generate_id
from backend.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(generate_id.router)

@app.get("/")
def root():
    return {"message": "ID Card Generator API is running."}
