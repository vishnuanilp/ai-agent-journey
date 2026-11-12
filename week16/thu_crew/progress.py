import runpy, time
from crew3 import crew

last = [time.perf_counter()]

def on_task_done(output):
    try:
        now = time.perf_counter()
        print(f"  DONE:     {output.agent}  +{now - last[0]:.1f}s", flush=True)
        last[0] = now
    except Exception:
        pass

def on_step(step):
    try:
        print(f"  STEP:     {type(step).__name__}", flush=True)
    except Exception:
        pass

crew.task_callback = on_task_done
crew.step_callback = on_step
runpy.run_path("ask3.py", run_name="__main__")
