# Vocview Backend — Phase 1

The brain of Vocview: a multi-provider AI backend that never turns a request away.

## Architecture

**adapter.py** — one function, `call_llm(prompt, provider)`.
Talks to three AI providers, each with a different response shape,
and always returns plain text:

| Provider | Model             | Unwrap shape                          |
|----------|-------------------|---------------------------------------|
| claude   | claude-sonnet-4-6 | response.content[0].text              |
| openai   | gpt-4o-mini       | response.choices[0].message.content   |
| gemini   | gemini-2.5-flash  | response.text                         |

**router.py** — the routing brain, `route(prompt)`.
Tries the best model first; if it fails, falls to the next down the ladder:

    claude → openai → gemini

If every provider fails, it raises loudly. Nobody is turned away
unless the whole ladder is down.

## Run

    python router.py