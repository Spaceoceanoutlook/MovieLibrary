import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from movielibrary.routers import films, filters, pages


app = FastAPI(title="Movie Library API", version="0.1.0")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="movielibrary/static"), name="static")
app.include_router(films.router, prefix="/api/films", tags=["Films"])
app.include_router(filters.router, prefix="/api/filters", tags=["Filters"])
app.include_router(pages.router, tags=["Web Pages"], include_in_schema=False)


if __name__ == "__main__":
    uvicorn.run("movielibrary.main:app", host="0.0.0.0", port=8000, reload=True)
