from typing import Optional, List

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

    def get_by_session_id(
        self, db: Session, session_id: Optional[int]
    ) -> List[audio_file_model.AudioFile]:
        exp = []
        if session_id is not None:
            exp = [audio_file_model.AudioFile.session_id == session_id]

        return self.get_multi(db, filter_expressions=exp)

    def is_duplicated_session_id(self, db: Session, audio: AudioFile):
        count = (
            db.query(self.model)
            .filter(
                audio_file_model.AudioFile.session_id == audio.session_id,
                audio_file_model.AudioFile.step_count == audio.step_count,
            )
            .count()
        )
        return count > 0


audio_file = CRUDAudioFile(audio_file_model.AudioFile)
