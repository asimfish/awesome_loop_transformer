"""Create English conceptual figures used by the English reports."""
from pathlib import Path
from html import escape as e
import re

ROOT = Path(__file__).resolve().parents[1]
FIGURES = {
    "ut_act": (
        "Shared computation, different stopping times",
        "Universal Transformers",
        ("A shared transformation", ["Apply the same attention and transition block.", "Position and step encodings distinguish each update.", "All token states can update in parallel."]),
        ("Adaptive computation time", ["Each token accumulates a halting probability.", "A halted token keeps its state while others continue.", "A step limit bounds the amount of computation."]),
        ("Token states", "Shared block", "Halting decision"),
        "The diagram describes the mechanism, not measured runtime or performance."
    ),
    "huginn_architecture": (
        "Allocate more computation in latent space",
        "Recurrent-depth pretraining",
        ("Prelude and recurrent core", ["Encode the input before recurrent processing.", "Reuse the core parameters across depth steps.", "Carry the hidden state from one step to the next."]),
        ("Coda and readout", ["Read out the recurrent state to predict tokens.", "Choose the inference loop budget independently.", "Compare accuracy, latency, and memory together."]),
        ("Prelude", "Recurrent core", "Coda"),
        "More recurrence adds computation without adding a new parameter set at every step."
    ),
    "training_free_ode": (
        "Repeat the computation; preserve the path",
        "Training-free looping",
        ("View depth as a flow", ["Treat a pretrained stack as a sequence of updates.", "Choose an intermediate segment to revisit.", "Interpret each residual update as a step."]),
        ("Refine the step size", ["Subdivide updates when introducing extra loops.", "Control the accumulated change in hidden state.", "Evaluate the retrofit without retraining weights."]),
        ("Hidden state", "Smaller updates", "Readout"),
        "Substepping aims to preserve the original flow; arbitrary repeated full steps can change it."
    ),
    "plt_gain_cost": (
        "Compare gains with the cost of the loop",
        "LoopCoder-v2",
        ("Parallel loop design", ["Use a parallel loop transformer for coding.", "Track how positional structure changes with looping.", "Keep the loop layout explicit in comparisons."]),
        ("Evaluate the trade-off", ["Compare task accuracy at the chosen loop count.", "Measure latency and cache use separately.", "Check how latent loops interact with explicit reasoning."]),
        ("Input tokens", "Parallel looping", "Coding output"),
        "Results for a specific parallel loop layout do not define a universal recurrence limit."
    ),
    "loopie_recipe": (
        "Reuse depth within a matched training budget",
        "Loop the Loopies",
        ("Architectural choices", ["Study mixture-of-experts transformer blocks.", "Compare layer, block, and model reuse.", "Track where the repeated computation occurs."]),
        ("Budget comparison", ["Match the training resource being measured.", "Account for activation memory and model width.", "Report inference costs as a separate comparison."]),
        ("Choose layout", "Train with reuse", "Match budgets"),
        "Weight sharing changes the allocation of parameters and computation; it does not make work free."
    ),
    "loop_granularity": (
        "Choose the part of the network that repeats",
        "A map of loop granularity",
        ("Where parameters are shared", ["Model loop: repeat the transformer stack.", "Block loop: repeat a contiguous segment.", "Layer loop: revisit a layer before advancing."]),
        ("How repeated work is scheduled", ["Sequential recurrence carries state between steps.", "Parallel-loop designs use a different arrangement.", "Keep scheduling separate from the size of the block."]),
        ("Input / prelude", "Repeated region", "Output / coda"),
        "Describe both the repeated region and its execution schedule when comparing architectures."
    ),
    "two_regimes": (
        "Two budgets, two different questions",
        "Pretraining and inference",
        ("Fixed training budget", ["Allocate compute between depth, width, and data.", "Compare models under a matched training budget.", "An economical loop count depends on the setup."]),
        ("Variable inference budget", ["Allocate extra steps to the same trained model.", "Check stopping rules and task difficulty.", "Measure the marginal gain from additional steps."]),
        ("Training budget", "Shared parameters", "Inference budget"),
        "A loop count that works well during budget-matched training need not be the best inference limit."
    ),
}

def svg(key, spec):
    title, subtitle, left, right, flow, footer = spec
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="480" viewBox="0 0 1100 480" role="img" aria-labelledby="title desc">
<title id="title">{e(title)}</title><desc id="desc">{e(subtitle + ". " + footer)}</desc>
<rect width="1100" height="480" rx="12" fill="#f8f7f2"/>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#17675d"/></marker></defs>
<g font-family="Verdana, sans-serif"><text x="38" y="38" font-size="12" letter-spacing="2" fill="#536b72">{e(subtitle.upper())}</text>
<text x="38" y="80" font-size="29" fill="#182c33">{e(title)}</text>''']
    for x,panel in [(38,left),(570,right)]:
        parts.append(f'<rect x="{x}" y="110" width="492" height="185" rx="8" fill="#fffefa" stroke="#ced9d3"/>')
        parts.append(f'<text x="{x+22}" y="147" font-size="20" fill="#17675d">{e(panel[0])}</text>')
        for i,line in enumerate(panel[1]):
            parts.append(f'<circle cx="{x+25}" cy="{180+i*34}" r="3" fill="#17675d"/><text x="{x+40}" y="{185+i*34}" font-size="15" fill="#435960">{e(line)}</text>')
    for i,label in enumerate(flow):
        x=70+i*340
        parts.append(f'<rect x="{x}" y="332" width="280" height="65" rx="6" fill="{"#17675d" if i==1 else "#e7eee8"}"/><text x="{x+140}" y="372" text-anchor="middle" font-size="18" fill="{"#ffffff" if i==1 else "#182c33"}">{e(label)}</text>')
        if i<2:
            parts.append(f'<path d="M{x+288} 364H{x+330}" stroke="#17675d" stroke-width="2" marker-end="url(#a)"/>')
    parts.append(f'<text x="38" y="447" font-size="13" fill="#536b72">{e(footer)}</text></g></svg>\n')
    return "".join(parts)

def main():
    target=ROOT/"assets/figures/en"
    target.mkdir(parents=True,exist_ok=True)
    for key,spec in FIGURES.items():
        (target/(key+".svg")).write_text(svg(key,spec),encoding="utf-8")
    print("Built 7 English vector figures.")

if __name__ == "__main__":
    main()
