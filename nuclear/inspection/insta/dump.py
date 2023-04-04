import base64
from pathlib import Path
import zlib


def dump_snippet(filename: str = 'inspection.py') -> str:
    text: str = Path(filename).read_text()
    code: str = encode_text(text)
    return code


def encode_text(text: str) -> str:
    compressed = zlib.compress(text.encode())
    b64: bytes = base64.b64encode(compressed)
    return b64.decode()
