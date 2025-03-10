from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
import base64, io, uvicorn
from modules.core import process_api
import os

app = FastAPI()

@app.post("/item")
async def read_root(
    source_path: str = Form(...),
    target_path: str = Form(...),
    output_path: str = Form(...),
    face_enhancer: bool = Form(...),
):
    if face_enhancer:
        frame_processors = ['face_swapper', 'face_enhancer']
    else:
        frame_processors = ['face_swapper']
    PATH = './images'
    process_api(os.path.join(PATH, source_path), os.path.join(PATH, target_path), os.path.join(PATH, output_path), frame_processors, True, False, False, False, False, False, False, 'libx264', 18, False, True, None, 'cuda', None)

    return {"Hello": "World"}
