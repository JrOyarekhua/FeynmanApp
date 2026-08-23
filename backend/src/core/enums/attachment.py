from enum import Enum

class AttachmentType(str,Enum):
    AUDIO = 'audio'
    PDF = 'pdf'
    
    @classmethod
    def from_mime(atype_cls, mime: str) -> "AttachmentType":
        """
        Map a MIME type string to an `AttachmentType` in a scalable way.

        Notes
        -----
        - This is a `@classmethod`, so the first parameter (`atype_cls`) is the
          class object (the same value normally named `cls`). It allows the
          method to reference enum members (for example `atype_cls.PDF`) in a
          way that remains correct if the enum is subclassed or renamed.
        - The method tries exact MIME -> type mappings first, then falls back
          to prefix-based patterns (for example `audio/*` → `AUDIO`).

        Args
        ----
        atype_cls: type
            The `AttachmentType` class object (automatically supplied by Python
            when this classmethod is called). Named `atype_cls` here for
            readability to emphasize it's the enum class, not an instance.
        mime: str
            The MIME content-type string to map (for example
            ``application/pdf`` or ``audio/mpeg``).

        Returns
        -------
        AttachmentType
            The matching enum member.

        Raises
        ------
        ValueError
            If the MIME type cannot be mapped.

        Example
        -------
        >>> AttachmentType.from_mime("application/pdf")
        <AttachmentType.PDF: 'pdf'>
        """
        # exact mime -> attachment type mappings
        exact_map = {
            "application/pdf": atype_cls.PDF,
            "audio/mpeg": atype_cls.AUDIO,
            "audio/wav": atype_cls.AUDIO,
            "audio/mp4": atype_cls.AUDIO,
        }

        if mime in exact_map:
            return exact_map[mime]

        # prefix pattern mappings
        if mime.startswith("audio/"):
            return atype_cls.AUDIO

        raise ValueError(f"Unknown mime type for attachment mapping: {mime}")


class MimeType(Enum):
    PDF = "application/pdf"
    MPEG = "audio/mpeg"
    WAV = "audio/wav"
    MP4 = "audio/mp4"

