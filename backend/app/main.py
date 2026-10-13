
from fastapi import FastAPI

from app.api.routes.activities import router as activities_router


app = FastAPI(
    title="StudyFlow API",
    version="0.1.0",
)

app.include_router(activities_router)


@app.get("/")
def read_root():
    return {"message": "StudyFlow API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
