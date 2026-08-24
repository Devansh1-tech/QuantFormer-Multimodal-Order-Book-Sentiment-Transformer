import json


def serialize(data: dict) -> bytes:
    """
    Convert Python dictionary to JSON bytes.
    """
    return json.dumps(data).encode("utf-8")


def deserialize(data: bytes) -> dict:
    """
    Convert JSON bytes back to dictionary.
    """
    return json.loads(data.decode("utf-8"))