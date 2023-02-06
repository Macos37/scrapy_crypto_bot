import websockets
import asyncio
import json

async def track_price_change(symbol,percentage=0.001):
    url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"
    async with websockets.connect(url) as websocket:
        while True:
            message = json.loads(await websocket.recv())
            new_price = float(message["c"])
            if 'price' in locals():
                change = (new_price-price)/price *100
                print(f"{symbol}: {price} -> {new_price} ({change:.2f}%)")
            price = new_price
            
async def monitor(tokens,percentage=0.001):
    tasks = [asyncio.create_task(track_price_change(token,percentage)) for token in tokens]
    await asyncio.gather(*tasks)
    

t = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LINKUSDT", "BCHUSDT"]
asyncio.run(monitor(t))