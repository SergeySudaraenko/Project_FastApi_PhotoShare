from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from routes import auth, photos, search
from routes import comments
from routes.comments import get_current_user
from src.database.db import get_db
from src.routes import rating, profile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api")

@app.get("/status")
def read_root():
    """Перевірка статусу API."""
    return {"status": "API працює"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(photos.router, prefix="/photos", tags=["photos"], dependencies=[Depends(get_current_user)])
app.include_router(comments.router, prefix="/comments", tags=["comments"], dependencies=[Depends(get_current_user)])
app.include_router(profile.router, prefix="/profile", tags=["profile"], dependencies=[Depends(get_current_user)])
app.include_router(rating.router, prefix="/rating", tags=["rating"], dependencies=[Depends(get_current_user)])
app.include_router(search.router, prefix="/search", tags=["search"], dependencies=[Depends(get_current_user)])

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")