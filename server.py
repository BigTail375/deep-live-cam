from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
import base64, io, uvicorn
from modules.core import process_api
import os
import shutil
import uuid

app = FastAPI()

async def save_input_files(target, source):
    PATH = './images'
    try:
        with open(os.path.join(PATH, target.filename), 'wb') as f:
            shutil.copyfileobj(target.file, f)
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        target.file.close()

    try:
        with open(os.path.join(PATH, source.filename), 'wb') as f:
            shutil.copyfileobj(source.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        source.file.close()

@app.post("/item")
async def read_root(
    target: UploadFile = File(...),
    source: UploadFile = File(...),
    face_enhancer: bool = Form(...),
):
    print (target.filename)
    if face_enhancer:
        frame_processors = ['face_swapper', 'face_enhancer']
    else:
        frame_processors = ['face_swapper']
    await save_input_files(target, source)
    target_path = target.filename
    source_path = source.filename
    output = str(uuid.uuid4()) + target_path[-4:]
    PATH = './images'
    process_api(os.path.join(PATH, source_path), os.path.join(PATH, target_path), os.path.join(PATH, output), frame_processors, True, False, False, False, False, False, False, 'libx264', 18, False, True, None, 'cuda', None)
    img = open(os.path.join(PATH, output), 'rb')

    if output.endswith('.jpg'):
        media_type = "image/jpeg"
    elif output.endswith('.mp4'):
        media_type = "video/mp4"
    elif output.endswith('.gif'):
        media_type = "image/gif"
    else:
        raise ValueError("Unsupported file format")
    
    return StreamingResponse(io.BytesIO(img.read()), media_type=media_type)
