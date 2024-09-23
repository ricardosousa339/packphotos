from datetime import datetime

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()

purchase_photos = Table(
    'purchase_photos',
    table_registry.metadata,
    Column('purchase_id', ForeignKey('purchases.id'), primary_key=True),
    Column('photo_id', ForeignKey('photos.id'), primary_key=True)
)


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    albums: Mapped[list['Album']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )
    purchases: Mapped[list['Purchase']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Album:
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    price_per_photo: Mapped[float] = mapped_column(default=0.0)
    user: Mapped[User] = relationship(init=False, back_populates='albums')

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    photos: Mapped[list['Photo']] = relationship(
        init=False, back_populates='album', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Photo:
    __tablename__ = 'photos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    url: Mapped[str]
    price: Mapped[float]
    album_id: Mapped[int] = mapped_column(ForeignKey('albums.id'))
    album: Mapped[Album] = relationship(init=False, back_populates='photos')
    
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    purchases: Mapped[list['Purchase']] = relationship(
        secondary=purchase_photos, back_populates='photos', default_factory=list
    )
    

@table_registry.mapped_as_dataclass
class Purchase:
    __tablename__ = 'purchases'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    amount: Mapped[float]

    photos: Mapped[list['Photo']] = relationship(
        secondary=purchase_photos, back_populates='purchases'
    )
    status: Mapped[str] = mapped_column(default='pending')
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    user: Mapped['User'] = relationship(init=False, back_populates='purchases')
