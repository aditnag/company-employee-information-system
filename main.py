from fastapi import FastAPI
from db import metadata, engine, database
import company, employee, user, auth

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(company.router)
app.include_router(employee.router)
app.include_router(user.router)
app.include_router(auth.router)
