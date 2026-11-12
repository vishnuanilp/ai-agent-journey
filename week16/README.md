# Week 16 — CrewAI multi-agent team inside Vocview's LangGraph

Vocview answers hotel guests. Week 15 built the graph (the front desk: routing, memory, pausing).
Week 16 built a three-agent CrewAI team and put it inside one box of that graph.
Final code: `week16/fri_crew/vocbook2.py` (Friday + Saturday).

## The flow

## Agent roles — the crew (one box: `crew`)

| Role | Job | Tools | Rule that matters |
|---|---|---|---|
| Researcher | Fetch the hotel policy text | `search_hotel_policy` only | Copy the text ABOUT the topic, even if it says no. NOT FOUND only if nothing is about the topic. Fetch, never judge. |
| Analyst | Decide YES / NO / UNKNOWN | none | Reply as VERDICT, REASON, LINE USED. |
| Writer | Speak to the guest | none | Two or three plain sentences, uses only the Analyst's verdict. |

Process: sequential. Delegation: off. Model: gpt-4o-mini, temperature 0, max_iter 3.

## Graph boxes around the crew

| Box | Job | Model calls |
|---|---|---|
| classify | question / action / chitchat — sees up to 3 earlier guest messages | 1 |
| extract | pulls day / nights / guests from a booking message | 1 |
| ask | asks for the missing booking detail | 0 |
| approve | PAUSES for the guest's yes — kept OUTSIDE the crew | 0 |
| book / cancel | confirms or drops the booking | 0 |
| chat | fixed reply: "Happy to help! What would you like to know about your stay?" | 0 |
| remember | saves the conversation | 0 |

## Measured

Cost per question, counted at the wire (counter2.py, every OpenAI request):

| Path | chat | input_tokens | embeddings |
|---|---|---|---|
| crew alone | 4 | 5 | 1 |
| question through vocbook2 | 5 (crew 4 + classify 1) | 5 | 1 |
| booking turn (pauses) | 2 (classify + extract) | 0 | 0 |
| "yes" turn (resumes, books) | 0 | 0 | 0 |
| chitchat | 1 (classify) | 0 | 0 |

Scores: 4 control questions 4/4 · hard questions (15kg dog, pool, 5kg dog + bed) 6/6 after the Researcher fix ·
full conversation (hello, 15kg dog, book, yes, cats) all right after the classify fix.

## What each day found

| Day | Finding |
|---|---|
| Mon | A two-agent crew (Researcher + Writer) inside Vocview. |
| Tue | Split deciding (Analyst) from speaking (Writer): crew3, 4/4 at 16 calls. |
| Wed | Tried a hierarchical manager; it did the Writer's job and made false claims. Kept sequential. |
| Thu | The model reads only a tool's label (name + inputs + description). The task callback shows progress at 0 calls. |
| Fri | Crew inside a graph node costs 0 extra calls. In vocbook2 it replaces research + respond. |
| Sat | The 15kg failure was the Researcher judging instead of fetching; one rule fixed it. classify needed more than 1 earlier message. |

## Rules learned

- Put the pause in its own box. LangGraph re-runs a paused box from its start; a crew in that box would be paid for twice.
- Put plain text (`.raw`) into graph state, not the CrewOutput object.
- Count calls at the wire, not with CrewAI's event bus: the bus cannot see Week 15's own calls.
- Give each agent one job. A Researcher that judges drops answers it should pass on.
- Run a control before naming a cause.

## How to run

Venv: crewai 1.15.33 · openai 2.54.0 · langgraph 1.2.12 · langgraph-checkpoint-sqlite 3.1.2.

## Known limits

- Every test ran once; reply wording drifts between runs at temperature 0.
- input_tokens shows one more request than chat calls; pattern so far is 4 + one per search. Cause not proven.
- Hotel only. Not yet tested on another business.
