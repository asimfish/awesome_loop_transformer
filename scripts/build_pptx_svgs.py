#!/usr/bin/env python3
"""Emit ppt-master flat-page SVGs (1280x720) for the summary deck, to be exported as an
editable PPTX with ppt-master's `svg_to_pptx.py --quick-generate`.

Usage:
  python3 scripts/build_pptx_svgs.py --out <ppt-master project>/svg_output
Then, inside the ppt-master checkout (python >= 3.10, deps from its requirements.txt):
  python3 scripts/svg_quality_checker.py <project> --quick-generate --canonical-authoring --stage final --json
  python3 scripts/svg_to_pptx.py <project> --quick-generate --no-notes -o slides.pptx

Design follows ppt-master's `technical-deepdive` style (blueprint palette). Every visible root
<g> carries an id and data-pptx-bounds; paragraphs are one <text> with positioned <tspan> lines.
"""
import argparse, pathlib, re
from xml.sax.saxutils import escape

W, H = 1280, 720
P = dict(field="#0F1C2B", surface="#16283C", surface2="#1D3450", ink="#E6EDF5", ink2="#A9B8CB",
         structure="#4A7BA7", focus="#4FC9E8", caution="#E8A54F", good="#6FD39A")
FONT = "Microsoft YaHei"

# ---------- text measurement (deliberately conservative) ----------
def cw(ch, fs):
    o = ord(ch)
    if o >= 0x2E80: return 1.02 * fs
    if ch in "iljtf.,;:!|'·": return 0.36 * fs
    if ch == " ": return 0.32 * fs
    if ch.isupper(): return 0.74 * fs
    if ch.isdigit(): return 0.62 * fs
    return 0.58 * fs

def tokens(text):
    """Split into (token, bold) with **bold** markup; CJK chars are single tokens."""
    out, bold = [], False
    for part in re.split(r"(\*\*)", text):
        if part == "**": bold = not bold; continue
        buf = ""
        for ch in part:
            if ord(ch) >= 0x2E80 or ch in "，。；：、（）！？—…":
                if buf: out.append((buf, bold)); buf = ""
                out.append((ch, bold))
            elif ch == " ":
                if buf: out.append((buf, bold)); buf = ""
                out.append((" ", bold))
            else:
                buf += ch
        if buf: out.append((buf, bold))
    return out

def wrap(text, fs, width):
    lines, cur, curw = [], [], 0.0
    for tok, bold in tokens(text):
        tw = sum(cw(c, fs) for c in tok) * (1.06 if bold else 1.0)
        if cur and curw + tw > width and tok != " ":
            lines.append(cur); cur, curw = [], 0.0
            if tok == " ": continue
        if not cur and tok == " ": continue
        cur.append((tok, bold)); curw += tw
    if cur: lines.append(cur)
    # never start a wrapped line with a separator dot (the exporter would read it as a list marker)
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0][0] in ("·", "•", "—"):
            lines[i - 1].append((" ", False)); lines[i - 1].append(lines[i].pop(0))
            if lines[i] and lines[i][0][0] == " ": lines[i].pop(0)
    return [l for l in lines if l]

def line_xml(line):
    segs, buf, state = [], "", None
    for tok, bold in line:
        if state is None: state = bold
        if bold != state:
            segs.append((buf, state)); buf, state = "", bold
        buf += tok
    if buf: segs.append((buf, state))
    if all(not b for _, b in segs):
        return escape("".join(s for s, _ in segs).rstrip())
    return "".join(f'<tspan font-weight="bold">{escape(s)}</tspan>' if b else escape(s) for s, b in segs).rstrip()

PAD = 0.12  # widen exported frames by ~12% so renderers that ignore wrap="none" do not re-wrap lines

def padded(line, fs, anchor=None, avail=None):
    """line_xml plus invisible NBSP padding (trailing for start-anchored, leading for end-anchored),
    capped so the padded line stays within 97% of the available width."""
    est = sum(cw(c, fs) for tok, _ in line for c in tok)
    want = PAD * est
    if avail is not None:
        want = min(want, max(0.0, 0.93 * avail - est))
    n = int(want / (0.32 * fs))
    if avail is None or est + 3 * 0.32 * fs <= 0.93 * avail:
        n = max(n, 3)   # short strings ("87%", "HE+") need slack too
    pad = "\u00a0" * n
    xml = line_xml(line)
    return (pad + xml) if anchor == "end" else (xml + pad)

def text_el(x, y, width, text, fs, fill, weight="normal", leading=1.45, anchor=None, max_lines=None):
    """Return (xml, height). y is the top of the block."""
    lines = wrap(text, fs, width * 0.80)   # safety margin vs. the exporter's glyph estimator / font substitution
    if max_lines: lines = lines[:max_lines]
    attrs = f'x="{x}" y="{y + fs:.0f}" font-size="{fs}" fill="{fill}"'
    if weight != "normal": attrs += f' font-weight="{weight}"'
    if anchor: attrs += f' text-anchor="{anchor}"'
    # all-<tspan> form (dy="0" first): required when a line starts with an inline run
    body = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else fs*leading:.1f}">{padded(l, fs, anchor, width)}</tspan>' for i, l in enumerate(lines))
    return f'<text {attrs}>{body}</text>', fs * (1 + leading * (len(lines) - 1)) + fs * 0.3

def fit_text(x, y, w, h, text, fs, fill, weight="normal", leading=1.45, min_fs=12, anchor=None):
    while fs > min_fs:
        xml, hh = text_el(x, y, w, text, fs, fill, weight, leading, anchor)
        if hh <= h: return xml, hh
        fs -= 1
    return text_el(x, y, w, text, fs, fill, weight, leading, anchor)

# ---------- page primitives ----------
class Page:
    def __init__(self, role="content"):
        self.role = role; self.parts = []; self.n = 0
    def g(self, gid, x, y, w, h, inner):
        self.parts.append(f'<g id="{gid}" data-pptx-bounds="{x:.0f} {y:.0f} {w:.0f} {h:.0f}">{inner}</g>')
    def render(self, lang=None):
        bg = f'<rect id="bg" data-pptx-role="background" x="0" y="0" width="{W}" height="{H}" fill="{P["field"]}"/>'
        lang_attr = f' lang="{lang}"' if lang else ''  # ppt-master reads the deck language from page 1
        return (f'<svg xmlns="http://www.w3.org/2000/svg"{lang_attr} viewBox="0 0 {W} {H}" data-pptx-page-role="{self.role}" '
                f'font-family="{FONT}">{bg}{"".join(self.parts)}</svg>')

def rect(x, y, w, h, fill, stroke=None, rx=10, sw=1, opacity=None):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity is not None: s += f' fill-opacity="{opacity}"'
    return s + "/>"

def hline(x1, x2, y, stroke, sw=1):
    return f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" stroke="{stroke}" stroke-width="{sw}"/>'

MX, MT = 64, 40   # margins
def title_block(page, kicker, title, tfs=26):
    inner, y = "", MT
    if kicker:
        k, kh = text_el(MX, y, W - 2 * MX, kicker, 13, P["focus"], "bold", 1.2)
        inner += k; y += 22
    t, th = text_el(MX, y, (W - 2 * MX) * 0.84, title, tfs, P["ink"], "bold", 1.22)
    inner += t
    h = (y - MT) + th + 10
    page.g("title", MX, MT, W - 2 * MX, h, inner)
    return MT + h + 10  # body top

def footer(page, left, num):
    inner = ""
    if left:
        t, _ = text_el(MX, H - 30, 1060, left, 10.5, P["ink2"], leading=1.2, max_lines=1)
        inner += t
    n, _ = text_el(W - MX, H - 30, 60, str(num), 11, P["structure"], anchor="end")
    inner += n.replace(f'x="{W - MX}"', f'x="{W - MX}"')
    page.g("footer", MX, H - 32, W - 2 * MX, 22, inner)

def takeaway(page, text, y, h=44):
    inner = rect(MX, y, W - 2 * MX, h, P["focus"], rx=4, opacity=0.08)
    inner += f'<rect x="{MX}" y="{y}" width="3" height="{h}" fill="{P["focus"]}"/>'
    t, _ = fit_text(MX + 16, y + 8, W - 2 * MX - 32, h - 12, text, 14, P["ink"], leading=1.35, min_fs=11)
    page.g("takeaway", MX, y, W - 2 * MX, h, inner + t)

def paras_el(x, y, width, paras, fs, fill, leading=1.42, gap=7):
    """All paragraphs of a body in ONE <text> frame so later paragraphs flow after wrapped
    lines instead of overlapping (a larger dy gap or a bullet marker starts a new paragraph)."""
    spans, total, first = [], 0.0, True
    for ptxt in paras:
        bullet = ptxt.startswith("- ")
        txt = ("• " + ptxt[2:]) if bullet else ptxt
        for i, line in enumerate(wrap(txt, fs, width * 0.80)):
            if first:
                dy = 0
            elif i == 0:
                dy = fs * leading + gap
            else:
                dy = fs * leading
            spans.append(f'<tspan x="{x}" dy="{dy:.1f}">{padded(line, fs, None, width)}</tspan>')
            total += fs if first else dy
            first = False
    xml = f'<text x="{x}" y="{y + fs:.0f}" font-size="{fs}" fill="{fill}">{"".join(spans)}</text>'
    return xml, total + fs * 0.35

def card(page, gid, x, y, w, h, heading, paras, accent=None, fs=13.5, heading_color=None):
    """paras: list of strings (bullets if starting with '- ')."""
    stroke = {"focus": P["focus"], "warn": P["caution"]}.get(accent, P["structure"])
    inner = rect(x, y, w, h, P["surface"], stroke, sw=1.2 if accent else 0.8)
    cy = y + 14
    if heading:
        hc = heading_color or (P["caution"] if accent == "warn" else P["focus"])
        t, th = text_el(x + 16, cy, w - 32, heading, 15, hc, "bold", 1.2)
        inner += t; cy += th + 4
    avail = y + h - 12 - cy
    while True:
        xml, hh = paras_el(x + 16, cy, w - 32, paras, fs, P["ink"])
        if hh <= avail or fs <= 11: break
        fs -= 0.5
    inner += xml
    page.g(gid, x, y, w, h, inner)

def kpi(page, gid, x, y, w, h, value, label, color=None):
    inner = rect(x, y, w, h, P["surface"], P["structure"], sw=0.8)
    v, vh = fit_text(x + 16, y + 14, w - 32, 44, value, 32, color or P["focus"], "bold", 1.1, min_fs=20)
    l, _ = fit_text(x + 16, y + 12 + vh + 2, w - 32, h - vh - 40, label, 12.5, P["ink2"], leading=1.3, min_fs=10)
    page.g(gid, x, y, w, h, inner + v + l)

def table(page, gid, x, y, w, cols, rows, fs=13, hl=None, row_h=None, colors=None, center_lines=False):
    """cols: list of (header, frac, align); rows: list of lists; hl: set of row indices to highlight;
    colors: {(row, col): fill} overrides; center_lines: centre each cell's wrapped lines in the row
    (default keeps the single-line offset used by the original pages)."""
    rh = row_h or (fs * 2.0)
    inner = ""
    cx, xs = x, []
    for hdr, frac, al in cols:
        xs.append((cx, w * frac, al)); cx += w * frac
    def cell(cxx, cww, al, txt, yy, color, bold=False):
        ax = cxx + 6 if al == "l" else cxx + cww - 6
        anchor = None if al == "l" else "end"
        t, _ = text_el(ax, yy, cww - 12, txt, fs, color, "bold" if bold else "normal", 1.2, anchor)
        return t
    yy = y
    for (hdr, frac, al), (cxx, cww, _) in zip(cols, xs):
        inner += cell(cxx, cww, al, hdr, yy + 4, P["focus"], True)
    yy += rh
    inner += hline(x, x + w, yy, P["structure"], 1.2)
    for i, row in enumerate(rows):
        if hl and i in hl:
            inner += rect(x, yy + 1, w, rh - 2, P["focus"], rx=3, opacity=0.10)
        for j, ((cxx, cww, al), txt) in enumerate(zip(xs, row)):
            bold = txt.startswith("**") and txt.endswith("**")
            body = txt.strip("*")
            bh = fs
            if center_lines:
                n = len(wrap(body, fs, (cww - 12) * 0.80))
                bh = fs * (1 + 1.2 * (n - 1))
            color = (colors or {}).get((i, j), P["ink"])
            inner += cell(cxx, cww, al, body, yy + (rh - bh) / 2 - 2, color, bold)
        yy += rh
        inner += hline(x, x + w, yy, P["structure"], 0.5)
    page.g(gid, x, y, w, yy - y + 10, inner)
    return yy - y + 10

# ---------- content ----------
def cols3(y, h, gap=16):
    w = (W - 2 * MX - 2 * gap) / 3
    return [(MX + i * (w + gap), y, w, h) for i in range(3)]
def cols2(y, h, gap=16, split=0.5):
    w1 = (W - 2 * MX - gap) * split; w2 = (W - 2 * MX - gap) - w1
    return [(MX, y, w1, h), (MX + w1 + gap, y, w2, h)]

pages = []

# 1 cover
pg = Page("cover")
inner = ""
t, _ = text_el(MX, 186, 1100, "awesome_loop_transformer · 汇总报告", 14, P["focus"], "bold"); inner += t
t, _ = text_el(MX, 222, 1100, "循环 Transformer 与循环深度", 54, P["ink"], "bold", 1.1); inner += t
t, _ = text_el(MX, 304, 1100, "GPT-6 Astra 背后的 Loop 技术全景：五篇核心论文 · 六十篇相关文献 · 十条趋势洞察（2018–2026）", 22, P["ink2"], leading=1.35); inner += t
t, _ = text_el(MX, 386, 1100, "基于微信文章《刚刚，GPT-6 Astra 背后的 Loop 技术全被挖出来了》串起的 5 篇论文，逐篇核对原文；arXiv 全量检索补齐 2018–2026 年约 60 篇相关工作（综述文献图谱）· 首版 2026-09-06", 15, P["ink2"], leading=1.5); inner += t
t, _ = text_el(MX, 440, 1100, "论文列表现收录 333 篇 · 2026-11-06 更新（新增 211 篇，见「九月以来的六个变化」）", 15, P["ink2"], leading=1.5); inner += t
t, _ = text_el(MX, 476, 1100, "github.com/asimfish/awesome_loop_transformer", 15, P["focus"]); inner += t
pg.g("cover_text", MX, 176, W - 2 * MX, 330, inner)
footer(pg, "视觉规范：ppt-master · technical-deepdive（blueprint）", 1)
pages.append(pg)

# 2 TLDR
pg = Page(); yb = title_block(pg, "一页结论", "三句话说清这个方向在 2026 年的位置")
for i, (x, y, w, h) in enumerate(cols3(yb, 400)):
    c = [("focus", "首胜", ["**算力匹配下第一次赢。** Loopie-20B-A2B 在与 Qwen3-30B-A3B 复现版相同的每步墙钟时间下训练 800B token，约 600B 后反超；SMELT 在 FLOPs / 参数 / KV 三重匹配下省 6.8–18% 训练 FLOPs。", "胜利发生在「两步 · 逐层 · MoE」这个窄配置里。"]),
         (None, "2 vs 32", ["**「循环几次」分裂成两个 regime。** 预训练算力受限 → 2（Loopie、LoopCoder-v2、SMELT、Nanbeige）；推理算力可变 → 越多越好但要自适应（Huginn 到 32–64）。", "「三次以上回退」是 PLT 并行设计的位置税，不是循环的普适上限。"]),
         (None, "超加", ["**隐式循环 + 显式 CoT 互补。** LoopCoder-v2 在 R=2 上叠加 thinking 模式，LiveCodeBench +26.9，远超两者单独之和；LOTUS 首次在 3B 规模用潜在 CoT 追平显式 CoT。", "标准 GRPO 与循环模型错配（RLTT、LoopRPT）。"])][i]
    card(pg, f"card{i+1}", x, y, w, h, c[1], c[2], accent=c[0], fs=14.5, heading_color=[P["focus"], P["caution"], P["good"]][i])
takeaway(pg, "**给工程团队的一句话：**中段循环、两次、layer-loop、MoE 骨干；部署前实测延迟和 KV cache——训练算力匹配的胜利不等于推理成本匹配的胜利。", yb + 416)
footer(pg, "数字来源：Loop the Loopies (2607.16051) · SMELT (2609.01343) · LoopCoder-v2 (2606.18023) · LOTUS (2606.31779)", 2)
pages.append(pg)

# 3 concept
pg = Page(); yb = title_block(pg, "概念", "什么是循环 Transformer：同一组参数在深度上重复使用，深度与参数量解耦")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 470, split=0.5)
card(pg, "granularity", x1, y1, w1, h1, "四种循环粒度", [
    "- **model-loop**（UT 2018 · Huginn 核心 · Ouro）：L1→L2→L3→L1→L2→L3，整栈输出喂回",
    "- **block-loop**（Huginn 三段式 · Hyperloop · Training-Free · SMELT）：首尾层不循环，中段重复；每步重新注入输入 e",
    "- **layer-loop**（Loopie · Training-Free layer-mode · MixerLoop）：L1→L1→L2→L2→L3→L3，每层先局部迭代再下传",
    "- **潜变量条件化**（Coconut · PLT 的 CLP · Latent Recurrent Transformer）：上一轮或上一 token 的隐状态作为条件注入；PLT 的 CLP 正是「两次饱和」的来源"], fs=14)
card(pg, "axes", x2, y2, w2, h2, "三条正交设计轴", [
    "- **循环次数**：固定（Loopie、LoopCoder-v2）/ 训练随机·推理任选（Huginn）/ 逐 token 自适应停机（ACT、MoR、Think-at-Hard、RecurTrace）",
    "- **训练方式**：从头预训练（Huginn、Ouro、Loopie）/ 改造已有模型（Relaxed Recursive、Retrofitted Recurrence）/ 免训练（Training-Free、Program-of-Layers）",
    "- **目标把循环当什么**：截断展开的 LM（Huginn）/ 不动点（DEQ、STARS、Attractor）/ ODE 细化（Training-Free）/ 有监督潜在 CoT（LOTUS）/ 循环步 RL（RLTT、LoopRPT）"], fs=14)
footer(pg, "粒度分类沿用微信原文与 Loopie / Training-Free 的术语", 3)
pages.append(pg)

# 4 timeline
pg = Page(); yb = title_block(pg, "时间线", "八年：从 bAbI 过拟合的补丁，到前沿架构的候选组件")
rows = [["2016", "Neural GPU · Adaptive Computation Time：循环 + 自适应停机的前身"],
        ["**2018-07**", "**Universal Transformers**：跨时间步共享参数、坐标嵌入、ACT；bAbI 联合训练错误率 22.1 → 0.29"],
        ["2019–2022", "ALBERT · Deep Equilibrium Models · deep thinking 系列（随机展开 + 输入注入）· 路径独立均衡模型"],
        ["2023–2024", "Looped Transformers as Programmable Computers · <10% 参数学会 ICL 算法 · MoEUT · Relaxed Recursive Transformers · Coconut"],
        ["**2025-02**", "**Recurrent Depth / Huginn-3.5B**：800B token 训成，定名 recurrent depth；Saunshi 证明 k 层循环 L 次 ≈ kL 层"],
        ["2025-06–11", "HRM · Mixture-of-Recursions · TRM · Ouro（2.6B，7.7T token）· Parallel Loop Transformer · 扩散式并行采样器 · Think-at-Hard"],
        ["2026-01–04", "LoopFormer（ICLR）· RLTT（ICML）· LoopRPT · Hyperloop · 迭代深度扩展律 φ=0.46 · Loop-Think-Generalize（COLM）"],
        ["**2026-05**", "**Training-Free Looped Transformers** · MELT · LT2 · LoopQ · STARS（ICML）· Attractor Models"],
        ["**2026-06**", "**LoopCoder-v2**（7B PLT，18T token，「只循环一次」）· 残差缩放 1/N 理论 · LOTUS · Program-of-Layers（ICML）"],
        ["**2026-07**", "**Loop the Loopies!**（Loopie-20B-A2B，算力匹配首胜）· Looped Latent Attention（KV 32×）· Nanbeige4.2-3B（28T token 产品模型）"],
        ["2026-09", "SMELT 扩展律（省 6.8–18% 训练 FLOPs）· RecurTrace · GPT-6 Astra 发布，The Information 报道其使用 recurrent depth"]]
table(pg, "timeline", MX, yb, W - 2 * MX, [("时间", 0.12, "l"), ("事件", 0.88, "l")], rows, fs=13.5, hl={1, 4, 7, 8, 9}, row_h=36)
footer(pg, "高亮行 = 微信文章的五篇核心论文", 4)
pages.append(pg)

# 5 five papers table
pg = Page(); yb = title_block(pg, "五篇核心论文", "一张表看五篇论文：各自回答一个问题，合起来是一条论证链")
cols = [("", 0.12, "l"), ("Universal Transformers", 0.17, "l"), ("Recurrent Depth (Huginn)", 0.18, "l"), ("Training-Free Looped", 0.18, "l"), ("LoopCoder-v2", 0.17, "l"), ("Loop the Loopies", 0.18, "l")]
rows = [["arXiv / 时间", "1807.03819 · 2018-07", "2502.05171 · 2025-02", "2605.23872 · 2026-05", "2606.18023 · 2026-06", "2607.16051 · 2026-07"],
        ["回答的问题", "机制是什么", "现代规模能训成吗", "已有模型能白拿吗", "部署时循环几次", "算力匹配下能赢吗"],
        ["粒度 / 次数", "model-loop · ACT", "block(2,4,2) · r̄=32", "中间 4 层 · K=3 级 RK", "model-loop(PLT) · R=2", "layer-loop · R=2"],
        ["训练", "从头 ~65M", "从头 3.5B · 800B tok", "**不训练** 0.6B–30B", "从头 7B · 18T tok", "从头 20B-A2B · 3.5T"],
        ["关键数字", "bAbI 22.1→0.29", "r 4→32：ARC-E 49.1→69.9", "45 格 87% 非负", "SWE-V 43.0→64.4→27.6", "600B tok 后反超 30B-A3B"],
        ["核心贡献", "定义循环深度 + 停机", "首次训成；隐空间轨道", "层 = 欧拉步；子步", "两步饱和诊断；CoT 超加", "Loopie Recipe；SPT"],
        ["最常被误读", "—", "「同样 0.8T」基线实为 0.18T", "收益上限约 2–3 点", "非单调是 PLT 特有", "算力匹配 = 实测步时"]]
th = table(pg, "papers", MX, yb, W - 2 * MX, cols, rows, fs=12.5, hl={4}, row_h=40)
takeaway(pg, "**论证链：**UT 提出机制 → Huginn 证明可训 → Training-Free 证明可白拿并给出 ODE 解释 → LoopCoder-v2 给出部署时的循环次数与代价 → Loopie 在算力匹配下赢。", yb + th + 16)
footer(pg, "详细解读见 reports/zh/01–05", 5)
pages.append(pg)

# 6 UT
pg = Page(); yb = title_block(pg, "论文 01 · 2018", "Universal Transformers：把 N 层换成同一层重复 T 次，再让每个位置自己决定想多久")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 250, split=0.62)
card(pg, "mech", x1, y1, w1, h1, "机制", ["每个时间步 t 对所有位置并行：自注意力交换信息 → 位置无关的转移函数（FFN 或深度可分离卷积）。参数跨时间步共享；坐标嵌入 P^t = 位置正弦 + 时间步正弦，每步重新加入。ACT 停机：每位置预测停机概率，累计过阈值即冻结状态。", "**留下的三个问题**：参数—计算比（翻译只 +0.9 BLEU）；训练不稳定；推理成本无讨论。"], fs=14)
kpi(pg, "kpi_act", x2, y2, w2, h2, "2.3 → 3.8", "bAbI 中需要 1 / 2 / 3 条支撑事实的问题，ACT 平均步数 2.3 / 3.1 / 3.8：模型按需分配计算。干扰名词越多、优势越大——这个模式七年后在 Huginn 上原样重现。")
rows = [["bAbI 10K 联合训练（错误率 / 失败任务）", "22.1 (12/20)", "0.47 (0/20)", "**0.29 (0/20)**"],
        ["LAMBADA LM 测试困惑度", "7321", "319", "**142**"],
        ["WMT14 En-De BLEU（base）", "28.0", "**28.9**", "–"],
        ["Copy / Reverse / Addition 字符准确率（训 40 测 400）", ".53 / .13 / .07", "**.91 / .96 / .34**", "–"]]
table(pg, "ut_table", MX, yb + 266, W - 2 * MX, [("任务", 0.46, "l"), ("Transformer", 0.18, "r"), ("UT", 0.18, "r"), ("UT + 动态停机", 0.18, "r")], rows, fs=13, row_h=32)
footer(pg, "Dehghani, Gouws, Vinyals, Uszkoreit, Kaiser · ICLR 2019 · arXiv 1807.03819", 6)
pages.append(pg)

# 7 Huginn
pg = Page(); yb = title_block(pg, "论文 02 · 2025-02", "Huginn-3.5B：Prelude → Core ×r → Coda，随机采样循环次数、只对最后 8 步反传")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 300, split=0.5)
card(pg, "arch", x1, y1, w1, h1, "架构与训练", [
    "e = P(x); s₀ ~ N(0,σ²I); sᵢ = R(e, sᵢ₋₁); p = C(s_r)",
    "- **输入注入**：像梯度下降每步都要用数据；只在第一步喂 e 的迭代不可能稳定。随机 s₀ + 注入 → 路径独立。",
    "- **训练目标**：r ~ 对数正态泊松（均值 32，重尾）；**只对最后 k=8 步反传**，内存与 r 无关。",
    "- **规模**：h=5280，(2,4,2)，3.5B 参数；r=32 时有效深度 132 层。800B token，4096 块 MI250X，恒定学习率 4e-5，三明治归一化。",
    "- **两次失败**：隐状态坍缩（token 间相关度→1）；循环坍缩（r=1 与 r=32 困惑度相同）。"], fs=13)
rows = [["4", "49.07", "27.99", "43.46", "23.39", "–"], ["8", "65.11", "35.15", "58.54", "25.29", "–"], ["16", "69.49", "37.71", "64.67", "31.25", "–"], ["**32**", "**69.91**", "**38.23**", "**65.21**", "**31.38**", "**34.80 / 42.08**"]]
table(pg, "huginn_table", x2, y2, w2, [("循环 r", 0.13, "l"), ("ARC-E", 0.16, "r"), ("ARC-C", 0.16, "r"), ("HellaSwag", 0.19, "r"), ("MMLU", 0.14, "r"), ("GSM8K CoT", 0.22, "r")], rows, fs=13, hl={3}, row_h=34)
kpi(pg, "kpi_flops", x2, y2 + 190, w2, 110, "32B / 50B", "「3.5B 打出 50B」是 FLOPs 等效：预训练每 token 原始 FLOPs 接近 32B 稠密模型，测试时可扩到 ~50B 的等效算力；基准分数接近 OLMo-7B、落后 OLMo-2。")
takeaway(pg, "**公平对照只有 0.18T token（Table 4）：**同为 0.18T，循环模型 ARC-E 53.62 vs 46.42、GSM8K CoT 10.24 vs 2.20；后 620B token 学到的能力全部编码在循环里（r=1 成绩几乎不动）。", yb + 316, h=52)
footer(pg, "Geiping, McLeish, Jain, Kirchenbauer, Singh, Bartoldson, Kailkhura, Bhatele, Goldstein · arXiv 2502.05171", 7)
pages.append(pg)

# 8 Huginn continued
pg = Page(); yb = title_block(pg, "论文 02 · 续", "循环在哪里最有用、白拿的能力、以及隐空间里发生了什么")
for i, (x, y, w, h) in enumerate(cols3(yb, 400)):
    c = [("循环在哪里最有用", ["- 难任务（ARC-C）收益大，事实回忆（SciQ）收益小", "- 上下文越多需要的循环越多：ARC-C 零样本 8–12 次饱和，25–50 shot 需 32 次", "- 开卷 OBQA +11.0（38.2→49.2）：记的事实少，对上下文推理强", "- **传播误差**：把 0.8T 的循环模型与 0.18T 的基线并列成「同样 0.8T」夸大了差距"], None),
         ("零样本免费能力", ["- 逐 token 自适应停机（KL < 5e-4）：MT-Bench 5.63→5.56", "- KV cache 共享（预算 4）：不掉分", "- 连续 CoT：用上一 token 的 s_r 热启动，少走 1–2 步", "- 自推测解码：少循环起草、多循环验证，无需 draft 模型"], None),
         ("隐空间里发生了什么", ["- 多数 token 收敛到不动点", "- 数值推理 token（GSM8K 的「3」）进入多维**轨道**", "- 关键 token（「wrong」）表现为单向**滑块**，可能在计步", "- 换 s₀ 轨迹形状不变（路径独立）", "- Lu et al. 2025 用 logit lens 只发现有限的可解释潜在 CoT 证据"], None)][i]
    card(pg, f"c{i+1}", x, y, w, h, c[0], c[1], fs=14)
footer(pg, "Table 4 · Figure 9–12 · Section 6–7", 8)
pages.append(pg)

# 9 Training-free
pg = Page(); yb = title_block(pg, "论文 03 · 2026-05", "Training-Free Looped Transformers：一层是 ODE 的一步欧拉，正确的循环是细分步长而不是走到 t=K")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 300, split=0.46)
card(pg, "insight", x1, y1, w1, h1, "关键洞察", [
    "pre-norm 层 L(x)=x+F(x) ⇔ ẋ=F(x) 上 h=1 的前向欧拉；post-loop 层是在 x(t=1) 的近似上训练的。",
    "- **朴素循环** x←g(x) 做 K 次 = 积分到 t=K，后段层没见过 → 掉点（2 维小网络：K=8 时 MSE 335）",
    "- **子步** x←(1−1/K)x+(1/K)g(x)：以 O(1/K) 逼近同一个 x(t=1)；K=8 时 MSE 1.04",
    "- **特殊 RK 表**：输出 = β·g(x₀) + (1−β)·F^K(x₀)，β 是锚点权重",
    "- Anderson / heavy-ball / Aitken 都不如 RK 子步 → 预训练中段**不是压缩映射**，是 ODE 流"], fs=13)
rows = [["Qwen3-4B-Instruct", "MMLU-Pro 5-shot", "57.14", "59.79", "**+2.64**"], ["", "GPQA-Main 0-shot", "33.71", "35.71", "**+2.01**"], ["Llama-3.2-1B-Instruct", "GPQA-Main", "27.90", "29.69", "+1.79"], ["Qwen1.5-MoE-A2.7B", "ARC-Challenge 25-shot", "48.29", "50.60", "**+2.30**"], ["Moonlight-16B-A3B", "OpenBookQA", "31.60", "32.80", "+1.20"], ["DeepSeek-V2-Lite-Chat", "ARC-Challenge", "57.94", "58.79", "+0.85"], ["Qwen3-30B-A3B（事先锁定）", "CSQA / MMLU-flex", "78.71 / 66.67", "79.85 / 67.46", "+1.14 / +0.79"]]
table(pg, "tf_table", x2, y2, w2, [("模型", 0.30, "l"), ("基准", 0.28, "l"), ("基线", 0.15, "r"), ("循环", 0.15, "r"), ("Δ pp", 0.12, "r")], rows, fs=12, hl={0, 3}, row_h=32)
ky = yb + 316
kw = (W - 2 * MX - 32) / 3
kpi(pg, "k1", MX, ky, kw, 104, "87%", "45 个（模型，基准）格子非负；60% 正、27% 中性；配方：中间 4 层、3 级 RK、稠密 block / MoE layer，零调参")
kpi(pg, "k2", MX + kw + 16, ky, kw, 104, "−27.7", "循环整个模型（28 层）掉 27.73 点；n=4 +0.55，n≥6 悬崖；朴素循环 K=6 掉 17.71", P["caution"])
kpi(pg, "k3", MX + 2 * (kw + 16), ky, kw, 104, "0.5", "最优窗口相对深度 0.43–0.71（>1.7B）；小模型前移到 0.25–0.56；MoE 必须 layer-mode（routing thrash）")
footer(pg, "Chen, Li, Liang, Lao, Liu · UT Austin · arXiv 2605.23872 · 收益集中在知识型多选题，小蒸馏模型可能掉分", 9)
pages.append(pg)

# 10 LoopCoder-v2
pg = Page(); yb = title_block(pg, "论文 04 · 2026-06", "LoopCoder-v2：在并行循环 Transformer 里，第二次循环几乎是全部——第三次开始交位置税")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 214, split=0.46)
card(pg, "plt", x1, y1, w1, h1, "PLT 怎样把延迟和 KV 压平", [
    "- **共享 KV + 门控滑窗注意力**：第一轮 KV 冻结共享；后续轮 = 全局分支与局部滑窗（w=64）的逐头门控混合。KV 从 O(RLSd) 降到 O(LSd)",
    "- **跨循环位置偏移 CLP**：B^(r) = Embed(x) + shift(h^(r−1))，上一轮状态右移一位，不同 token 的不同轮次可并行；延迟 ≈ 单次前向",
    "- **代价**：token i 拿到的是邻居的状态 → 位置错配。7B，R∈{1,2,3,4} 各自从头训练 18T token，同一份 SFT，共 100 万 GPU 小时"], fs=12.5)
rows = [["基线 R=1", "81.1", "27.4", "43.0", "14.0", "11.2", "32.2", "38.0"], ["**R=2**", "**84.1**", "**35.4**", "**64.4**", "**31.0**", "**21.0**", "**40.1**", "**46.5**"], ["R=3", "75.0", "28.6", "27.6", "11.0", "12.2", "36.3", "36.9"], ["R=4", "76.8", "24.5", "22.4", "9.3", "9.0", "39.5", "34.3"]]
table(pg, "lc_table", x2, y2, w2, [("7B 模型", 0.19, "l"), ("HE+", 0.11, "r"), ("LCB", 0.11, "r"), ("SWE-V", 0.13, "r"), ("Multi-SWE", 0.16, "r"), ("TB-v2", 0.11, "r"), ("BFCL", 0.09, "r"), ("均值", 0.10, "r")], rows, fs=12.5, hl={1}, row_h=34)
t, _ = text_el(x2, y2 + 192, w2, "Table 2；SWE-V = SWE-bench Verified。R=2 的 64.4 超过 Kimi-Dev-72B（60.4）、Qwen3-235B-A22B（45.2），接近 Qwen3-Coder-480B（67.0）。", 11, P["ink2"], leading=1.3)
pg.g("lc_note", x2, y2 + 190, w2, 34, t)
ky = yb + 230; kw = (W - 2 * MX - 32) / 3
kpi(pg, "k1", MX, ky, kw, 104, "174.6", "有效秩在第 2 轮达峰（172.5 → 158.2 递减）：后续循环在收窄表示子空间；更新方向震荡（cos θ < 0）")
kpi(pg, "k2", MX + kw + 16, ky, kw, 104, "30–45×", "CLP 偏移成本 Ω ≈ 常数，是第 3 轮起边际收益的 30–45 倍——收益递减 + 固定成本 → R=2 达峰", P["caution"])
kpi(pg, "k3", MX + 2 * (kw + 16), ky, kw, 104, "+26.9", "R=2 上叠加显式 CoT（Thinking）：LiveCodeBench 35.4→62.3，CRUX +6.6，超加性", P["good"])
takeaway(pg, "**适用边界：**「两次最优」是 PLT 的性质（每次 R 单独从头训练，CLP 固定税）。顺序循环的 Huginn 到 r=32 单调上升。看有效秩曲线而不是穷举训练来选循环数。", ky + 120)
footer(pg, "Yang et al. · 北航 / IQuest / 澜舟 / 人大 · arXiv 2606.18023", 10)
pages.append(pg)

# 11 Loopie
pg = Page(); yb = title_block(pg, "论文 05 · 2026-07", "Loop the Loopies!：layer-loop + 实测步时匹配 + 两次循环，循环 MoE 第一次在算力匹配下赢")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 260, split=0.5)
card(pg, "recipe", x1, y1, w1, h1, "Loopie Recipe（按实测优化器步时匹配）", [
    "1. 参考 Qwen3-like 30B-A3B（D=2048, L=48, R=1）→ 层数减半、循环两次：种子 (2048, 24, 2)。块执行次数不变，**激活内存减半**（∝ s·b·D·L，随存储深度而非执行深度）",
    "2. 省下的内存换**每卡 micro-batch 翻倍**（梯度累积减半，每步 token 不变）",
    "3. 把效率增益再投资到宽度 / 深度，选实测步时最接近参考的候选 → Loopie-20B-A2B：D=2304，L=27，R=2，名义算力 1.42×，激活内存 0.63×"], fs=13)
card(pg, "why", x2, y2, w2, h2, "为什么 layer-loop、为什么只两次", [
    "- 6B-A0.6B 上 layer-loop 约 1.2T token 后反超 model-loop；消融去掉 layer-loop 明显更差",
    "- 流水线并行友好：一层的所有循环在同一 stage 内完成，无环回依赖",
    "- N× 循环 vs N× 存储层（250B token）：边际收益在 R=2 最大，之后快速衰减",
    "- **SPT 监督预训练**：SFT 的损失掩码 + PT 的优化规模（batch ≥1024、序列 ≥128K、2T token、10 epoch）：预训练与推理指标同时上升，无过拟合、无遗忘"], fs=13)
ky = yb + 276; kw = (W - 2 * MX - 32) / 3
kpi(pg, "k1", MX, ky, kw, 104, "~600B", "800B token 算力匹配对照，约 600B 后反超 Qwen3-30B-A3B 复现版并保持领先；4 级扩展梯全胜且差距不缩小")
kpi(pg, "k2", MX + kw + 16, ky, kw, 104, "81.28", "20B-A2B Thinking MMLU（3.5T token）vs Nemotron 3 Nano 80.52、Cascade 2 81.22（各 25T）；AIME24 92.09")
kpi(pg, "k3", MX + 2 * (kw + 16), ky, kw, 104, "80.42", "6B-A0.6B Thinking 的 AIME24（Ouro 2.6B：62.50）；AIME25 70.83；MATH-500 93.80", P["good"])
takeaway(pg, "**口径：**名义 FLOPs 高 42%，但 MBS 2 vs 1 使每步墙钟时间持平——这是实测训练成本相等，不是 FLOPs 相等；推理成本未报告。", ky + 120)
footer(pg, "Gao, Chen, Xiao, Yang, Tao, Zhou, Dai · IQuest Research · arXiv 2607.16051", 11)
pages.append(pg)

# 12 divider
pg = Page("section")
inner = ""
t, _ = text_el(MX, 230, 1100, "02", 110, P["focus"], "bold", 1.0); inner += t.replace(f'fill="{P["focus"]}"', f'fill="{P["focus"]}" fill-opacity="0.22"')
t, _ = text_el(MX, 350, 1100, "更广的图谱与十条洞察", 50, P["ink"], "bold", 1.1); inner += t
t, _ = text_el(MX, 425, 1100, "arXiv 全量检索 · 约 60 篇直接相关工作 · 十个主题", 20, P["ink2"]); inner += t
pg.g("divider_text", MX, 220, W - 2 * MX, 240, inner)
footer(pg, "", 12)
pages.append(pg)

# 13 map
pg = Page(); yb = title_block(pg, "文献图谱", "十个主题：2026 年上半年每个方向都有了专门的论文")
themes = [("理论", "Giannou 2023 可编程计算机；Saunshi 2025 k 层×L 次 ≈ kL 层；Xu&Sato 2025 循环擅长 DAG、CoT 擅长自约化；Zhang 2026 预算律"),
          ("预训练", "Huginn 3.5B/0.8T · Ouro 2.6B/7.7T · LoopCoder-v2 7B/18T · Loopie 20B-A2B/3.5T · Nanbeige4.2-3B/28T · SMELT 至 54B；循环数 2–4，MoE 成默认"),
          ("效率", "PLT 并行；扩散式采样器 5×；MELT 常数 KV；Looped Latent Attention 跨循环 KV 低秩 32×；LT2 线性注意力；LoopQ W4A4"),
          ("稳定性", "残差缩放需 1/N 而非 1/√L；DeepLoop 指数 1/4→1/2；Fully Looped 稳到 12 次；STARS 谱半径正则；settling / drifting 分类"),
          ("停机", "ACT · PonderNet · MoR（NeurIPS 25）· Think-at-Hard（93% token 不循环）· LoopFormer 弹性深度 · RecurTrace 平均 2.0 次达 56.9%"),
          ("改造", "Relaxed Recursive（逐层 LoRA）· Retrofitted Recurrence 课程 · Training-Free RK 子步 · Program-of-Layers 学跳过 / 重复程序"),
          ("后训练", "RLTT 沿潜在轨迹分配奖励 +10.9% · LoopRPT 强化预训练 · LOTUS 金标 CoT 监督潜在位置追平显式 CoT · LoopMTP · SPT"),
          ("可解释", "轨道 / 滑块（Huginn）· logit lens 证据有限（Lu 2025）· 两尺度动力学 · Jacobian lens：Ouro 每轮重建工作区、Huginn 跨 16 轮携带"),
          ("小模型", "HRM 27M 解数独 / ARC · TRM 7M ARC-AGI-1 45% · Attractor Models 隐式微分、均衡内化 · Denoising Recursion 超过 TRM"),
          ("应用", "LoopViT 18M ARC 65.8% · RD-VLA 0%→90%、80× 加速 · 组合式工具调用随深度提升 · Nanbeige4.2-3B agentic 产品")]
gw = (W - 2 * MX - 4 * 12) / 5; gh = 250
for i, (name, txt) in enumerate(themes):
    r, c = divmod(i, 5)
    x = MX + c * (gw + 12); y = yb + r * (gh + 12)
    card(pg, f"theme{i+1}", x, y, gw, gh, name, [txt], fs=12.5)
footer(pg, "完整清单与摘要：README · data/papers.csv · data/related_abstracts.json", 13)
pages.append(pg)

# 14-16 insights
def insights_page(num, kicker, title, items, foot):
    pg = Page(); yb = title_block(pg, kicker, title)
    n = len(items)
    if n == 3:
        boxes = cols3(yb, 420)
    else:
        (xa, ya, wa, ha), (xb, yb2, wb, hb) = cols2(yb, 200)
        boxes = [(xa, ya, wa, ha), (xb, yb2, wb, hb), (xa, ya + 216, wa, ha), (xb, yb2 + 216, wb, hb)]
    for i, (x, y, w, h) in enumerate(boxes):
        head, body, acc = items[i]
        card(pg, f"ins{i+1}", x, y, w, h, head, [body], accent=acc, fs=13 if n == 3 else 12.5)
    footer(pg, foot, num)
    pages.append(pg)

insights_page(14, "洞察 1–3", "算力匹配的门已过、但门很窄；循环次数分裂成两个 regime；粒度向中间收敛", [
    ("1 · 窄门里的首胜", "Loopie 与 SMELT 第一次在匹配训练成本下赢，但配置极窄：MoE、layer-loop / 中段、两次。Schwethelm 的扩展律解释原因——一次循环只值 r^0.46 份独立参数（截断反传下 0.38），用循环换参数在 FLOPs 匹配下必输；Loopie 是用循环省下的**激活内存**换 micro-batch 再换宽度，理论 FLOPs 看不见这笔红利。", "focus"),
    ("2 · 两个 regime", "最优循环数：Loopie 2 · LoopCoder-v2 2 · SMELT 2 · Nanbeige 2 · Ouro 4 · Huginn 32（可到 64）· RecurTrace 2.0 · Think-at-Hard 在 93% token 上 1。分裂线是**算力约束在哪**：预训练受限 → 2；推理可变 → 按需自适应（Huginn ARC-C 随 few-shot 数从 8 次饱和到 32 次）。「三次以上回退」是 PLT 的位置税。", None),
    ("3 · 粒度变细、位置居中", "整模型（UT）→ 三段式（Huginn）→ 逐层 / 中段（Loopie、Training-Free、SMELT）→ 只循环 mixer（MixerLoop 保留 41.5% 收益、省 45.9% FLOPs）。三条独立证据指向同一位置：深度分数规则 0.43–0.71（众数 0.5）、SMELT 的「中间一半」、Huginn 的首尾层特化。MoE 必须 layer-loop，免训练与从头训练两篇独立一致。", None)],
    "Loopie 2607.16051 · SMELT 2609.01343 · Schwethelm 2604.21106 · MixerLoop 2608.18230 · Training-Free 2605.23872")

insights_page(15, "洞察 4–7", "ODE 流还是不动点？稳定性成了定理；推理成本被拆成三件事；循环与 CoT 互补", [
    ("4 · 两种哲学分化", "Training-Free：预训练中段不是压缩映射，不动点加速器都不如 RK 子步——对**已训练**模型顺着 ODE 流细分步长。另一支把循环**训成**不动点：STARS（谱半径正则）、Fixed-Point Reasoners、Attractor Models。Viakhirev：settling 算子加深不变差；Huginn 属 non-settling，LoopCoder-v2 的 cos θ<0 震荡正是其表现。", None),
    ("5 · 稳定性从经验到定理", "Huginn 的两次失败（2025）到 2026 年成了定理：残差缩放 ε=1/N 而非 1/√L；DeepNorm 指数 1/4→1/2；最优学习率只依赖唯一层数、可跨循环数迁移。Fully Looped 稳到 12 次，LoopMTP 到 15 次。「循环模型难训」这道 2018 年以来的障碍基本被拆除。", None),
    ("6 · 推理成本拆成三个子问题", "延迟：PLT 并行、扩散式并行采样器 5×。KV：共享（Huginn / MoR / MELT）或压缩（LLA：跨循环 KV 低秩，32× 近无损，H200 上批容量 32→768）。量化：LoopQ。三者独立可叠加。**口径警告**：Loopie 的算力匹配是训练步时；推理时每 token 54 次块计算 vs 48，未报延迟。", None),
    ("7 · 互补而非替代", "LoopCoder-v2 R=2 叠加 thinking：LCB +26.9 远超各自之和；LOTUS 用金标 CoT 监督潜在位置，3B 追平显式 CoT，思考延迟降 2.5–6.9×。配套发现：**标准 RL 与循环模型错配**——GRPO 只给最终潜在状态分配 credit；RLTT 沿轨迹分配后 Ouro-2.6B 数学 +10.9%；LoopRPT 在预训练就给潜在步分配强化信号。", "focus")],
    "STARS 2605.26733 · Think Shallow 2608.18222 · 残差缩放 2606.18524 · DeepLoop 2607.13491 · LLA 2607.15456 · RLTT 2602.10520")

insights_page(16, "洞察 8–10", "循环擅长「操作」知识而非「存储」；应用扩到 agent 与具身；生产化开始、工具链没跟上", [
    ("8 · 能力剖面", "Ouro 的对照把优势归因于知识操作而非容量；Huginn 闭卷弱、开卷 +11.0；Frey：循环帮数学、记忆库帮常识，合并才超 iso-FLOP 基线；Dual-Path 学到的门控让标点 / 符号 / 算术 token 走「深」、功能词走「宽」。**最佳搭档**：检索、长上下文、MoE 专家库——把存储外置。", None),
    ("9 · 从谜题到 agent", "2025 年证据集中在数独 / 迷宫 / ARC / GSM8K；2026 年扩到三类：软件工程 agent（LoopCoder-v2 SWE-V +21.4）、工具调用（多步有依赖的调用随深度提升；Nanbeige4.2-3B 以 3B 超 Qwen3.5-9B）、机器人（RD-VLA 0%→>90%，比 token 推理 VLA 快 80×）。共同点：一次前向内维护中间状态与依赖。", None),
    ("10 · 工具链缺口", "五个开源家族：Huginn、Ouro、LoopCoder-v2、Loopie、Nanbeige4.2-3B（28T token，已作为产品发布）。但复现报告显示 Nanbeige 在 HF transformers 上开箱 5 个 bug，修复后层复用仍使注意力内存翻倍。推理框架、量化、KV 管理都没有循环模型的标准接口；Loopie 的 megatron-loopie / vllm-loopie 分支是往这个方向的信号。", "warn")],
    "Ouro 2510.25741 · Frey 2603.08391 · Dual-Path 2605.30202 · Popescu 2608.18171 · RD-VLA 2602.07845 · Halloran 2608.13987")

# 17 what changed since September 2026
pg = Page(); yb = title_block(pg, "九月以来的变化 · 2026-11-06 更新", "九月以来的六个变化（2026-09 – 11）：两次循环不是规律，安全成了新维度")
rows = [["1", "**从头训练不靠 MoE 也胜过匹配基线；事后加循环收益不稳定**", "Loopback 用标准 Transformer **40–75%** 的 Transformer 参数达到更低 loss（token 数与执行深度相同）", "2611.07226", "细化洞察 1"],
        ["2", "**「两次」是现有设计的最优点而非规律；自适应停机节省被高估**", "LOOM 700M 在近似等 FLOPs 下 **5 次**循环最好", "2610.01153", "修正洞察 2"],
        ["3", "**推理部署成为最大技术方向，循环模型进入生产推理引擎**", "LoopVQ 在 SGLang 中把 Ouro 的服务吞吐最多提高到 **6.1 倍**", "2611.05304", "修正洞察 10 工具链；细化洞察 6"],
        ["4", "**循环深度会改变安全行为——十条洞察都没有覆盖的维度**", "Ouro-1.4B-Thinking 半深度下保留 89% 的 GSM8K 准确率，协助有害请求的比例升到 **5.3 倍**", "2610.15218", "新维度；牵涉洞察 7"],
        ["5", "**「操作知识、不存储知识」落到架构：循环内加记忆或状态通道**", "合成编辑实验的事实编辑传播率：有可寻址记忆 **0.71–0.96**，只靠循环 0.04–0.30", "2606.20737", "支持洞察 8"],
        ["6", "**应用扩展到生成式和科学基础模型**", "260M 的 Looped-DiT 以 **1/4.9** 的推理算力超过大 6.5 倍的文生图模型", "2609.40305", "扩展洞察 9"]]
tag = {(i, 4): (P["caution"] if i in (1, 2, 3) else P["focus"]) for i in range(6)}
th = table(pg, "changes", MX, yb, W - 2 * MX, [("#", 0.04, "l"), ("变化", 0.38, "l"), ("关键数字（条件）", 0.32, "l"), ("来源 arXiv", 0.10, "l"), ("对应洞察", 0.16, "l")],
           rows, fs=12.5, hl={1, 2}, row_h=48, colors=tag, center_lines=True)
ky = yb + th + 6; kw = (W - 2 * MX - 32) / 3
kpi(pg, "k1", MX, ky, kw, 104, "211", "2026-11-06 新增：167 篇首版提交于 2026-09-01 至 11-06；44 篇是首轮检索漏掉的 6–8 月论文")
kpi(pg, "k2", MX + kw + 16, ky, kw, 104, "26 / 167", "167 篇新论文中 26 篇以效率为主类：推理部署是最大的技术方向（变化 3）")
kpi(pg, "k3", MX + 2 * (kw + 16), ky, kw, 104, "0.8B", "事后给已训练的 Qwen3/Qwen3.5 加循环，只在 0.8B 上胜过等参数和等 FLOPs 基线（2610.42030）", P["caution"])
takeaway(pg, "**怎么读：**洞察 2 和洞察 10 的工具链部分被修正，洞察 1、6 被细化，洞察 8、9 得到支持和扩展；后训练（洞察 7）需要覆盖模型可能运行的每个深度。", ky + 116)
footer(pg, "数字均出自所引论文的摘要 · 全文：README_zh「九月以来的变化」· README「What changed since September 2026」", 17)
pages.append(pg)

# 18 misreadings
pg = Page(); yb = title_block(pg, "核对", "五处被二次传播放大的说法，对照原文")
rows = [["Huginn「同样 0.8T token」下循环模型碾压基线", "非循环基线只训了 0.18T；同为 0.18T 时循环模型 ARC-E 53.62 vs 46.42、GSM8K CoT 10.24 vs 2.20"],
        ["「循环两次就够，三次以上回退」是循环 Transformer 的规律", "是 PLT（跨循环位置偏移）特有的现象；每个 R 单独从头训练；Huginn 到 r=32 单调上升"],
        ["Loopie 与 Qwen3-30B-A3B「相同算力」", "相同**实测优化器步时**；Loopie 名义 FLOPs 高 42%，推理成本未报告；对照的是 800B token 自复现版"],
        ["Training-Free 让开源模型「变强」", "收益约 1–2.6 个百分点，集中在知识型多选题；3B 以下蒸馏模型可能掉分；额外约 15–30% 推理延迟"],
        ["Huginn「3.5B 打出 50B 的表现」", "FLOPs 等效，非基准等效；基准上接近 OLMo-7B、落后 OLMo-2-7B"]]
th = table(pg, "misread", MX, yb, W - 2 * MX, [("常见说法", 0.40, "l"), ("原文事实", 0.60, "l")], rows, fs=13.5, row_h=58)
takeaway(pg, "**方法：**每条都回到原论文的表号核对（Huginn Table 4、LoopCoder-v2 Table 2、Loopie Table 1 与 §2.4、Training-Free Table 2–3）。", yb + th + 18)
footer(pg, "reports/zh 与 survey 附录 A", 18)
pages.append(pg)

# 19 Astra
pg = Page(); yb = title_block(pg, "推断 · 明确标注", "关于 GPT-6 Astra：能核实的与不能核实的")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 440, split=0.36)
card(pg, "unverifiable", x1, y1, w1, h1, "不能核实", ["Astra 用了哪种循环、循环几次、如何训练——OpenAI 发布页无架构细节，The Information 报道基于匿名信源，两份原始材料本报告作者均无法访问。", "以下四条全部是基于公开文献的推断。"], accent="warn", fs=14)
card(pg, "inferences", x2, y2, w2, h2, "四条推断", [
    "1. 若 Astra 用 recurrent depth，公开文献中最接近「前沿规模 + 算力匹配」的配方是 Loopie / SMELT 路线：MoE、中段或逐层、循环次数很小。整模型循环 32 次的 Huginn 路线没有前沿预算下的算力匹配证据。",
    "2. 「OpenAI 绕过了两次饱和」这一推测前提不成立——两次饱和是 PLT 特有；真正的瓶颈是推理成本，而 KV 32× 压缩、扩散式并行采样 5× 已把它压低一个量级。",
    "3. 报道中的「安全担忧」对应文献里的真实问题：潜在推理无可读中间 token，探测结果依赖层与解码方式（Lu 2025、Jacobian Lens 2026），比监督 CoT 更难。",
    "4. Loopie（7 月）、LLA（7 月）、SMELT（9/1）与 Astra（9 月初）密集出现：更合理的解读是多个团队在 2026 上半年同时把这个方向推到可用，而非某篇论文导致某个产品。"], fs=13.5)
footer(pg, "The Information, 2026-09-02（未访问原文）· openai.com/index/gpt-6-astra（无架构细节）", 19)
pages.append(pg)

# 20 open problems
pg = Page(); yb = title_block(pg, "未解问题", "七个还没有公开答案的问题")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 360)
card(pg, "op_left", x1, y1, w1, h1, None, [
    "- **多循环的算力匹配。** 所有算力匹配的胜利都在 R=2；R≥4 能否赢没有公开证据",
    "- **推理成本的完整账。** 训练步时、推理延迟、KV 峰值内存需同时报告；目前没有一篇三者齐全",
    "- **扩展律的函数形式。** SMELT 到 54B、Schwethelm 到 ~1B；Chinchilla + r^φ 项在 100B+ 是否成立未知",
    "- **自适应停机的预训练规模收益。** MoR / TaH / RecurTrace 都在 ≤8B；只有 Ouro 的熵正则深度分配在 7.7T token 验证过"], fs=14)
card(pg, "op_right", x2, y2, w2, h2, None, [
    "- **潜在推理的可监督性。** LOTUS 需要金标 CoT；无 CoT 数据时如何让潜在轨迹可读、可审计，是安全层面的开放问题",
    "- **layer-loop 的机制。** Loopie 三个理由中只有扩展性有实验；SMELT 的「第二次访问削弱注意力沉降」是唯一机制解释",
    "- **循环 vs 序列长度扩展。** Hidden Decoding（WeLM 617B）走序列维度并称更兼容流水线并行；Loopie 的 layer-loop 恰为流水线兼容而设计；100B+ 上无正面对比"], fs=14)
takeaway(pg, "**最值得做的两个空白：**R≥4 的算力匹配扩展律；循环专用的 RL 目标（把 credit 分到潜在轨迹上）。", yb + 376)
footer(pg, "", 20)
pages.append(pg)

# 21 recipes
pg = Page(); yb = title_block(pg, "给从业者", "三种预算下的可执行配方")
for i, (x, y, w, h) in enumerate(cols3(yb, 400)):
    c = [("零训练：已有模型", ["- 中间 4 层窗口，3 级 RK 子步，β 取中间值", "- 稠密 block-mode，MoE layer-mode（先固定路由）", "- 先在知识型多选题上验证；预期 +1–2.6 pp，多 15–30% 延迟", "- 任何「某段层跑两遍」的实验都用阻尼更新 x←(1−1/K)x+(1/K)g(x)"], None),
         ("从头预训练：前沿预算", ["- MoE 骨干，layer-loop，R=2", "- 层数减半 → 激活内存减半 → micro-batch 翻倍 → 用效率增益买宽度；按**实测步时**匹配算力", "- SmallInit / 三明治归一化 / 残差 1/N 缩放；检查 r=1 与 r=max 的困惑度是否分开", "- 后训练：SPT（SFT 掩码 + PT 规模）；RL 用轨迹级 credit（RLTT 类）"], "focus"),
         ("推理时可变算力", ["- 顺序循环（Huginn 类）+ 训练时随机 r + 截断反传，推理任选 r", "- 逐 token 自适应停机（KL 阈值 / 二阶步长差 / 学习式停机头）", "- KV：共享预算或 LLA 低秩编码；延迟：扩散式并行采样", "- 给它检索 / 长上下文——循环模型的强项是对上下文推理"], None)][i]
    card(pg, f"rec{i+1}", x, y, w, h, c[0], c[1], accent=c[2], fs=14)
takeaway(pg, "**部署前必做：**实测延迟与 KV 峰值内存；不要把「训练算力匹配」当作「推理成本匹配」。", yb + 416)
footer(pg, "", 21)
pages.append(pg)

# 22 repo
pg = Page("ending"); yb = title_block(pg, "仓库导航", "awesome_loop_transformer：这份报告的全部材料")
(x1, y1, w1, h1), (x2, y2, w2, h2) = cols2(yb, 400)
card(pg, "dirs", x1, y1, w1, h1, "目录", [
    "- README.md — awesome 列表（14 个主题、333 篇，五篇核心论文加星）",
    "- papers/original/ — 五篇原文 PDF；papers/zh/ — 保版式中译 + QA 报告；papers/src/ — arXiv 全文",
    "- reports/zh | en/ — 五篇逐篇深度解读；reports/pdf/ — 中、英文完整报告 PDF",
    "- survey/zh | en/ — 趋势综述（Markdown + PDF）",
    "- slides/html/ — HTML 演示（含 PDF 导出）；slides/beamer/ — Beamer PDF；slides/pptx/ — 本 PPTX",
    "- data/ — papers.csv、related_abstracts.json；src/generator.py 生成 README"], fs=13.5)
card(pg, "methods", x2, y2, w2, h2, "方法与工具", [
    "- 翻译：SuperTranslate 保版式引擎（DeepSeek 后端）+ 对象级 QA，5 篇中 3 篇 0 issue，2 篇为图内刻度 / 公式行的可解释误报",
    "- 检索：arXiv API，关键词 looped / recurrent-depth / depth-recurrent transformer、latent reasoning ∧ loop，60 篇摘要留档",
    "- 写作：主张先行、必要限定只写一次、数字随处可核对（anti-defensive-writing / 说人话）",
    "- 排版：pandoc + XeLaTeX（报告）、Beamer 16:9（学术幻灯）、HTML 与本 PPTX（ppt-master technical-deepdive 风格，SVG → 原生 DrawingML）"], fs=13.5)
takeaway(pg, "github.com/asimfish/awesome_loop_transformer · 欢迎 PR 补充新论文（data/papers.csv → src/generator.py）", yb + 416)
footer(pg, "首版 2026-09-06 · 2026-11-06 更新", 22)
pages.append(pg)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.svg"): f.unlink()
    for i, pg in enumerate(pages, 1):
        (out / f"page_{i:02d}.svg").write_text(pg.render("zh-CN" if i == 1 else None), encoding="utf-8")
    print(f"wrote {len(pages)} pages to {out}")

if __name__ == "__main__":
    main()
