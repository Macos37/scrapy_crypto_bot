from sqlalchemy import select, insert, update, delete
from db.session import get_session
from db.models import CoinsUser, Coin, User
from sqlalchemy.engine import Row

   
async def register_user(user_id: int, first_name: str):
    session = await get_session()
    query = select(User).where(User.tg_id == user_id)
    user_q = await session.execute(query)
    user = user_q.scalars().first()
    if user:
        return 'You already register!'
    else:
        user = User(
            tg_id=user_id,
            first_name=first_name
        )
        session.add(user)
        await session.commit()
        await session.close()
        return 'Registration completed successfully'
    
   
async def check_coin(coin, session):
    query = select(Coin.name).where(Coin.name == coin)
    coin_query = await session.execute(query)
    coin = coin_query.fetchone()
    if isinstance(coin, Row):
        return True
    return False


async def add_coin(coin: str, user_id: int):
    session = await get_session()
    if await check_coin(coin, session):
        query = CoinsUser(
            user_tg_id = user_id,
            token_id = coin
        )
        session.add(query)
        await session.commit()
        await session.close()
        return 'Done'
    return 'such coin does not exist'

   
async def get_user_token(user_id: int):
    session = await get_session()
    query = select(Coin.name, Coin.price, Coin.percent_change_24h).\
        join(CoinsUser, Coin.name == CoinsUser.token_id).\
            join(User, CoinsUser.user_tg_id == User.tg_id).\
                filter(User.tg_id == user_id)
    coin_query = await session.execute(query)
    coin = coin_query.fetchall()
    await session.close()
    coins = ''
    for name, price, perc_change_24h in coin:
        coins += f"{name} = {price} , {perc_change_24h}\n"
    coin_query.close()
    return coins
        
        
