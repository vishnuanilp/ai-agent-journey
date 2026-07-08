from unittest.mock import patch
from llm_helper import call_llm

def test_call_llm_wraps_the_answer():
    with patch("llm_helper.expensive_claude_call") as fake_call:
        fake_call.return_value = "hello there"
        result = call_llm("any prompt")
        assert result == "Claude says: hello there"
