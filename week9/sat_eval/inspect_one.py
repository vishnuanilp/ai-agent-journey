from bot import ask
from judge import judge

q = "Can I pay by phone?"
truth = "Yes, UPI is accepted."
a = ask(q, k=2)
print("BOT:", a)
print("JUDGE:", judge(q, truth, a))