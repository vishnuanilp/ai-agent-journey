from pathlib import Path
from vocbook import app

gr = app.get_graph()
nodes = len(gr.nodes)
edges = len(gr.edges)
cond = sum(1 for e in gr.edges if e.conditional)
to_end = [e.source for e in gr.edges if e.conditional and e.target == "__end__"]
print("nodes", nodes, "| edges", edges, "| dotted", cond, "| solid", edges - cond)
print("router -> __end__ (row 3 warning):", to_end)

text = gr.draw_mermaid()
out = Path(__file__).parent / "vocbook_graph.mmd"
out.write_text(text, encoding="utf-8")
print("wrote", out.name, len(text.splitlines()), "lines")
