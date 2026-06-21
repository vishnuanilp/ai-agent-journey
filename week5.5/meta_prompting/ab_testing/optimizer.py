import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv("../.env")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def make_xml_variant(original_prompt: str) -> str:
    """Wrap the original prompt's body in XML tags."""
    body = original_prompt.strip()
    # Remove the original's input slot — our <input> tag will replace it
    for marker in ["The message to classify is:", "{MESSAGE}"]:
        body = body.replace(marker, "")
    body = body.strip()
    
    wrapped = (
        "<task>\n"
        "Parse the incoming family message into structured JSON.\n"
        "</task>\n\n"
        "<rules>\n"
        f"{body}\n"
        "</rules>\n\n"
        "<input>\n"
        "{MESSAGE}\n"
        "</input>"
    )
    return wrapped



META_INSTRUCTION_COT = """You will be given a prompt that asks a model to classify Telegram messages and return a JSON object.

Your job: rewrite this prompt so it uses CHAIN-OF-THOUGHT reasoning.

Specifically, add a "reasoning_steps" instruction near the top telling the model to think step-by-step BEFORE producing the JSON. The model should:
1. First, internally identify keywords and signals in the message.
2. Second, internally rule out categories that don't fit.
3. Third, output ONLY the final JSON object (no reasoning shown in output).

CRITICAL RULES YOU MUST FOLLOW:
- The OUTPUT SCHEMA must stay EXACTLY the same: same field names (message_type, bill_name, amount, currency, payer), same allowed values, same nullability rules.
- Do NOT add new fields. Do NOT remove fields. Do NOT rename fields.
- The {MESSAGE} placeholder must appear exactly once and must be preserved verbatim.
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.

Here is the original prompt to rewrite:

---ORIGINAL PROMPT START---
{ORIGINAL}
---ORIGINAL PROMPT END---"""


def make_cot_variant(original_prompt: str) -> str:
    """Ask Claude to rewrite the prompt with Chain-of-Thought reasoning."""
    instruction = META_INSTRUCTION_COT.replace("{ORIGINAL}", original_prompt)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        temperature=0,
        messages=[{"role": "user", "content": instruction}]
    )
    return response.content[0].text.strip()


META_INSTRUCTION_FEWSHOT = """You will be given a prompt that asks a model to classify Telegram messages and return a JSON object.

Your job: rewrite this prompt so it uses FEW-SHOT examples.

Specifically:
- Invent 3 realistic example Telegram messages: one bill_announcement, one payment_claim, one ambiguous.
- For each, show the full JSON output that the model should produce.
- Format them as a clear "EXAMPLES:" section placed BEFORE the {MESSAGE} input slot.
- Make the examples concrete (real bill names like "electricity", real amounts like 1450, real names like "amma" or "papa").

CRITICAL RULES YOU MUST FOLLOW:
- The OUTPUT SCHEMA must stay EXACTLY the same: same field names (message_type, bill_name, amount, currency, payer), same allowed values, same nullability rules.
- Do NOT add new fields. Do NOT remove fields. Do NOT rename fields.
- The {MESSAGE} placeholder must appear exactly once and must be preserved verbatim.
- Each example's JSON output must use the same 5 fields as the main schema.
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.

Here is the original prompt to rewrite:

---ORIGINAL PROMPT START---
{ORIGINAL}
---ORIGINAL PROMPT END---"""


def make_fewshot_variant(original_prompt: str) -> str:
    """Ask Claude to rewrite the prompt with 3 worked examples."""
    instruction = META_INSTRUCTION_FEWSHOT.replace("{ORIGINAL}", original_prompt)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        temperature=0,
        messages=[{"role": "user", "content": instruction}]
    )
    return response.content[0].text.strip()

META_INSTRUCTION_ROLE = """You will be given a prompt that asks a model to classify Telegram messages and return a JSON object.

Your job: rewrite this prompt so it uses a ROLE-BASED framing.

Specifically:
- Replace the opening sentence with a specific, high-context role statement. The role should describe the model as an experienced bookkeeper or accountant familiar with Indian family households.
- The role statement should be 2-3 sentences, mentioning years of experience, what they're known for (attention to detail, conservative judgments when unsure), and a sentence about their working style.
- Place this role statement at the very top, before any rules.
- Leave everything else unchanged.

CRITICAL RULES YOU MUST FOLLOW:
- The OUTPUT SCHEMA must stay EXACTLY the same: same field names (message_type, bill_name, amount, currency, payer), same allowed values, same nullability rules.
- Do NOT add new fields. Do NOT remove fields. Do NOT rename fields.
- The {MESSAGE} placeholder must appear exactly once and must be preserved verbatim.
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.

Here is the original prompt to rewrite:

---ORIGINAL PROMPT START---
{ORIGINAL}
---ORIGINAL PROMPT END---"""


def make_role_variant(original_prompt: str) -> str:
    """Ask Claude to rewrite the prompt with an expert role at the top."""
    instruction = META_INSTRUCTION_ROLE.replace("{ORIGINAL}", original_prompt)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        temperature=0,
        messages=[{"role": "user", "content": instruction}]
    )
    return response.content[0].text.strip()

META_INSTRUCTION_META = """You are an expert prompt engineer reviewing a prompt that classifies Telegram messages and returns a JSON object.

Your job: read the prompt below carefully and rewrite it to be more accurate, clearer, and less prone to model error. You decide what to change. You may add structure, examples, reasoning steps, role framing, or anything else you think will help — pick whichever changes you believe matter most.

CRITICAL RULES YOU MUST FOLLOW:
- The OUTPUT SCHEMA must stay EXACTLY the same: same field names (message_type, bill_name, amount, currency, payer), same allowed values, same nullability rules.
- Do NOT add new fields. Do NOT remove fields. Do NOT rename fields.
- The {MESSAGE} placeholder must appear exactly once and must be preserved verbatim.
- The five message_type categories must remain unchanged: bill_announcement, payment_claim, confirm, noise, ambiguous.
- Return ONLY the rewritten prompt. No preamble, no explanation, no markdown fences.

Here is the original prompt to rewrite:

---ORIGINAL PROMPT START---
{ORIGINAL}
---ORIGINAL PROMPT END---"""


def make_meta_variant(original_prompt: str) -> str:
    """Ask Claude to rewrite the prompt however it sees fit."""
    instruction = META_INSTRUCTION_META.replace("{ORIGINAL}", original_prompt)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        temperature=0,
        messages=[{"role": "user", "content": instruction}]
    )
    return response.content[0].text.strip()

