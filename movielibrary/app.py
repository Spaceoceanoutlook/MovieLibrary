from fastapi import FastAPI, Depends, Request
from sqlalchemy import desc
import uvicorn
from movielibrary.routers import film
from fastapi.templating import Jinja2Templates
from movielibrary.schemas.film import FilmRead
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from movielibrary.database import get_db
from .models import Film, FilmGenre, FilmCountry
from fastapi.staticfiles import StaticFiles


app = FastAPI()

templates = Jinja2Templates(directory="movielibrary/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(film.router)

@app.get("/", response_class=HTMLResponse)
def read_films(request: Request, db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).order_by(desc(Film.id)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})

if __name__ == "__main__":
    uvicorn.run("movielibrary.app:app", host="0.0.0.0", port=8000, reload=True)
