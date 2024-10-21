import uvicorn
from fastapi import FastAPI
from routes.paper_routes import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    """
    Entry point of the application.

    Runs the FastAPI application using Uvicorn server on host 0.0.0.0 and port 8000.
    The `reload=True` option enables auto-reloading of the server when code changes.
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
