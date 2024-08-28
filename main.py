from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.routes import auth
from src.routes import users

origins = [
    "http://localhost:3000"
    ]

app = FastAPI()


app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.get('/')
def index():
    return {'message': 'Contact Application'}



@app.get('/api/healthcheker')
async def healthcheker(db: AsyncSession = Depends(get_db)):
    try:
        #Make request
        result = await db.execute(text('SELECT 1'))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database isn\'t confifured correctly')
        return {'message': 'Welcome to FastApi!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error connecting to the database')