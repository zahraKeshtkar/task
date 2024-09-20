from entities.user import UserEntity

class UserRepository:
    def __init__(self, session):
        self._session = session

    def create_user(self, entity: UserEntity):
        self._session.add(entity)

    def get_user_by_phone(self, phone):
        return self._session.query(UserEntity).filter(
            UserEntity.phone == phone,
            UserEntity.deleted_at.is_(None),
        ).first()

