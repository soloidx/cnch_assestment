import sqlalchemy.exc
from fastapi import APIRouter, Body, Depends

from project.schema import AudioFile, CreateAudioFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.deps import get_db
from project.crud.audo_file import audio_file as crud_audio_file
from project.exceptions import SessionIdIntegrityError


router = APIRouter()


@router.post("/audio_files/", tags=["audio-files"], description="Create a new audio file", response_model=CreateAudioFile)
def create_audio_file(audio: AudioFile = Body(embed=True), db: Session = Depends(get_db)):
    try:
        data_audio = crud_audio_file.create(db, obj_in=audio)
    except IntegrityError as err:
        raise SessionIdIntegrityError("The session_id value already exists")
    return data_audio
