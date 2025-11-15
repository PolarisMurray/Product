from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.research import router as research_router
from routers.personal import router as personal_router
from routers.report import router as report_router

app = FastAPI(title="BioReport Copilot")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Create React App default port
        "http://localhost:8080",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research_router)
app.include_router(personal_router)
app.include_router(report_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

