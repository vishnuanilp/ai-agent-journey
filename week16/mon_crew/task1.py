from crewai import Task
from researcher import researcher
from clinic_docs import DOCS
from counter import CALLS

find = Task(
    description="Patient asks: {question}\nCopy the policy lines that answer it.",
    expected_output="The exact policy lines copied word for word, or NOT FOUND",
    agent=researcher)
for q in ["Can I bring my child?", "Do you do teeth whitening?"]:
    find.interpolate_inputs_and_add_conversation_history({"question": q})
    out = find.execute_sync(context=DOCS)
    print("Q:", q, "| OUT:", out.raw)
print("CALLS:", len(CALLS))