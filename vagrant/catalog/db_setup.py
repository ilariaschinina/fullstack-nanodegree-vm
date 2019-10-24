import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    token = Column(String(500), nullable=True)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    title = Column(String(80), nullable = False)
    author = Column(String(80), nullable = False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

	#serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
    #Returns object data in easily serializeable format
        return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
       }

engine = create_engine('sqlite:///catalogapp.db')

Base.metadata.create_all(engine)