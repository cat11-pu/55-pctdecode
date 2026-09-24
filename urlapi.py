"""urlapi.py：对外门面（老接口 decode 不能改）。"""
from __future__ import annotations

from pctdecode import Decoder


class Url:
    def __init__(self, plus_as_space: bool = True):
        self.decoder = Decoder(plus_as_space)

    def decode(self, text: str) -> str:
        return self.decoder.decode(text)

    def decode_stream(self, text: str) -> dict:
        return self.decoder.decode_stream(text)

    def locate(self, text: str) -> int:
        return self.decoder.locate(text)

    def snapshot(self) -> bytes:
        return self.decoder.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.decoder.restore(blob)
