# -*- coding: utf-8 -*-
"""从 all_stats.json 生成图4对比柱状图（SVG）。"""
import json
import os

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(LAB, "images", "fig4_results.svg")


def load_stats():
    path = os.path.join(LAB, "outputs", "all_stats.json")
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return {s["scenario"]: s for s in data}


def build(stats):
    scenarios = [
        ("baseline", "基线\n（良性网页）"),
        ("attack", "恶意网页\n（无防御）"),
        ("defense_label", "来源标注\n防御"),
        ("defense_policy", "收件人\n白名单"),
    ]
    groups = []
    for key, label in scenarios:
        s = stats.get(key, {})
        groups.append(
            {
                "label": label,
                "exfil": s.get("exfil_events", 0),
                "blocked": s.get("blocked_events", 0),
                "n": s.get("n", 8),
            }
        )

    W, H = 1280, 740
    x0, y0, x1, y1 = 150, 175, 1160, 610
    max_y = 8
    gw = (x1 - x0) / len(groups)
    bw = 62
    lines = []
    lines.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="\'Microsoft YaHei\',\'PingFang SC\',Arial,sans-serif">' % (W, H, W, H))
    lines.append("  <defs>")
    lines.append('    <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ef4444"/><stop offset="1" stop-color="#dc2626"/></linearGradient>')
    lines.append('    <linearGradient id="gAmber" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbbf24"/><stop offset="1" stop-color="#f59e0b"/></linearGradient>')
    lines.append('    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.15"/></filter>')
    lines.append("  </defs>")
    lines.append('  <rect x="0" y="0" width="%d" height="%d" fill="#f8fafc"/>' % (W, H))
    lines.append('  <text x="%d" y="50" text-anchor="middle" font-size="25" font-weight="700" fill="#0f172a">图4　浏览器智能体间接注入攻击与防御对比（每场景 8 轮，模型 qwen2.5:7b）</text>' % (W // 2))

    def y(v):
        return y1 - (y1 - y0) * (v / max_y)

    for v in range(0, max_y + 1):
        yy = y(v)
        lines.append('  <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e2e8f0" stroke-width="1.5"/>' % (x0, yy, x1, yy))
        lines.append('  <text x="%d" y="%.1f" text-anchor="end" font-size="14" fill="#64748b">%d</text>' % (x0 - 12, yy + 5, v))
    lines.append('  <text x="66" y="%d" text-anchor="middle" font-size="14" fill="#475569" transform="rotate(-90 66 %d)">次数 / 8 轮</text>' % ((y0 + y1) // 2, (y0 + y1) // 2))

    for i, g in enumerate(groups):
        cx = x0 + gw * i + gw / 2
        series = [("exfil", g["exfil"], "url(#gRed)"), ("blocked", g["blocked"], "url(#gAmber)")]
        for j, (key, v, grad) in enumerate(series):
            if v == 0:
                continue
            bx = cx - bw * 1.25 + j * bw
            by = y(v)
            lines.append('  <rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="6" fill="%s" filter="url(#shadow)"/>' % (bx, by, bw - 8, y1 - by, grad))
            lines.append('  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">%d</text>' % (bx + (bw - 8) / 2, by - 8, v))
        for k, line in enumerate(g["label"].split("\n")):
            lines.append('  <text x="%.1f" y="%d" text-anchor="middle" font-size="14.5" font-weight="600" fill="#334155">%s</text>' % (cx, 636 + k * 22, line))

    lines.append('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#94a3b8" stroke-width="2"/>' % (x0, y1, x1, y1))
    legend = [("url(#gRed)", "外带事件（发到攻击者邮箱）"), ("url(#gAmber)", "被白名单拦截")]
    lx = 430
    for grad, text in legend:
        lines.append('  <rect x="%d" y="116" width="24" height="16" rx="4" fill="%s"/>' % (lx, grad))
        lines.append('  <text x="%d" y="129" font-size="14" fill="#334155">%s</text>' % (lx + 32, text))
        lx += 420
    lines.append("</svg>")
    return "\n".join(lines)


def main():
    stats = load_stats()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(build(stats))
    print("written:", OUT)


if __name__ == "__main__":
    main()
