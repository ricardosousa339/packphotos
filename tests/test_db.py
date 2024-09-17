from sqlalchemy import select

from fast_zero.models import User


def test_select_user(session):
    # Assuming there is already a user with username 'bob' in the database
    user = session.scalar(select(User).where(User.username == 'teste0'))

    assert user is not None
    assert user.username == 'teste0'
    assert user.email == 'teste0@test.com'
