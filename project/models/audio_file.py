from sqlalchemy import Column, String, Integer, JSON

from project.models.database import Base


class AudioFile(Base):
    __tablename__ = 'audio_files'

    id = Column(Integer, primary_key=True, index=True)
    ticks = Column(JSON)
    selected_tick = Column(Integer)
    session_id = Column(Integer)
    step_count = Column(Integer)
