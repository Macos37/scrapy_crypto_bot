import websockets
import asyncio
import json


async def track_price_change(symbol):
    url = f"wss://stream.binance.com: 9443/ws/{symbol.lower()}@ticker"
    async with websockets.connect(url) as websocket:
        while True:
            message = json.loads(await websocket.recv())
            new_price = float(message["c"])
            if 'price' in locals():
                change = (new_price-price)/price *100
                print(f"{symbol}: {price} -> {new_price} ({change:.2f}%)")
            price = new_price
            await asyncio.sleep(60)
                    
                    
async def monitor(tokens, percentage=1):
    tasks = [asyncio.create_task(track_price_change(token, percentage)) for token in tokens]
    await asyncio.gather(*tasks)
coins = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LINKUSDT", "BCHUSDT"]
asyncio.run(monitor(coins))