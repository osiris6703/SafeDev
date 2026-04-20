
import aiohttp
import asyncio

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def download_parallel(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for url in urls]
        return await asyncio.gather(*tasks)
