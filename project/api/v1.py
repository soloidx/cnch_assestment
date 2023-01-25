from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project.crud.audo_file import audio_file as crud_audio_file
from project.deps import get_db
from project.exceptions import SessionIdIntegrityError
from project.schema import AudioFile, CreateAudioFile, DeleteAudioFile

router = APIRouter()


@router.post(
    "/audio_files/",
    tags=["audio-files"],
    description="Create a new audio file",
    response_model=CreateAudioFile,
)
def create_audio_file(
    audio: AudioFile = Body(embed=True), db: Session = Depends(get_db)
):
    try:
        data_audio = crud_audio_file.create(db, obj_in=audio)
    except IntegrityError as err:
        raise SessionIdIntegrityError("The session_id value already exists")
    return data_audio


@router.put(
    "/audio_files/",
    tags=["audio-files"],
    description="Create a new audio file",
    response_model=CreateAudioFile,
)
def update_audio_file(
    audio: AudioFile = Body(embed=True), db: Session = Depends(get_db)
):
    audio_obj = crud_audio_file.get_by_session_id_and_step_count(
        db, audio.session_id, audio.step_count
    )
    if audio_obj is None:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        data_audio = crud_audio_file.update(db, db_obj=audio_obj, obj_in=audio)
    except IntegrityError as err:
        raise SessionIdIntegrityError("The session_id value already exists")
    return data_audio


@router.delete(
    "/audio_files/",
    tags=["audio-files"],
    description="Create a new audio file",
    response_model=Optional[CreateAudioFile],
)
def delete_audio_file(
    audio: DeleteAudioFile = Body(embed=True), db: Session = Depends(get_db)
):
    data_audio = crud_audio_file.remove_by_session_id_and_step_count(
        db, audio.session_id, audio.step_count
    )
    return data_audio
