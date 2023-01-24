from fastapi import FastAPI

from project.api.urls import router
from settings import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root():
    return {"Project": "CLabs Take home project, check /docs for api documentation"}


app.include_router(router)
