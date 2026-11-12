import runpy, time
from crew3 import crew
from hotel_tool2 import policy_tool

for agent in crew.agents:
    if agent.tools:
        agent.tools = [policy_tool]
for task in crew.tasks:
    if task.tools:
        task.tools = [policy_tool]

last = [time.perf_counter()]

def on_task_done(output):
    try:
        now = time.perf_counter()
        print(f"  DONE:     {output.agent}  +{now - last[0]:.1f}s", flush=True)
        last[0] = now
    except Exception:
        pass

crew.task_callback = on_task_done
runpy.run_path("ask3.py", run_name="__main__")
