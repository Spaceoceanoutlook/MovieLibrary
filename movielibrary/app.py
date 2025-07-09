from fastapi import FastAPI
from movielibrary.routers import film, filters, homepage
import uvicorn

app = FastAPI(title="Movie Library API", version="0.1.0")

app.include_router(film.film_router, prefix="/api", tags=["films"])
app.include_router(filters.filters_router, tags=["filters"])
app.include_router(homepage.homepage_router, tags=["homepage"])


if __name__ == "__main__":
    uvicorn.run("movielibrary.app:app", host="0.0.0.0", port=8000, reload=True)
