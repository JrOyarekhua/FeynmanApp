from enum import Enum


class AttachmentType(str,Enum):
    NOTES = 'notes'
    EXPLANATION = 'explanation'
    

class NoteMimeTypes(str,Enum):
    PDF = "application/pdf"
    
class ExplanationMimeTypes(str,Enum):
    MPEG = "audio/mpeg"
    WAV = "audio/wav"
    MP4 = "audio/mp4"

VALID_MIME_TYPES = {
    AttachmentType.NOTES.value:[val.value for val in NoteMimeTypes],
    AttachmentType.EXPLANATION.value:[val.value for val in ExplanationMimeTypes]
}