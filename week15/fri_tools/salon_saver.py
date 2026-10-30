import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect(Path(__file__).parent / "salon.db", check_same_thread=False)
saver = SqliteSaver(conn)