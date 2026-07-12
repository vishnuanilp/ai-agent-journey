import pytest
from unittest.mock import patch, AsyncMock
from router import route

@pytest.mark.asyncio
async def test_route_uses_first_provider():
    with patch("router.call_llm", new=AsyncMock(return_value="fake answer")):
        result = await route("test prompt")
        assert result == "fake answer"

@pytest.mark.asyncio
async def test_route_falls_back_on_failure():
    async def fake_call(prompt, provider):
        if provider == "claude":
            raise Exception("claude is down")
        return f"{provider} answered"

    with patch("router.call_llm", new=fake_call):
        result = await route("test prompt")
        assert result == "openai answered"