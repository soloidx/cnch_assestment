from typing import Optional

from sqlalchemy.orm import Session

from project.crud.base import CRUDBase
from project.models import audio_file as audio_file_model
from project.schema import AudioFile, CreateAudioFile, UpdateAudioFile


class CRUDAudioFile(CRUDBase[AudioFile, CreateAudioFile, UpdateAudioFile]):
    def get_by_session_id_and_step_count(
        self, db, session_id: int, step_count: int
    ) -> audio_file_model.AudioFile:
        return self.get(
            db,
            None,
            [
                audio_file_model.AudioFile.session_id == session_id,
                audio_file_model.AudioFile.step_count == step_count,
            ],
        )

    def remove_by_session_id_and_step_count(
        self, db: Session, session_id: int, step_count: int
    ) -> Optional[audio_file_model.AudioFile]:
        return self.remove(
            db,
            _id=None,
            filter_expressions=[
                audio_file_model.AudioFile.session_id == session_id,
                audio_file_model.AudioFile.step_count == step_count,
            ],
        )


audio_file = CRUDAudioFile(audio_file_model.AudioFile)
