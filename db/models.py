
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,String,VARCHAR,Integer,BigInteger,ForeignKey

Base = declarative_base()



class CoinsUser(Base):
    
    __tablename__= 'coins_user'
    
    id = Column(Integer, nullable=True, autoincrement=True)
    user_tg_id = Column(BigInteger, ForeignKey('user_tg.tg_id'), primary_key=True)
    token_id = Column(VARCHAR(30), ForeignKey('coin.name'), primary_key=True)

class User(Base):
    
    __tablename__='user_tg'
    
    id = Column(Integer, nullable=True, autoincrement=True)
    tg_id = Column(BigInteger, primary_key=True,index=True)
    first_name = Column(String(30),nullable=True)
    coins = relationship('Coin',secondary='coins_user', back_populates='users', lazy='joined')
    
    def __init__(self, tg_id, first_name):
        self.tg_id = tg_id
        self.first_name = first_name
        

class Coin(Base):
    
    __tablename__= 'coin'
    
    id = Column(Integer,autoincrement=True,nullable=True)
    name = Column(VARCHAR(15),primary_key=True, index=True, unique=True, nullable=True)
    market_cap = Column(BigInteger)
    price = Column(VARCHAR(10))
    percent_change_24h = Column(VARCHAR(4))
    volume_24h = Column(BigInteger)
    users = relationship('User',secondary='coins_user',back_populates='coins', lazy='joined')
    
    def __init__(self, name, market_cap, price, percent_change_24h, volume_24h):
        self.market_cap = market_cap
        self.volume_24h = volume_24h
        self.name = name
        self.price = f'{price:.2f}' if price > 0.1 else f'{price:.6f}'
        self.percent_change_24h = f'{percent_change_24h:.2f}'
        
