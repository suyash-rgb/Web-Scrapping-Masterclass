import sys, asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from scrapy.cmdline import execute

if __name__ == "__main__":
    execute()