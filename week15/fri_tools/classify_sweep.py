from classify import classify
def with_context(prev, now):
    return classify(f"(Guest's previous message: {prev})\n{now}")
CASES = [("can I bring my dog?", "what about cats?", "question"),
         ("can I bring my dog?", "thanks!", "chitchat"),
         ("can I bring my dog?", "and the pool hours?", "question"),
         ("do you sell mobile phones?", "ok, book me a room for Saturday", "action"),
         ("book me a room for Saturday", "Sunday instead", "action")]
for prev, now, want in CASES:
    raw, ctx = classify(now), with_context(prev, now)
    print(f"{now!r:36} want {want:9} raw={raw:9} context={ctx:9} {'OK' if ctx == want else 'WRONG'}")