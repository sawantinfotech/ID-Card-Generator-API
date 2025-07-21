from fastapi import FastAPI
from backend import auth, generate_id
from backend.database import Base, engine, DB_TYPE
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(generate_id.router)

@app.get("/")
def root():
    return {"message": "ID Card Generator API is running."}

@app.get("/db-status")
def db_status():
    return {"database_in_use": DB_TYPE}
