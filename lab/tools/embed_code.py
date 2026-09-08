# -*- coding: utf-8 -*-
"""把 lab 中的完整代码嵌入 article.md 附录（机械式代码注入）。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTICLE = os.path.join(ROOT, "article.md")
FILES = [
    ("lab/browser_agent.py", "browser_agent.py", "python"),
    ("lab/experiments.py", "experiments.py", "python"),
]


def main():
    with open(ARTICLE, "r", encoding="utf-8") as fh:
        text = fh.read()
    start_marker = "<!-- APPENDIX_CODE_START -->"
    end_marker = "<!-- APPENDIX_CODE_END -->"
    parts = []
    for rel, label, lang in FILES:
        path = os.path.join(ROOT, rel)
        with open(path, "r", encoding="utf-8") as fh:
            code = fh.read().rstrip()
        parts.append("#### %s（%s）\n\n```%s\n%s\n```\n" % (label, rel, lang, code))
    body = "\n".join(parts)
    if start_marker not in text or end_marker not in text:
        raise RuntimeError("markers not found")
    head = text.split(start_marker)[0] + start_marker + "\n"
    tail = end_marker + text.split(end_marker)[1]
    with open(ARTICLE, "w", encoding="utf-8") as fh:
        fh.write(head + body + "\n" + tail)
    print("embedded code appendix OK")


if __name__ == "__main__":
    main()
