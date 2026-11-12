from pathlib import Path

here = Path(__file__).parent
mmd = (here / "vocbook_graph.mmd").read_text(encoding="utf-8").strip()
sweeps = "peek answer_sweep ans_prompts ans_sweep ans_confirm e2e_tools par_prompts par_tools par_sweep cancel_sweep".split()
stale = "agent_prompts agent_shape e2e_prompts e2e_sweep cancel_cases".split()
code = lambda names: ", ".join(f"`{n}.py`" for n in names)
lines = ["# Week 15 - Vocview as a LangGraph state machine", "",
    "Diagram generated from `sat_build/vocbook.py` by `draw_vocbook.py`. Do not hand-edit.", "",
    "```mermaid", mmd, "```", "", "Dotted arrow = router decides. Solid arrow = always taken.",
    "`approve` pauses with `interrupt()` and waits for an exact \"yes\". The diagram cannot show the pause.", "",
    "## sat_build files", "", "- Run: `python askbook.py <thread> \"<message>\"` (graph wired in `vocbook.py`)",
    "- Sweeps, Saturday's measurement record: " + code(sweeps),
    "- STALE, written before Saturday's fixes, do not re-run: " + code(stale)]
(here.parent / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
missing = [n for n in sweeps + stale if not (here / f"{n}.py").exists()]
print("wrote", here.parent.name + "/README.md", "| fences:", sum(l.startswith("```") for l in lines), "| missing:", missing)
