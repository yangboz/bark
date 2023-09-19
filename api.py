import uvicorn

from fastapi import FastAPI, Query

from fastapi import FastAPI, Header
from pydantic import BaseModel


from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

##bark module related
from transformers import AutoProcessor, BarkModel
import scipy
hgmodelname="suno/bark-small"
processor = AutoProcessor.from_pretrained(hgmodelname)
model = BarkModel.from_pretrained(hgmodelname)
import os
import sys

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    text: str = 'what a nice day!'
    preset: str= 'v2/en_speaker_0'
    rate: str = 0.75
    gen_dir:str ='gen_audios'
    filename: str ='bark_out.wav'
    tokens:int  =100
    lang:str='en'

app = FastAPI(title="SMKT-AIGCapps",
    description="SMKTtech enpowering AI",
    summary="SMKTtechAIGC's example app. yangboz at your service.",
    version="0.0.1",
    terms_of_service="http://smartkit.club/terms/",
    contact={
        "name": "SMKT-AIGCapps the Amazing AIGC apps.",
        "url": "https://github.com/smartkit",
        "email": "contact@smartkit.club",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)
app.selected_lang = "en"
version = f"{sys.version_info.major}.{sys.version_info.minor}"
app.mount("/gen_audios/", StaticFiles(directory="gen_audios", html=True), name="gen_audios") 
# @app.on_event("startup")
# async def startup_event():
#     """
#     Load all the necessary models and data once the server starts.
#     """
#     hgmodelname="suno/bark-small"
# processor = AutoProcessor.from_pretrained(hgmodelname)
# model = BarkModel.from_pretrained(hgmodelname)
# def get_prompt() =
###TODO  https://github.com/yangboz/bark/blob/main/bark/generation.py

# @app.get('/set_lang')##more on https://suno-ai.notion.site/
# async def set_prompts(_q: str = Query("en", enum=["en", "us", "cn", "ru","de"])):
     # app.selected_lang = _q
    # return {"selected": app.selected_lang}


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')
@app.get("/info")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"Hello world! From FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}
@app.post("/items/audio")
async def gen_audio(item: Item):
    # return {"name": item.text, "preset": item.preset}
    #audio file gen process
    audio_file_dir='gen_audios/'
    voice_preset = item.preset

    inputs = processor(item.text)
    audio_array = model.generate(**inputs,pad_token_id=item.tokens)
    audio_array = audio_array.cpu().numpy().squeeze()
    audio_filename =item.filename
    #save as file.
    sample_rate = model.generation_config.sample_rate
    physic_audio_filename = os.getcwd()+"/"+item.gen_dir+"/"+item.filename
    print("physic_audio_filename:",physic_audio_filename)
    scipy.io.wavfile.write(physic_audio_filename, rate=sample_rate, data=audio_array)
    ##Write file to disk. This simulates some business logic that results in a file sotred on disk
    # with open(os.path.join(audio_file_dir, item.filename), 'wb') as disk_file:
        # file_bytes = await file.read()
    print(f"Generated audio file named {physic_audio_filename} . ")
    ##more audio gen:https://github.com/yangboz/bark/blob/main/bark/generation.py
    return FileResponse(item.gen_dir+"/"+item.filename, media_type="audio/mpeg")
    ##or video
    #return FileResponse(video_path, media_type="video/mp4")

    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
           <audio controls>
<source src="http://0.0.0.0:8000/gen_audios/bark_out.wav" type="audio/mpeg">
</audio>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
       
        ##TODO video，https://stackoverflow.com/questions/75510956/fastapi-return-text-and-video-with-sound

    
     

if __name__ == '__main__':
    uvicorn.run("api:app", reload=True)
