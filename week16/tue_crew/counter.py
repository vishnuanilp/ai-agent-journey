from crewai.events import crewai_event_bus
from crewai.events.types.llm_events import LLMCallCompletedEvent

CALLS = []


@crewai_event_bus.on(LLMCallCompletedEvent)
def count_call(source, event):
    CALLS.append(event.model)