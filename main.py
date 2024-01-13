import asyncio
import logging
from data_resolvers_runner import DataResolversRunner

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    resolver_runner = DataResolversRunner('./appsettings.json')
    await resolver_runner.resolve_data_async()

if __name__ == '__main__':
    asyncio.run(main())