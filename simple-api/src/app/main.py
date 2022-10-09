import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from .services import version_service

app = FastAPI()


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
async def redirect_to_swagger():
    return "/docs"


@app.get("/version")
async def root():
    app_version = version_service.get_application_version()
    return {"message": app_version}


@app.get("/health", include_in_schema=False, status_code=200)
def health():
    """Health Endpoint"""
    return JSONResponse(
        status_code=200,
        content={"message": "OK", "description": "Service is up and running"},
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
