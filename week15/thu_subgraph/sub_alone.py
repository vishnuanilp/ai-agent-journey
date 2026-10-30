from shop_sub import research
for msg in ["do you have rice?", "rice and milk please", "any phone?"]:
    out = research.invoke({"msg": msg})
    print(msg, "|", out)