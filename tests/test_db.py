from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='alice', password='secret', email='teste@test.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
    assert user.password == 'secret'
    assert user.email == 'teste@test.com'
