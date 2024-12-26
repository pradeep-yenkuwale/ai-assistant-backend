import asyncio
import os
import time
from fastapi import APIRouter, Body, File, Path, Request, Response, UploadFile
from fastapi.encoders import jsonable_encoder
from app.helpers.response_helpers import response_helper
from app.helpers.stream_helpers import StreamingCallback
from app.helpers.voice_helpers import detect_language
from app.lib.process_query import stream_text, stream_voice
from app.lib.user import add_user, get_search_logs, get_user
from app.lib.voice.audio_to_text import transcribe_audio
from app.models.user_query import UserModel
from fastapi.responses import FileResponse, StreamingResponse
from main import root_path

router = APIRouter()

TEMP_DIR = "./temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

TEMP_AUDIO_DIR = root_path + "/temp_audio"

@router.get('/user/stream/text')
async def stream_user_query(request: Request):
    input_object = dict(request.query_params)
    language = request.query_params.get("language")
    return StreamingResponse(stream_text(input_object, language), media_type="text/event-stream")

@router.post('/user/text')
async def get_user_text(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    user_text = transcribe_audio(file_path)

    print("Generated user text", user_text)
    return user_text

@router.post('/user/stream/voice')
async def stream_user_voice(request: Request, file: UploadFile = File(...)):
    input_object = dict(request.query_params)
    audio_path = os.path.join(TEMP_DIR, file.filename)
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    user_text = transcribe_audio(audio_path)
    print("user_text", user_text)
    language_detected = detect_language(user_text)
    print("language_detected", language_detected)
    if language_detected not in ['ar', 'en']:
        language_detected = 'en'
    query_object = {
        "query": user_text,
        "context": input_object["context"],
        "sent_at": input_object["sent_at"]
    }
    stream_user_input = stream_voice(query_object, TEMP_AUDIO_DIR, language_detected)
    print("Stream user input", stream_user_input)
    output_file = "temp_audio/output" + "_" + language_detected + ".wav"
    print("output_file", output_file)
    with open(output_file, "rb") as audio_file:
            audio_data = audio_file.read()
    return Response(content=audio_data)

@router.get('/user/validate')
async def validate_user(request: Request):
    try:
        email = request.query_params.get("email")
        user = await get_user(email)
        if(user==None):
            return response_helper(user, 200, "Invalid user")
        return response_helper(user, 200, "User retrieved")
    except Exception as error:
        print("error", error)
        return response_helper(None, 500, "Oops! It seems like we're experiencing a technical issue at the moment. Please try again later. If the issue persists, feel free to click the help icon located at the top right corner to raise your concern. We apologize for the inconvenience!")

@router.post('/user')
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return response_helper(new_user, 200, "User have been added successfully")

@router.get('/user/logs')
async def get_user_logs(request: Request):
    email = request.query_params.get("email")
    user_logs = await get_search_logs(email)
    print("user_logs", user_logs)
    if(user_logs==None):
        return response_helper([], 200, "User search logs retreived")

    return response_helper(user_logs, 200, "User search logs retreived")