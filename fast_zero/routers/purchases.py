from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from fast_zero.database import get_session
from fast_zero.models import Purchase, Photo, User
from fast_zero.routers.albums import CurrentUser
from fast_zero.schemas import PhotoPublic, PurchaseCreate, PurchasePublic
from fast_zero.security import get_current_user


Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/purchases', tags=['purchases'])


@router.get('/photos', response_model=List[PhotoPublic])
def list_photos(session: Session):
    photos = session.query(Photo).all()
    return photos

@router.post('/purchases', response_model=PurchasePublic)
def create_purchase(
    purchase: PurchaseCreate,
    session: Session,
    current_user: CurrentUser,
):
    db_photos = session.query(Photo).filter(Photo.id.in_(purchase.photo_ids)).all()
    if not db_photos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='One or more photos not found',
        )

    total_amount = sum(photo.price for photo in db_photos)  # Assumindo que cada foto tem um preço

    db_purchase = Purchase(
        user_id=current_user.id,
        amount=total_amount,
        photos=db_photos,
    )
    db_purchase.photos.extend(db_photos)
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)

    return db_purchase


@router.get('/purchases', response_model=List[PurchasePublic])
def list_purchases(session: Session, current_user: CurrentUser):
    purchases = session.query(Purchase).filter(Purchase.user_id == current_user.id).all()
    return purchases