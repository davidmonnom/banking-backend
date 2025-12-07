import os

from fastapi import FastAPI, Depends
from fastapi_sso.sso.base import OpenID
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routers import user, auth, data, item, transaction, account, category, goal, budget
from .security import get_logged_user

load_dotenv('app/.env')

SECRET_KEY = os.environ.get("JWT_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

app = FastAPI(
    title="Cedav Accounting",
    version="1.0.0",
    description="Endpoint for the Cedav Accounting API",
)

origins = [
    "http://localhost:3000",
    "https://www.cedav.be",
    "https://cedav.be",
    "http://192.168.0.141",
    "http://10.0.3.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(data.router)
app.include_router(item.router)
app.include_router(transaction.router)
app.include_router(account.router)
app.include_router(category.router)
app.include_router(goal.router)
app.include_router(budget.router)
Base.metadata.create_all(bind=engine)


@app.get("/")
async def protected_endpoint(user: OpenID = Depends(get_logged_user)):
    """This endpoint will say hello to the logged user.
    If the user is not logged, it will return a 401 error from `get_logged_user`."""
    return {
        "message": f"You are very welcome, {user.email}!",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
