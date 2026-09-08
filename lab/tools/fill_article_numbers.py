# -*- coding: utf-8 -*-
"""用 all_stats.json 的实际数字回填 article.md 占位符。"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATS_PATH = os.path.join(ROOT, "lab", "outputs", "all_stats.json")
ARTICLE_PATH = os.path.join(ROOT, "article.md")


def main():
    with open(STATS_PATH, "r", encoding="utf-8") as fh:
        stats = {s["scenario"]: s for s in json.load(fh)}

    def g(scenario, key):
        return stats.get(scenario, {}).get(key, 0)

    repl = {
        "{{ATTACK_EXFIL}}": str(g("attack", "exfil_events")),
        "{{LABEL_EXFIL}}": str(g("defense_label", "exfil_events")),
        "{{POLICY_EXFIL}}": str(g("defense_policy", "exfil_events")),
        "{{POLICY_BLOCK}}": str(g("defense_policy", "blocked_events")),
    }
    with open(ARTICLE_PATH, "r", encoding="utf-8") as fh:
        text = fh.read()
    for k, v in repl.items():
        text = text.replace(k, v)
    with open(ARTICLE_PATH, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("replaced:", repl)


if __name__ == "__main__":
    main()
