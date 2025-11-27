from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks, analytics
from app.database import init_db

app = FastAPI(title="Task Manager API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Task Manager API - Demo for Carbonara"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
