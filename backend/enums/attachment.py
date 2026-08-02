from enum import Enum

class AttachmentType(str,Enum):
    AUDIO = 'audio'
    PDF = 'pdf'


class MimeType(Enum):
    PDF = "application/pdf"
    MPEG = "audio/mpeg"
    WAV = "audio/wav"
    MP4 = "audio/mp4"

