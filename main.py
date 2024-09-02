import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.routes import auth, comments, photos, profile, rating, search, users, tags
from src.database.db import get_db


origins = ["*"]

app = FastAPI()

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Включення маршрутів
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(tags.router, prefix="/api") #Важливий роутер
app.include_router(search.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(rating.router, prefix="/api")


@app.get("/")
def index():
    return {"message": "Контактний додаток"}


@app.get("/api/healthcheker")
async def healthcheker(db: AsyncSession = Depends(get_db)):
    try:
        # Перевірка з'єднання з базою даних
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="База даних не налаштована правильно"
            )
        return {"message": "Ласкаво просимо до FastAPI!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Помилка підключення до бази даних")


@app.on_event("shutdown")
async def shutdown():
    # Очищення ресурсів
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
