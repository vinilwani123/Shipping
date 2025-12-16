from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import users, countries

app = FastAPI(title="BigBag Shipping API")

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(countries.router)

@app.get("/")
def health_check():
    return {"status": "BigBag API running"}
