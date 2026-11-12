from crewai import Crew
from researcher import researcher
from responder import responder
from tasks import find, reply
from clinic_docs import DOCS
from counter import CALLS

crew = Crew(agents=[researcher, responder], tasks=[find, reply], verbose=False)
for q in ["Can I bring my child?", "Do you do teeth whitening?", "Can I pay by cheque?"]:
    out = crew.kickoff(inputs={"question": q, "docs": DOCS})
    print("Q:", q)
    print("  RESEARCH:", out.tasks_output[0].raw)
    print("  REPLY:   ", out.raw)
print("CALLS:", len(CALLS))