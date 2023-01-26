from typing import Optional

from pydantic import BaseModel, conlist, confloat, conint, EmailStr


class AudioFile(BaseModel):
    ticks: conlist(item_type=confloat(le=-10.0, ge=-100.0), min_items=15, max_items=15)
    selected_tick: conint(ge=0, le=14)
    session_id: int
    step_count: int


class CreateAudioFile(AudioFile):
    id: Optional[int]

    class Config:
        orm_mode = True


class UpdateAudioFile(CreateAudioFile):
    pass


class DeleteAudioFile(BaseModel):
    session_id: int
    step_count: int


class User(BaseModel):
    name: str
    email: EmailStr
    address: str


class CreateUser(User):
    id: Optional[int]

    class Config:
        orm_mode = True


class UpdateUser(CreateUser):
    pass


class DeleteUser(CreateUser):
    pass
