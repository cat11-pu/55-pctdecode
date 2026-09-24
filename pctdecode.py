"""pctdecode.py：百分号编码解码（基线：字符串替换）。"""
from __future__ import annotations


class Decoder:
    def __init__(self, plus_as_space: bool = True):
        self.plus_as_space = plus_as_space
        self.decoded = 0
        self.errors = 0

    def decode(self, text: str) -> str:
        """基线：只替换 %20，别的强转，非法序列不报。"""
        result = text.replace("%20", " ")
        if self.plus_as_space:
            result = result.replace("+", " ")
        self.decoded += len(result)
        return result

    def decode_stream(self, text: str) -> dict:
        raise NotImplementedError("流式解码还没实现")

    def locate(self, text: str) -> int:
        raise NotImplementedError("非法序列定位还没实现")

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"decoded": self.decoded, "errors": self.errors, "plus_as_space": self.plus_as_space}
