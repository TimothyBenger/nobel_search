from fastapi import FastAPI
from app.services.ingest_data import ingest_data
from app.routes.search import router as search_router

app = FastAPI()

# Event that triggers data ingestion at startup
@app.on_event("startup")
async def startup_event():
    await ingest_data()

# Include the routes for search functionality
app.include_router(search_router)