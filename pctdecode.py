"""pctdecode.py：百分号编码解码（单趟扫描内核）。"""
from __future__ import annotations

import json

_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")


class Decoder:
    def __init__(self, plus_as_space: bool = True):
        self.plus_as_space = plus_as_space
        self.decoded = 0
        self.errors = 0

    def _scan(self, text: str, stream: bool = False):
        """单趟扫描：%HH 出一个字节，其余字符按 UTF-8 计字节。

        返回 (字节序列, 余量)。stream 为真时，末尾不完整的 % 或 %H
        不进结果，原样放进余量；否则按普通字符处理。
        """
        buf = bytearray()
        plus = self.plus_as_space
        n = len(text)
        i = 0
        remainder = ""
        while i < n:
            ch = text[i]
            if ch == "%":
                pair = text[i + 1:i + 3]
                if len(pair) == 2 and pair[0] in _HEX_DIGITS and pair[1] in _HEX_DIGITS:
                    buf.append(int(pair, 16))
                    i += 3
                    continue
                if stream and i + 2 >= n:
                    remainder = text[i:]
                    break
                self.errors += 1
                buf.append(0x25)  # '%'
                i += 1
            elif ch == "+" and plus:
                buf.append(0x20)
                i += 1
            else:
                buf.extend(ch.encode("utf-8"))
                i += 1
        return bytes(buf), remainder

    def decode(self, text: str) -> str:
        data, _ = self._scan(text)
        self.decoded += len(data)
        return data.decode("utf-8", errors="replace")

    def decode_stream(self, text: str) -> dict:
        data, remainder = self._scan(text, stream=True)
        return {"text": data.decode("utf-8", errors="replace"), "remainder": remainder}

    def locate(self, text: str) -> int | None:
        """返回第一个非法 % 序列的下标；全部合法时返回 None。"""
        n = len(text)
        i = 0
        while i < n:
            if text[i] == "%":
                pair = text[i + 1:i + 3]
                if len(pair) == 2 and pair[0] in _HEX_DIGITS and pair[1] in _HEX_DIGITS:
                    i += 3
                    continue
                return i
            i += 1
        return None

    def persist(self) -> bytes:
        return json.dumps(self.stats()).encode("utf-8")

    def restore(self, blob: bytes = None) -> dict:
        if blob is not None:
            state = json.loads(blob.decode("utf-8"))
            self.decoded = state["decoded"]
            self.errors = state["errors"]
            self.plus_as_space = state["plus_as_space"]
        return self.stats()

    def stats(self) -> dict:
        return {"decoded": self.decoded, "errors": self.errors, "plus_as_space": self.plus_as_space}
