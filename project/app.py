from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from project.api.v1 import router
from settings import settings
from project.exceptions import SessionIdIntegrityError, UserEmailIntegrityError

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root():
    return {"Project": "CLabs Take home project, check /docs for api documentation"}


@app.exception_handler(SessionIdIntegrityError)
def handling_duplicate_session_id(request: Request, exc: SessionIdIntegrityError):
    return JSONResponse(
        status_code=422,
        content={"detail": [
            {
                "loc": ["body", "audio", "session_id"],
                "msg": str(exc)
            }
        ]}
    )


@app.exception_handler(UserEmailIntegrityError)
def handling_duplicate_session_id(request: Request, exc: UserEmailIntegrityError):
    return JSONResponse(
        status_code=422,
        content={"detail": [
            {
                "loc": ["body", "user", "email"],
                "msg": str(exc)
            }
        ]}
    )


app.include_router(router)

