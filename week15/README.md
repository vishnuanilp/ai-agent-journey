# Week 15 - Vocview as a LangGraph state machine

Diagram generated from `sat_build/vocbook.py` by `draw_vocbook.py`. Do not hand-edit.

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	classify(classify)
	research(research)
	respond(respond)
	extract(extract)
	ask(ask)
	approve(approve)
	book(book)
	cancel(cancel)
	chat(chat)
	error_box(error_box)
	remember(remember)
	__end__([<p>__end__</p>]):::last
	__start__ -.-> classify;
	__start__ -.-> extract;
	approve -.-> book;
	approve -.-> cancel;
	ask --> remember;
	book --> remember;
	cancel --> remember;
	chat --> remember;
	classify -. &nbsp;chitchat&nbsp; .-> chat;
	classify -. &nbsp;error&nbsp; .-> error_box;
	classify -. &nbsp;action&nbsp; .-> extract;
	classify -. &nbsp;question&nbsp; .-> research;
	error_box --> remember;
	extract -.-> approve;
	extract -.-> ask;
	extract -.-> cancel;
	extract -.-> classify;
	research --> respond;
	respond --> remember;
	remember --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

Dotted arrow = router decides. Solid arrow = always taken.
`approve` pauses with `interrupt()` and waits for an exact "yes". The diagram cannot show the pause.

## sat_build files

- Run: `python askbook.py <thread> "<message>"` (graph wired in `vocbook.py`)
- Sweeps, Saturday's measurement record: `peek.py`, `answer_sweep.py`, `ans_prompts.py`, `ans_sweep.py`, `ans_confirm.py`, `e2e_tools.py`, `par_prompts.py`, `par_tools.py`, `par_sweep.py`, `cancel_sweep.py`
- STALE, written before Saturday's fixes, do not re-run: `agent_prompts.py`, `agent_shape.py`, `e2e_prompts.py`, `e2e_sweep.py`, `cancel_cases.py`
