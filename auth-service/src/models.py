from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

from src.database import Base

# Association table for user roles
user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id')),
                   Column('role_id', Integer, ForeignKey('roles.id'))
                   )

# Association table for role permissions
role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', Integer, ForeignKey('roles.id')),
                         Column('permission_id', Integer, ForeignKey('permissions.id'))
                         )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to roles
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to roles
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission(name='{self.name}')>"


class RegistrationAttempt(Base):
    __tablename__ = "registration_attempts"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    last_registration_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    registration_count = Column(Integer, default=0)

    def __init__(self, *args, **kwargs):
        # Ensure last_registration_time is timezone-aware in UTC
        if 'last_registration_time' in kwargs:
            if kwargs['last_registration_time'].tzinfo is None:
                kwargs['last_registration_time'] = kwargs['last_registration_time'].replace(tzinfo=pytz.UTC)
            elif kwargs['last_registration_time'].tzinfo != pytz.UTC:
                kwargs['last_registration_time'] = kwargs['last_registration_time'].astimezone(pytz.UTC)
        super().__init__(*args, **kwargs)
