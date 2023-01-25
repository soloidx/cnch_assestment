from typing import List, Optional
from pydantic import BaseModel, conlist, confloat, conint


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


class DeleteAudioFile(CreateAudioFile):
    pass


class User(BaseModel):
    name: str
    email: str
    address: str


class GetUser(User):
    id: int
