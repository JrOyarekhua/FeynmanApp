from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User


class UserRepository:
    """
    Repository responsible for all database operations related to the User model.

    This class abstracts the persistence layer and provides CRUD operations
    for User entities. It should not contain business logic or validation;
    those responsibilities belong in the service layer.

    Attributes:
        db (Session): Active SQLAlchemy database session used to execute
            database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with a SQLAlchemy database session.

        Args:
            db (Session): SQLAlchemy session used for database transactions.
        """
        self.db = db

    def create_user(self, user: User) -> UUID:
        """
        Persist a new user to the database.

        The user is added to the current session, flushted to the database,
        refreshed to obtain any database-generated values, and the user's
        unique identifier is returned.

        Args:
            user (User): The User model instance to be created.

        Returns:
            UUID: The UUID of the newly created user.
        """
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user.user_id

    def get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by its unique identifier.

        Args:
            user_id (UUID): The UUID of the user to retrieve.

        Returns:
            User | None:
                The matching User object if found; otherwise None.
        """
        return self.db.get(User, user_id)
    
    def get_user_by_auth_id(self, sub) -> User | None:
        """
        Retrive a user by it's unique jwt identifier 

        Args: 
            sub: jwt sub field 
        Returns:
            User | None:
                matching user object if found otherwise none
        
        """
        return self.db.scalars(
            select(User).where(User.auth_id == sub)
        ).one_or_none()


    def update_user(self, user_id: UUID, data: dict[str, Any]) -> User:
        """
        Update an existing user's attributes.

        Each key-value pair in the provided dictionary is applied to the
        corresponding attribute of the User object. After updating, the
        changes are flushted and the updated entity is refreshed.

        Note:
            This method assumes the provided fields are valid and that the
            user exists. Validation and existence checks should be handled
            by the service layer.

        Args:
            user_id (UUID): The UUID of the user to update.
            data (dict[str, Any]): Dictionary containing the fields and
                values to update.

        Returns:
            User: The updated User object.
        """
        user: User = self.get_user_by_id(user_id)

        for key, value in data.items():
            setattr(user, key, value)

        self.db.flush()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: UUID) -> UUID:
        """
        Delete a user from the database.

        The user is removed from the database and the transaction is
        flushted. The UUID of the deleted user is returned.

        Note:
            This method assumes the user exists. Existence checks should
            be performed by the service layer.

        Args:
            user_id (UUID): The UUID of the user to delete.

        Returns:
            UUID: The UUID of the deleted user.
        """
        user: User = self.get_user_by_id(user_id)

        self.db.delete(user)
        self.db.flush()

        return user.user_id