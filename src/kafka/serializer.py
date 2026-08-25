import json


def serialize(data) -> bytes:
    """
    Convert Python dictionary to JSON bytes.
    """
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    return json.dumps(data).encode("utf-8")


def deserialize(data) -> dict:
    """
    Convert JSON bytes back to dictionary.
    """
    if data is None:
        return {}
    if isinstance(data, dict):
        return data
    if isinstance(data, (bytes, bytearray)):
        data = data.decode("utf-8")
    if isinstance(data, str):
        return json.loads(data)
    return data