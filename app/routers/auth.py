import os

from fastapi import Depends, HTTPException, Request, APIRouter
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

from sqlalchemy.orm import Session

from .. import schemas, utils
from ..security import get_new_jwt, get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

SECRET_KEY = os.environ.get("JWT_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
sso = GoogleSSO(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_SECRET,
    redirect_uri=GOOGLE_REDIRECT_URI)


@router.get("/login")
async def login(source: str = None):
    """Redirect the user to the Google login page."""

    with sso:
        return await sso.get_login_url(params={
            "source": source
        })


@router.get("/logout")
async def logout():
    """Forget the user's session."""
    response = RedirectResponse(url="/")
    response.delete_cookie(key="token")
    return response


@router.post("/exchange_code")
async def auth_code_callback(auth_code: str, request: Request, db: Session = Depends(get_db)):
    """Create a new user."""
    with sso:
        openid = await sso.process_login(auth_code, request)
        if not openid:
            raise HTTPException(
                status_code=401, detail="Authentication failed")


@router.get("/callback")
async def login_callback(request: Request, db: Session = Depends(get_db)):
    """Process login and redirect the user to the protected endpoint."""
    with sso:
        openid = await sso.verify_and_process(request)
        if not openid:
            raise HTTPException(
                status_code=401, detail="Authentication failed")

    # Create the user if it doesn't exist
    user = utils.user.get_by_external_id(db, external_id=openid.id)
    user_data = dict(openid)

    if not user:
        user_data = dict(openid)

        group = utils.group.create(db, schemas.GroupCreate(**{
            "name": f"{user_data['first_name']}'s group",
            "description": f"Group for {user_data['first_name']}",
        }))

        user = utils.user.create(db, user=schemas.UserCreate(**{
            "externalId": user_data["id"],
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "display_name": user_data["display_name"],
            "picture": user_data["picture"],
            "provider": user_data["provider"],
            "language": "en",
            "darkMode": False,
        }))

        user.groups.append(group)
        group.userOwnerId = user.id
        db.commit()

    # Create a JWT token and store it in a cookie
    jwt = get_new_jwt(openid)
    referer = request.headers.get("referer")
    response = RedirectResponse(
        url=f"{referer}?token={jwt['token']}&expiration={jwt['expiration']}")

    # just return a cookie
    return response
