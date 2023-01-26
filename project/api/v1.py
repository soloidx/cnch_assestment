from typing import Optional, List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from project.crud.audo_file import audio_file as crud_audio_file
from project.crud.user import user as crud_user
from project.deps import get_db
from project.exceptions import SessionIdIntegrityError, UserEmailIntegrityError
from project.schema import (
    AudioFile,
    CreateAudioFile,
    DeleteAudioFile,
    User,
    CreateUser,
    UpdateUser,
    DeleteUser,
)

router = APIRouter()


@router.get(
    "/audio_files/",
    tags=["audio-files"],
    description="List and search for audio files",
    response_model=List[CreateAudioFile],
)
def list_audio_file(session_id: Optional[int] = None, db: Session = Depends(get_db)):
    audio_files = crud_audio_file.get_by_session_id(db, session_id)
    return audio_files


@router.post(
    "/audio_files/",
    tags=["audio-files"],
    description="Create a new audio file",
    response_model=CreateAudioFile,
)
def create_audio_file(
    audio: AudioFile = Body(embed=True), db: Session = Depends(get_db)
):
    if crud_audio_file.is_duplicated_session_id(db, audio):
        raise SessionIdIntegrityError(
            "The session_id/step_count combination already exists"
        )
    data_audio = crud_audio_file.create(db, obj_in=audio)
    return data_audio


@router.put(
    "/audio_files/",
    tags=["audio-files"],
    description="Updates an audio file",
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

    # this is not needed because the only way to identify an audio object is by session_id and
    # step count but,  in case we used a unique id we need to check for conflicts on update

    # if audio_obj.session_id != audio.session_id or audio_obj.step_count != audio.step_count:
    #     if crud_audio_file.is_duplicated_session_id(db, audio):
    #         raise SessionIdIntegrityError("The session_id value already exists")

    data_audio = crud_audio_file.update(db, db_obj=audio_obj, obj_in=audio)
    return data_audio


@router.delete(
    "/audio_files/",
    tags=["audio-files"],
    description="Deletes an audio file",
    response_model=Optional[CreateAudioFile],
)
def delete_audio_file(
    audio: DeleteAudioFile = Body(embed=True), db: Session = Depends(get_db)
):
    data_audio = crud_audio_file.remove_by_session_id_and_step_count(
        db, audio.session_id, audio.step_count
    )
    return data_audio


@router.get(
    "/user/",
    tags=["users"],
    description="Retrieves and search a list of users",
    response_model=List[CreateUser],
)
def list_users(session_id: Optional[int] = None, db: Session = Depends(get_db)):
    users = crud_user.get_multi(db)
    return users


@router.post(
    "/user/",
    tags=["users"],
    description="Create a new user",
    response_model=CreateUser,
)
def create_user(user: User = Body(embed=True), db: Session = Depends(get_db)):
    if crud_user.is_duplicated_email(db, user):
        raise UserEmailIntegrityError("There is another user with the same email")

    _user = crud_user.create(db, obj_in=user)
    return _user


@router.put(
    "/user/{user_id}",
    tags=["users"],
    description="Updates the user information",
    response_model=UpdateUser,
)
def update_user(
    user: User = Body(embed=True),
    user_id: int = Path(title="The id of the user"),
    db: Session = Depends(get_db),
):
    user_db = crud_user.get(db, user_id)

    if user_db.email != user.email and crud_user.is_duplicated_email(db, user):
        raise UserEmailIntegrityError("There is another user with the same email")

    user_obj = crud_user.update(db, db_obj=user_db, obj_in=user)
    return user_obj


@router.delete(
    "/user/{user_id}",
    tags=["users"],
    description="Deletes an user",
    response_model=Optional[DeleteUser],
)
def delete_user(
    user_id: int = Path(title="The id of the user"), db: Session = Depends(get_db)
):
    user = crud_user.remove(db, _id=user_id)
    return user
