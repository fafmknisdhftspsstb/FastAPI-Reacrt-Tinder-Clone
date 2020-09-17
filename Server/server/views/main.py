from server import app, oauth2_scheme 
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from server.security.authentication import verify_password
from sqlalchemy.orm import Session
from server.database import schemas
from server.database.database import SessionLocal, engine
from server.security.user_management import get_user_from_db, create_user_in_db
from server.security.token import create_access_token, validate_token, Token
from server.Exceptions import EXCEPTIONS

# TODO: Create a global exception definition file
# TODO: Create a global db that is initialized on startup and destroyed on shutdown
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_from_db(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = validate_token(token)

    user = get_user_from_db(username, db)
    if user is None:
        raise EXCEPTIONS['invalid_credentials']
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise EXCEPTIONS['inactive_user']
    return current_user

@app.post("/register", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user_in_db(user, db)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise EXCEPTIONS['invalid_username_or_password']

    # TODO: Move to token.py
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]