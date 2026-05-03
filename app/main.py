from fastapi import FastAPI
from app.database.database import SessionLocal, engine, Base
from app.routes.cidade_routes import router as cidade_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cidade_router)




