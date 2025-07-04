from fastapi import FastAPI
import uvicorn
from movielibrary.routers import film

app = FastAPI()

app.include_router(film.router)

if __name__ == "__main__":
    uvicorn.run("movielibrary.app:app", host="0.0.0.0", port=8000, reload=True)
