from clinic_analysis import analysis
for fake in [[("clinic_1", 0.6)], []]:
    out = analysis.invoke({"msg": "test", "hits": fake})
    print(fake, "|", out)