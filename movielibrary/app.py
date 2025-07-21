from fastapi import FastAPI
from movielibrary.routers import films, filters, pages
import uvicorn

app = FastAPI(title="Movie Library API", version="0.1.0")

app.include_router(films.router, prefix="/api/films", tags=["Films"])
app.include_router(filters.router, prefix="/api/filters", tags=["Filters"])
app.include_router(pages.router, tags=["Web Pages"], include_in_schema=False)


if __name__ == "__main__":
    uvicorn.run("movielibrary.app:app", host="0.0.0.0", port=8000, reload=True)
