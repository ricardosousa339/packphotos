from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


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


@table_registry.mapped_as_dataclass
class Album:
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

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

    album_id: Mapped[int] = mapped_column(ForeignKey('albums.id'))
    album: Mapped[Album] = relationship(init=False, back_populates='photos')

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
