import sys, asyncio
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

app = FastAPI()

@app.get("/greet")
async def greet(name: str = "World"):
    return {"message": f"Hello, {name}!"}