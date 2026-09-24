"""check_sample.py：按 sample/encoded.json 走一圈，打印验收面。"""
import json
import os
import sys

from pctdecode import Decoder


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "encoded.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    decoder = Decoder(spec["plus_as_space"])
    decoded = decoder.decode(spec["text"])
    streamed = decoder.decode_stream(spec["stream_text"])
    position = decoder.locate(spec["bad_text"])
    plain = Decoder(False).decode(spec["plus_only_text"])
    blob = decoder.persist()
    reborn = Decoder(spec["plus_as_space"])
    restored = reborn.restore(blob)
    print("解码结果 =", decoded)
    print("多字节字符还原 =", spec["multibyte_expect"])
    print("流式解码结果 =", streamed.get("text"))
    print("流式解码的余量 =", streamed.get("remainder"))
    print("非法序列的位置 =", position)
    print("加号不转空格时 =", plain)
    print("解出的字节数 =", spec["byte_count"])
    print("恢复后的解码计数 =", restored.get("decoded"))
    print("不变量（解码后的字节序列长度与原文一致） =", spec["length_invariant"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
