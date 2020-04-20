from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine("postgresql://postgres:docker@localhost/api_example")
Base = declarative_base()

class User(Base):
    __tablename__ = 'TB_USERS2'
    u_id = Column(Integer, Sequence('user2_id_seq'), primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(4000))
    last_update = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, fav_movie):
        self.username = username
        self.password = password
        self.favorite_movie = fav_movie
        

class Movie(Base):
    __tablename__ = 'TB_MOVIES'
    m_id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    name = Column(String(100), unique=True)
    author = Column(String(4000))
    imdb_rating = Column(Integer)

    def __init__(self, name, author, imdb_rating):
        self.name = name
        self.author = author
        self.imdb_rating = imdb_rating
		

class UserMovie(Base):
    __tablename__ = 'TB_USERS_MOVIES'
    um_id = Column(Integer, Sequence('usermovie_id_seq'), primary_key=True)
    u_id = Column(Integer, ForeignKey(User.u_id))
    m_id = Column(Integer, ForeignKey(Movie.m_id))

    def __init__(self, u_id, m_id):
        self.u_id = u_id
        self.m_id = m_id

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
    
	
def create_movie(name, author, imdb_rating):
	movie = Movie(name, author, imdb_rating)
	session.add(movie)
	session.commit()
	return movie.m_id
    
def get_movie_by_id(id):
    result = session.query(Movie).filter(Movie.m_id == id).first()
    return result

def get_movie_by_name(name):
    result = session.query(Movie).filter(Movie.name == name).first()
    return result
    
def get_movies():
	results = session.query(Movie).all()
	return [result for result in results]

def update_movie_info(m_id, name, author, imdb_rating):
    result = session.query(Movie).filter(Movie.m_id == m_id).first()
    if result:
        result.imdb_rating = imdb_rating
        result.name = name
        result.author = author
        session.commit()
    return



def create_user_movie(u_id, m_id):
	user_movie = UserMovie(u_id, m_id)
	session.add(user_movie)
	session.commit()
	return

def remove_user_movie(u_id, m_id):
	session.query(UserMovie).filter(UserMovie.u_id == u_id).filter(UserMovie.m_id == m_id).delete()
	session.commit()
	return
	
def get_movies_for_user(u_id):
	results = session.query(Movie).join(
		UserMovie).filter(UserMovie.u_id==u_id).order_by(
		Movie.imdb_rating).all()
	return results
	
	
	
	
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)