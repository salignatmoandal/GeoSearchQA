from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="GeoSearchQA",
    description="Assistant local avec conscience géographique",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


