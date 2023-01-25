from project.crud.base import CRUDBase

from project.models import audio_file as audio_file_model
from project.schema import AudioFile, CreateAudioFile, UpdateAudioFile


class CRUDAudioFile(CRUDBase[AudioFile, CreateAudioFile, UpdateAudioFile]):
    pass


audio_file = CRUDAudioFile(audio_file_model.AudioFile)
