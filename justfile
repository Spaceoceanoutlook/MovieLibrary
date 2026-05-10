up:
    docker compose up --build -d

down:
    docker compose down

db:
    docker exec -it films_db psql -U postgres -d films_db

app:
    docker exec -it movielibrary_web /bin/bash