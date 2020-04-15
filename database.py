from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine("postgresql://postgres:docker@localhost/api_example")
Base = declarative_base()

class User(Base):
    __tablename__ = 'TB_USERS'
    u_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(4000))
    favorite_movie = Column(String(4000))
    last_update = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, fav_movie):
        self.username = username
        self.password = password
        self.favorite_movie = fav_movie
        

def create_user(name, password, fav_movie):
    user = User(name, password, fav_movie)
    session.add(user)
    session.commit()
    return user.u_id
    
def get_user_by_id(id):
    result = session.query(User).filter(User.u_id == id).first()
    return result
    

def get_user_by_name(name):
    result = session.query(User).filter(User.username == name).first()
    return result
    
def get_users():
	results = session.query(User).all()
	return [result for result in results]
    

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)