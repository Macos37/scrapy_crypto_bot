from sqlalchemy import Column,Integer,String,BigInteger
from sqlalchemy.ext.asyncio import create_async_engine,AsyncConnection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class User(Base):
    
    __tablename__='users'
    id = Column(Integer)
    user_tg_id = Column(BigInteger,primary_key=True)
    tokens = Column(String(255),unique=True)
    
    def __repr__(self):
        return f'User - {self.user_tg_id}, tokens - {self.tokens}'
    
async def create_conn_db():
    engine = create_async_engine('postgresql+psycopg2://crypto_db:2314@192.168.0.102:5432/crypto_db',future=True)
    async_session = sessionmaker(engine,expire_on_commit=False,class_=AsyncConnection)
    return async_session
    
    

    
    