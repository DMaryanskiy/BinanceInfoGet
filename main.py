import asyncio
import logging
from datetime import datetime, timedelta

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE = "https://api.binance.com"

async def get_max_price() -> int:
    path = "/api/v3/klines"
    # Get a time an hour ago
    start = datetime.utcnow() - timedelta(hours=1)

    url = BASE + path
    params = {
        "symbol": "XRPUSDT",
        "interval": "1h",
        "startTime": int(start.timestamp() * 1000),
        "limit": 1
    }

    req = requests.get(url, params)
    if req.status_code == 200:
        data = req.json()
        # return max price ("high" property from first and only kline)
        return data[0][2]
    else:
        logger.error(req.reason)

async def main():
    while True:
        path = "/api/v3/ticker/price"
        
        url = BASE + path
        params = {
            "symbol": "XRPUSDT"
        }
        max_price = float(await get_max_price())
        
        req = requests.get(url, params)
        if req.status_code == 200:
            data = req.json()
            price = float(data["price"])
            if abs(price - max_price) > max_price * 0.01:
                logger.info(price)

        else:
            logger.error(req.reason)
        
        await asyncio.sleep(5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
