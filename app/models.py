from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class ModelBase(object):
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=ModelBase)

class User(Base):
    __tablename__ = 'users'

    birthday = Column(DateTime)
    is_admin = Column(Boolean, default=False)

class Server(Base):
    __tablename__ = 'servers'

class ServerAdmin(Base):
    __tablename__ = 'server_admins'

    user_id = Column(Integer, ForeignKey('users.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))

class Role(Base):
    __tablename__ = 'roles'

class SelfRole(Base):
    __tablename__ = 'self_roles'

    role_id = Column(Integer, ForeignKey('roles.id'))
    alias = Column(String)

class RolesGroup(Base):
    __tablename__ = 'roles_groups'
