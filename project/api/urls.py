from fastapi import APIRouter, Body

from project.api.v1 import data_audio
from project.api.schema import AudioFile


router = APIRouter()


@router.post("/audio_files/", tags=["audio-files"], description="Create a new audio file")
def create_audio_file(audio: AudioFile = Body(embed=True)):
    data_audio.create_data_audio(audio)
    return {"result": "ok"}
