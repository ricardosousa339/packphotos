from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Album, User
from fast_zero.schemas import AlbumPublic, AlbumSchema
from fast_zero.security import get_current_user

# db = firestore.Client()


Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/albums', tags=['albums'])


@router.post('/', response_model=AlbumPublic)
def create_album(
    album: AlbumSchema,
    user: CurrentUser,
    session: Session,
):
    db_album = Album(
        title=album.title,
        user_id=user.id,
    )

    print(db_album)
    print('-----\n\n\n\n\n\n\n\n\n\n\\n-------testeteste')
    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    return db_album
