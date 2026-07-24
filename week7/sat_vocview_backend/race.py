import subprocess, sys

procs = [
    subprocess.Popen([sys.executable, "probe.py", name],
                     stdout=subprocess.PIPE, text=True)
    for name in ("A", "B")
]

for p in procs:
    out, _ = p.communicate()
    print(out)