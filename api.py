import uvicorn

from fastapi import FastAPI, Query

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    txt: str
    prompt: str

app = FastAPI(title="SMKT-AIGCapps",
    description="SMKTtech enpowering AI",
    summary="SMKTtechAIGC's example app. yangboz at your service.",
    version="0.0.1",
    terms_of_service="http://smartkit.club/terms/",
    contact={
        "name": "SMKT-AIGCapps the Amazing",
        "url": "https://github.com/smartkit",
        "email": "contact@smartkit.club",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


@app.get('/set_prompts')
async def set_prompts(_q: str = Query("en", enum=["en", "us", "cn", "ru","de"])):
    return {"selected": _q}

@app.post("/items/")
async def gen_audio(item: Item):
    return {"name": item.text, "prompt": item.prompt}

if __name__ == '__main__':
    uvicorn.run("api:app", reload=True)
