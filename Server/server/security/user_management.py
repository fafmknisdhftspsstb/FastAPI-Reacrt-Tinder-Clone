from server.database import crud
from server.database import schemas
from server.Exceptions import EXCEPTIONS
from sqlalchemy.orm import Session


def create_user_in_db(user: schemas.UserCreate, db: Session):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise EXCEPTIONS['user_exists']
    return crud.create_user(db=db, user=user)

def get_user_from_db(username: str, db: Session):
	return crud.get_user_by_username(db, username=username)