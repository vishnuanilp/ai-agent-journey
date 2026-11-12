from crewai import Task
from researcher import researcher
from responder import responder

find = Task(
    description="Patient asks: {question}\nDocuments:\n{docs}\nCopy the policy lines that answer it.",
    expected_output="The exact policy lines copied word for word, or NOT FOUND",
    agent=researcher)
reply = Task(
    description="Reply to the patient: {question}\nIf the research says NOT FOUND, "
                "say you don't have that information and suggest calling the clinic.",
    expected_output="One or two friendly sentences",
    agent=responder)