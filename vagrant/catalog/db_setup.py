import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine

# Base = declarative_base()
from application import db, User, Category, Item

# class User(db.Model):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key = True)
#     name = Column(String(250), nullable = False)
#     email = Column(String(250), nullable = False)
#     picture = Column(String(250), nullable = False)
#     token = Column(String(500), nullable = True)

# class Category(db.Model):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key = True)
#     name = Column(String(250), nullable = False)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship(User)

# class Item(db.Model):
#     __tablename__ = 'item'
#     id = Column(Integer, primary_key = True)
#     title = Column(String(80), nullable = False)
#     author = Column(String(80), nullable = False)
#     description = Column(String(250))
#     category_id = Column(Integer, ForeignKey('category.id'))
#     category = relationship(Category)

# 	#serialize function to be able to send JSON objects in a serializable format
#     @property
#     def serialize(self):
#     #Returns object data in easily serializeable format
#         return {
#            'title' : self.name,
#            'author' : self.author,
#            'description' : self.description,
#            'category' : self.category,
#            'id' : self.id,
#        }

#db.sqlalchemy.create_engine('sqlite:///catalogapp.db')
#engine = create_engine('sqlite:///catalogapp.db')
db.create_all()

#Base.metadata.create_all(engine)