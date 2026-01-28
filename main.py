from db.session import get_session
from models.base import Base
from db.engine import create_db_engine
from services.user import UserService, CreateUserDTO, UserAlreadyExists


def init_db() -> None:
    """
    Create database tables if they do not exist yet.
    In a real app you would likely use migrations instead.
    """
    engine = create_db_engine()
    Base.metadata.create_all(bind=engine)


def demo_create_user() -> None:
    """
    Very simple demonstration of the 'create user' feature
    using the service layer.
    """
    init_db()

    service = UserService()

    # In a real application, these would come from an API/CLI input
    data = CreateUserDTO(
        email="alice@example.com",
        name="Alice",
        age=25,
    )

    with get_session() as db:
        try:
            user = service.create_user(db, data)
            db.commit()
            print(f"Created user: id={user.id}, email={user.email}, name={user.name}")
        except UserAlreadyExists as exc:
            db.rollback()
            print(str(exc))
        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    demo_create_user()

