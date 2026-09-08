#!/usr/bin/env python3
"""Hand-authored explanatory diagrams (SVG) for the reports and survey; PNGs are rendered with
headless Chromium by scripts/render_diagrams.sh. Light theme so they read well on GitHub and in PDF."""
import pathlib
from xml.sax.saxutils import escape as _esc
OUT = pathlib.Path(__file__).resolve().parents[1] / "assets/figures/diagrams"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, BLUE, ORANGE, GREEN, GRAY, BG = "#1F2A37", "#6B7280", "#0173B2", "#DE8F05", "#029E73", "#CBD5E1", "#FFFFFF"
FONT = "PingFang SC, Microsoft YaHei, Helvetica Neue, Arial, sans-serif"

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" font-size="14" fill="{INK}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>'
            '<defs><marker id="a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
            f'<path d="M0,0 L9,4.5 L0,9 z" fill="{MUTED}"/></marker>'
            '<marker id="ab" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
            f'<path d="M0,0 L9,4.5 L0,9 z" fill="{BLUE}"/></marker>'
            '<marker id="ao" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
            f'<path d="M0,0 L9,4.5 L0,9 z" fill="{ORANGE}"/></marker></defs>' + body + '</svg>')

BOLD = ' font-weight="bold"'

def box(x, y, w, h, label, fill="#F1F5F9", stroke=GRAY, color=INK, fs=14, bold=False, rx=8, sub=None):
    bw = BOLD if bold else ""
    ty = y + h / 2 + (0 if sub is None else -6) + 5
    t = f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="{fs}" fill="{color}"{bw}>{_esc(label)}</text>'
    if sub: t += f'<text x="{x+w/2}" y="{y+h/2+13}" text-anchor="middle" font-size="11" fill="{MUTED}">{_esc(sub)}</text>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>' + t

def arrow(x1, y1, x2, y2, color=MUTED, marker="a", dash=None, w=1.6):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" marker-end="url(#{marker})"{d}/>'

def text(x, y, s, fs=13, color=INK, anchor="start", bold=False):
    bw = BOLD if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{fs}" fill="{color}" text-anchor="{anchor}"{bw}>{_esc(s)}</text>'

def title(s, sub=None, w=900):
    out = text(24, 30, s, 17, INK, bold=True)
    if sub: out += text(24, 50, sub, 12, MUTED)
    return out

# 1. loop granularity ------------------------------------------------------------
def d_granularity():
    b = title("三种循环粒度：同一组参数如何被重复使用", "model-loop 整栈循环 · block-loop 只循环中段 · layer-loop 每层各自循环")
    rows = [("model-loop（整模型循环）", "UT 2018 · Huginn 核心块 · Ouro", ["L1", "L2", "L3", "L1", "L2", "L3"], [BLUE]*6, "整栈输出再喂回：L1→L2→L3→L1→L2→L3"),
            ("block-loop（块循环）", "Huginn 三段式 · Hyperloop · Training-Free · SMELT", ["首层", "中段", "中段", "中段", "尾层"], [GRAY, BLUE, BLUE, BLUE, GRAY], "首尾层只走一次，中段重复；每步重新注入输入 e"),
            ("layer-loop（逐层循环）", "Loopie · Training-Free layer-mode · MixerLoop", ["L1", "L1", "L2", "L2", "L3", "L3"], [BLUE, "#7FB3D5", GREEN, "#7FD1B9", ORANGE, "#F0BC6A"], "每层先自己重复两次再下传：L1→L1→L2→L2→L3→L3")]
    y = 72
    for name, who, cells, cols, note in rows:
        b += text(24, y + 18, name, 14, INK, bold=True) + text(24, y + 36, who, 11, MUTED)
        x = 330
        for c, col in zip(cells, cols):
            b += box(x, y, 64, 34, c, fill=col, stroke=col, color="#FFFFFF" if col not in (GRAY,) else INK, fs=13, rx=6)
            x += 74
        b += text(330, y + 56, note, 12, MUTED)
        y += 90
    b += text(24, y + 8, "共同点：有效深度 = 存储层数 × 循环次数，参数量不变。三条独立证据都指向「循环中段、避开首尾层」（相对深度约 0.5）。", 12, INK)
    return svg(900, y + 24, b)

# 2. Huginn -----------------------------------------------------------------------
def d_huginn():
    b = title("Huginn-3.5B 的三段式循环深度（Geiping et al. 2025）", "Prelude 嵌入 → Core 重复 r 次（每步重新注入 e）→ Coda 解码；训练时 r 随机，只对最后 8 步反传")
    y = 80
    b += box(40, y, 130, 56, "输入 token x", fill="#F8FAFC")
    b += arrow(170, y + 28, 210, y + 28)
    b += box(212, y, 150, 56, "Prelude P", fill="#E0ECF7", stroke=BLUE, bold=True, sub="2 层 · 嵌入 e")
    b += arrow(362, y + 28, 402, y + 28)
    b += f'<rect x="404" y="{y-22}" width="230" height="100" rx="10" fill="#E6F4EE" stroke="{GREEN}" stroke-width="1.5"/>'
    b += box(424, y, 190, 56, "Core R", fill="#FFFFFF", stroke=GREEN, bold=True, sub="4 层 · sᵢ = R(e, sᵢ₋₁)")
    b += text(519, y - 8, "× r（训练时随机，均值 32；测试时任选）", 11, GREEN, anchor="middle", bold=True)
    b += f'<path d="M614,{y+8} C660,{y-30} 380,{y-30} 424,{y+8}" fill="none" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#a)"/>'
    b += arrow(287, y + 56, 287, y + 100, BLUE, "ab") + f'<path d="M287,{y+100} L424,{y+100} L424,{y+56}" fill="none" stroke="{BLUE}" stroke-width="1.6" marker-end="url(#ab)"/>'
    b += text(300, y + 116, "每一步都重新注入 e（输入注入）", 11, BLUE)
    b += arrow(634, y + 28, 674, y + 28)
    b += box(676, y, 150, 56, "Coda C", fill="#FBE9E7", stroke="#C0392B", bold=True, sub="2 层 · 解码到词表")
    b += text(40, y + 150, "s₀ 是随机噪声；有效深度 2 + 4r + 2，r = 32 时 132 层，但参数只有 3.5B。", 12, INK)
    b += text(40, y + 170, "训练：r ~ 对数正态泊松（重尾）；只对最后 k = 8 步反向传播 → 显存与 r 无关。三明治归一化 + 小学习率避免两种坍缩。", 12, INK)
    # mini bar chart ARC-E
    bx, by = 40, y + 200
    b += text(bx, by, "测试时多循环 = 多算力：ARC-E 随 r 上升（Table 1）", 12, INK, bold=True)
    vals = [(4, 49.07), (8, 65.11), (16, 69.49), (32, 69.91)]
    for i, (r, v) in enumerate(vals):
        w = (v - 40) * 14
        barc = BLUE if i == 3 else "#93C5FD"
        b += f'<rect x="{bx+60}" y="{by+12+i*22}" width="{w}" height="14" fill="{barc}"/>'
        b += text(bx, by + 24 + i * 22, f"r={r}", 11, MUTED) + text(bx + 66 + w, by + 24 + i * 22, f"{v}", 11, INK)
    b += text(560, by + 30, "公平对照要看同为 0.18T token 的 Table 4：", 12, ORANGE, bold=True)
    b += text(560, by + 50, "ARC-E 46.42 → 53.62，GSM8K CoT 2.20 → 10.24。", 12, INK)
    b += text(560, by + 70, "「0.8T 循环模型 vs 0.18T 基线」的对比夸大了差距。", 12, MUTED)
    return svg(900, by + 110, b)

# 3. Training-free ODE ---------------------------------------------------------------
def d_ode():
    b = title("Training-Free 的关键洞察：一层 = ODE 的一步欧拉，循环应细分步长而不是走到 t = K",
              "pre-norm 层 L(x) = x + F(x) 就是 ẋ = F(x) 上步长 h = 1 的一步；后面的层只见过 t = 1 处的状态")
    y0 = 170
    # axis
    b += arrow(60, y0, 840, y0) + text(845, y0 + 4, "t", 13, MUTED)
    for t, lab in [(0, "t=0"), (1, "t=1"), (2, "t=2"), (3, "t=3")]:
        x = 60 + 120 + t * 200
        b += f'<line x1="{x}" y1="{y0-6}" x2="{x}" y2="{y0+6}" stroke="{MUTED}"/>' + text(x, y0 + 22, lab, 12, MUTED, "middle")
    xs = lambda t: 180 + t * 200
    # trained region
    b += f'<rect x="{xs(1)-28}" y="{y0-72}" width="56" height="66" rx="8" fill="#E6F4EE" stroke="{GREEN}" stroke-dasharray="4 3"/>'
    b += text(xs(1), y0 + 40, "后段层训练时只见过 t=1 附近的状态", 11, GREEN, "middle")
    # naive loop: big steps to t=3
    yn = y0 - 48
    for t in range(3):
        b += arrow(xs(t) + 6, yn, xs(t + 1) - 8, yn, ORANGE, "ao", w=2)
        b += f'<circle cx="{xs(t)}" cy="{yn}" r="5" fill="{ORANGE}"/>'
    b += f'<circle cx="{xs(3)}" cy="{yn}" r="5" fill="{ORANGE}"/>'
    b += text(xs(2), yn - 14, "朴素循环 K=3：三大步走到 t=3，后段层没见过 → 掉点", 12, ORANGE, "middle", bold=True)
    # substep: 3 small steps within [0,1]
    ys = y0 - 14
    for k in range(3):
        xa = xs(0) + k * 200 / 3; xb = xs(0) + (k + 1) * 200 / 3
        b += arrow(xa + 5, ys, xb - 7, ys, BLUE, "ab", w=2)
        b += f'<circle cx="{xa}" cy="{ys}" r="4" fill="{BLUE}"/>'
    b += f'<circle cx="{xs(1)}" cy="{ys}" r="5" fill="{BLUE}"/>'
    b += text(xs(0.5), ys + 22, "子步 K=3：三小步走到同一个 t=1，逼近更准", 12, BLUE, "middle", bold=True)
    b += text(60, y0 + 70, "阻尼欧拉：x ← (1 − 1/K)·x + (1/K)·g(x)，以 O(1/K) 逼近 x(t=1)；加锚点 β：输出 = β·g(x₀) + (1−β)·F^K(x₀)。", 12, INK)
    b += text(60, y0 + 90, "2 维小网络：K=8 时朴素循环 MSE 335，子步 1.04。真实模型：中间 4 层、3 级 RK，45 个格子 87% 非负，MMLU-Pro 最多 +2.64。", 12, INK)
    b += text(60, y0 + 110, "配方边界：窗口 n=4 是甜点，n≥6 悬崖，循环整模型 −27.7；MoE 必须 layer-mode（否则路由抖动）。", 12, MUTED)
    return svg(900, y0 + 130, b)

# 4. PLT gain-cost -----------------------------------------------------------------
def d_plt():
    b = title("LoopCoder-v2：并行循环 Transformer 为什么在第 2 次循环就饱和", "左：PLT 把上一轮状态右移一位后并行执行；右：收益递减、位置税不变 → R=2 达峰")
    # left: sequential vs PLT
    x0, y0 = 40, 78
    b += text(x0, y0, "顺序循环", 13, INK, bold=True) + text(x0 + 90, y0, "R 次串行，延迟与 KV 都 ×R", 11, MUTED)
    for r in range(3):
        b += box(x0 + r * 92, y0 + 10, 84, 30, f"第 {r+1} 轮", fill="#F1F5F9", fs=12, rx=5)
        if r < 2: b += arrow(x0 + r * 92 + 84, y0 + 25, x0 + (r + 1) * 92, y0 + 25)
    b += text(x0, y0 + 70, "PLT（跨循环位置偏移 CLP）", 13, INK, bold=True) + text(x0 + 200, y0 + 70, "一次前向内并行，延迟 ≈ 单次", 11, MUTED)
    toks = ["x₁", "x₂", "x₃", "x₄"]
    for i, t in enumerate(toks):
        b += box(x0 + i * 62, y0 + 82, 54, 26, f"{t} 轮1", fill="#E0ECF7", stroke=BLUE, fs=11, rx=4)
        if i >= 1: b += box(x0 + i * 62, y0 + 114, 54, 26, f"{t} 轮2", fill="#E6F4EE", stroke=GREEN, fs=11, rx=4)
        if i >= 1: b += arrow(x0 + (i - 1) * 62 + 27, y0 + 108, x0 + i * 62 + 22, y0 + 116, GREEN, "a", w=1.4)
    b += text(x0, y0 + 160, "第 2 轮的 xᵢ 拿到的是邻居 xᵢ₋₁ 的第 1 轮状态：位置错配，", 11, ORANGE)
    b += text(x0, y0 + 176, "这是标准循环没有、PLT 每轮都要交的固定「位置税」Ω。", 11, ORANGE)
    # right: scissors chart
    cx, cy, cw, ch = 520, 78, 340, 150
    b += f'<line x1="{cx}" y1="{cy+ch}" x2="{cx+cw}" y2="{cy+ch}" stroke="{MUTED}"/><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+ch}" stroke="{MUTED}"/>'
    for i, lab in enumerate(["R=2", "R=3", "R=4"]):
        b += text(cx + 60 + i * 110, cy + ch + 16, lab, 12, MUTED, "middle")
    gain = [(60, 30), (170, 95), (280, 80)]   # conceptual: Δp 1.75, 1.32, 1.58 (readout) -> show diminishing "productive" gain
    pts = " ".join(f"{cx+x},{cy+y}" for x, y in [(60, 30), (170, 110), (280, 125)])
    b += f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
    for x, y in [(60, 30), (170, 110), (280, 125)]: b += f'<circle cx="{cx+x}" cy="{cy+y}" r="4" fill="{BLUE}"/>'
    b += f'<line x1="{cx+40}" y1="{cy+60}" x2="{cx+300}" y2="{cy+58}" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += text(cx + 200, cy + 50, "偏移成本 Ω ≈ 常数（固定位置税）", 11, ORANGE)
    b += text(cx + 64, cy + 22, "有效精化收益", 11, BLUE)
    b += text(cx, cy - 8, "每多一次循环：收益 vs 成本（示意，非实测曲线）", 12, INK, bold=True)
    b += text(cx, cy + ch + 40, "实测：有效秩 174.6 → 172.5 → 158.2；更新方向震荡（cos θ<0）；", 11, INK)
    b += text(cx, cy + ch + 56, "第 3 轮起 Ω 是边际收益的 30–45 倍。", 11, INK)
    b += text(cx, cy + ch + 72, "SWE-bench Verified：43.0 → 64.4 → 27.6 → 22.4。", 11, INK)
    b += text(40, 310, "边界：非单调是 PLT 特有；顺序循环的 Huginn 到 r=32 单调上升。", 12, MUTED)
    b += text(40, 328, "R=2 上叠加显式 CoT 是超加的（LiveCodeBench +26.9）。", 12, MUTED)
    return svg(900, 346, b)

# 5. Loopie recipe ---------------------------------------------------------------------
def d_loopie():
    b = title("Loopie Recipe：把循环省下的显存换成宽度，再按实测步时匹配算力", "Loop the Loopies!（2026-07）：layer-loop · 两次循环 · MoE 骨干")
    y = 80
    steps = [("参考模型", "Qwen3-like 30B-A3B", "D=2048 · L=48 · R=1", "#F1F5F9", GRAY),
             ("① 层数减半、循环两次", "种子 Loopie", "D=2048 · L=24 · R=2\n块执行次数不变，激活内存 ×0.5", "#E0ECF7", BLUE),
             ("② 显存换吞吐", "每卡 micro-batch ×2", "梯度累积 ÷2，每步 token 不变\n实测每步更快", "#E6F4EE", GREEN),
             ("③ 再投资到容量", "Loopie-20B-A2B", "D=2304 · L=27 · R=2\n名义算力 1.42×，步时 ≈ 参考", "#FDF1E1", ORANGE)]
    x = 24
    for i, (h, name, desc, fill, stroke) in enumerate(steps):
        b += f'<rect x="{x}" y="{y}" width="200" height="120" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
        b += text(x + 12, y + 22, h, 12, stroke, bold=True) + text(x + 12, y + 44, name, 14, INK, bold=True)
        for j, line in enumerate(desc.split("\n")):
            b += text(x + 12, y + 68 + j * 18, line, 11, MUTED)
        if i < 3: b += arrow(x + 200, y + 60, x + 216, y + 60)
        x += 218
    y2 = y + 150
    b += text(24, y2, "为什么是 layer-loop：", 13, INK, bold=True)
    order = [("L1", BLUE), ("L1", "#7FB3D5"), ("L2", GREEN), ("L2", "#7FD1B9"), ("L3", ORANGE), ("L3", "#F0BC6A")]
    for i, (c, col) in enumerate(order):
        b += box(190 + i * 54, y2 - 18, 46, 28, c, fill=col, stroke=col, color="#FFFFFF", fs=12, rx=5)
    b += text(520, y2 - 6, "每层的所有循环都在同一流水线 stage 内完成；", 11, MUTED)
    b += text(520, y2 + 10, "6B 模型上约 1.2T token 后反超 model-loop。", 11, MUTED)
    b += text(24, y2 + 34, "结果：与参考模型同预算训练 800B token，约 600B 后反超并保持；4 级扩展梯全胜。20B-A2B Thinking：MMLU 81.28、AIME24 92.09（3.5T token）。", 12, INK)
    b += text(24, y2 + 54, "口径：匹配的是实测优化器步时，不是 FLOPs（名义高 42%）；推理时每 token 54 次块计算 vs 48，推理延迟未报告。", 12, ORANGE)
    return svg(900, y2 + 76, b)

# 6. UT with ACT -----------------------------------------------------------------------
def d_ut():
    b = title("Universal Transformer（2018）：同一个块在时间步上重复，每个位置自己决定停在哪一步", "每步 = 自注意力（跨位置交换信息）+ 位置无关的转移函数；ACT 让不同 token 有不同的「思考深度」")
    y0 = 80
    T = 5
    for t in range(T):
        b += text(120 + t * 130, y0 - 8, f"t={t+1}", 12, MUTED, "middle")
    labels = ["The", "keys", "to", "the", "cabinet", "are"]
    halts = [2, 4, 1, 2, 5, 3]
    for i, (lab, hstep) in enumerate(zip(labels, halts)):
        y = y0 + 10 + i * 32
        b += text(50, y + 16, lab, 12, INK, "end")
        for t in range(T):
            x = 120 + t * 130 - 45
            active = t < hstep
            fillc = "#E0ECF7" if active else "#F8FAFC"; strokec = BLUE if active else GRAY; dash = "" if active else "3 3"
            b += f'<rect x="{x}" y="{y}" width="90" height="22" rx="5" fill="{fillc}" stroke="{strokec}" stroke-dasharray="{dash}"/>'
            if active: b += text(x + 45, y + 15, "共享块", 10, BLUE, "middle")
            elif t == hstep: b += text(x + 45, y + 15, "已停机（复制状态）", 9, MUTED, "middle")
    b += text(120 + 5 * 130 - 40, y0 + 110, "→ 输出", 12, INK)
    yb = y0 + 10 + 6 * 32 + 16
    b += text(50, yb, "同一列内所有位置通过自注意力互相看见上一时刻的状态（RNN 做不到这一点）；参数跨 t 共享，加坐标嵌入 P^t 告知当前步数。", 12, INK)
    b += text(50, yb + 20, "ACT 实证：需要 1 / 2 / 3 条支撑事实的问题平均想 2.3 / 3.1 / 3.8 步。bAbI 联合训练错误率 22.1 → 0.29；LAMBADA 困惑度 7321 → 142。", 12, INK)
    b += text(50, yb + 40, "留下三个问题：参数—计算比（翻译只 +0.9 BLEU）、训练不稳定、推理成本——正是之后八年的研究议程。", 12, MUTED)
    return svg(900, yb + 60, b)

# 7. two regimes -----------------------------------------------------------------------
def d_regimes():
    b = title("「循环几次」分裂成两个 regime：取决于算力约束在哪里", "洞察 2：预训练预算固定 → 2 次；推理算力可变 → 越多越好、但要自适应")
    y = 80
    b += f'<rect x="24" y="{y}" width="410" height="200" rx="12" fill="#E0ECF7" stroke="{BLUE}" stroke-width="1.5"/>'
    b += text(44, y + 28, "预训练算力受限（前沿模型训练）", 14, BLUE, bold=True)
    for i, s in enumerate(["每多一次循环 = 训练 FLOPs 乘一个系数", "边际收益在 R=2 后衰减最快（Loopie Fig. 6）", "Loopie 2 · LoopCoder-v2 2 · SMELT 2 · Nanbeige4.2 2", "答案：R = 2，用省下的显存买宽度"]):
        b += text(44, y + 58 + i * 26, ("• " if i < 3 else "→ ") + s, 12, INK if i < 3 else BLUE, bold=(i == 3))
    b += f'<rect x="466" y="{y}" width="410" height="200" rx="12" fill="#E6F4EE" stroke="{GREEN}" stroke-width="1.5"/>'
    b += text(486, y + 28, "推理算力可变（同一个模型、按题分配）", 14, GREEN, bold=True)
    for i, s in enumerate(["Huginn：ARC-C 零样本 8 次饱和，25–50 shot 需 32 次", "Ouro 4 · Huginn 32–64 · RecurTrace 平均 2.0 · TaH 93% token 只 1 次", "自适应停机：KL 阈值 / 步长二阶差 / 学习式停机头", "答案：按需、自适应，越难想越久"]):
        b += text(486, y + 58 + i * 26, ("• " if i < 3 else "→ ") + s, 12, INK if i < 3 else GREEN, bold=(i == 3))
    b += text(24, y + 230, "常见误读：「循环两次就够，三次以上回退」——那是并行循环（PLT）的位置税，不是循环深度的普适上限；顺序循环的 Huginn 到 r=32 单调上升。", 12, ORANGE)
    return svg(900, y + 250, b)

for name, fn in [("loop_granularity", d_granularity), ("huginn_architecture", d_huginn), ("training_free_ode", d_ode),
                 ("plt_gain_cost", d_plt), ("loopie_recipe", d_loopie), ("ut_act", d_ut), ("two_regimes", d_regimes)]:
    (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("wrote", name)
