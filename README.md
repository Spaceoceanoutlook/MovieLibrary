## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/Spaceoceanoutlook/MovieLibrary.git
```
Открыть проект в редакторе, в корне проекта создать файл `.env` и добавить следующие переменные:
```

```
В системе должен быть установлен poetry
Для корректной работы приложения, версия python должны быть < 3.14
Если глобальная версия python >= 3.14, то установить 3.13.0 через pyenv, после чего выполнить
```bash 
poetry env use ~/.pyenv/versions/3.13.0/bin/python
```
Активируем и добавляем полученный путь в Select Interpreter
```bash
poetry env activate
```
Установка библиотек:
```bash 
poetry install
```
Запуск базы данных 
```bash 
docker compose -f docker-compose.dev.yml up -d
```
Запуск приложения
```bash 
python movielibrary/main.py
```
