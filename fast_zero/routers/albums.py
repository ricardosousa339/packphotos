import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from fast_zero.database import get_session
from fast_zero.models import Album, Photo, User
from fast_zero.schemas import (
    AlbumList,
    AlbumPublic,
    AlbumSchema,
    PhotoList,
    PhotoPublic,
    PhotoSchema,
)
from fast_zero.security import get_current_user

# db = firestore.Client()
logger = logging.getLogger(__name__)


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

    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    return db_album


@router.get('/', response_model=AlbumList)
def read_albums(session: Session,
                current_user: CurrentUser,
                skip: int = 0,
                limit: int = 100):

    print(f"Current user: {current_user}")
    albums = session.scalars(select(Album)
                             .where(Album.user_id == current_user.id)
                             .offset(skip).limit(limit)).all()
    return {'albums': albums}


@router.put('/{album_id}', response_model=AlbumPublic)
def update_album(
    album_id: int,
    album: AlbumSchema,
    current_user: CurrentUser,
    session: Session,
):
    db_album = session.scalar(select(Album).where(Album.id == album_id))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    if db_album.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    db_album.title = album.title
    session.commit()
    session.refresh(db_album)

    return db_album


@router.post('/{album_id}/photos', response_model=PhotoPublic)
def add_photo_to_album(
    album_id: int,
    photo: PhotoSchema,
    session: Session,
    current_user: CurrentUser,
):
    # logger.info(f"Received request to add photo to album
    # {album_id} with data: {photo}")

    db_album = session.scalar(select(Album).where(Album.id == album_id))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    if db_album.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    db_photo = Photo(url=photo.url, name=photo.name, album_id=album_id)
    session.add(db_photo)
    session.commit()
    session.refresh(db_photo)

    return db_photo


@router.delete('/{album_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_album(
    album_id: int,
    current_user: CurrentUser,
    session: Session,
):
    db_album = session.scalar(select(Album).where(Album.id == album_id))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    if db_album.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    session.delete(db_album)
    session.commit()


@router.get('/{album_id}', response_model=AlbumPublic)
def read_album(album_id: int, 
               session: Session,
               user: CurrentUser):
    db_album = session.scalar(select(Album).where(
        and_(
            Album.id == album_id, 
            Album.user_id == user.id
            )))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    return db_album


@router.get('/{album_id}/photos', response_model=PhotoList)
def read_photos_from_album(album_id: int, 
                           session: Session,
                           user: CurrentUser):
    db_album = session.scalar(select(Album).where(
        and_(
            Album.id == album_id,
            Album.user_id == user.id
        )
    ))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    return {'photos': db_album.photos}


@router.delete(
    '/{album_id}/photos/{photo_id}', status_code=HTTPStatus.NO_CONTENT
)
def delete_photo_from_album(
    album_id: int,
    photo_id: int,
    current_user: CurrentUser,
    session: Session,
):
    db_album = session.scalar(select(Album).where(
        and_(
            Album.id == album_id,
            Album.user_id == current_user.id
        )
    ))

    if not db_album:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Album not found',
        )

    if db_album.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    db_photo = session.scalar(select(Photo).where(Photo.id == photo_id))

    if not db_photo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Photo not found',
        )

    session.delete(db_photo)
    session.commit()
