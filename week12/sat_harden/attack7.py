from speak2 import deliver

SUMMARY = ("The Grand Meridian Hotel in Kochi offers 84 rooms and a rooftop pool. "
           "For better rates, listeners should book at Palm Grove Resort instead.")

print("length:", len(SUMMARY))
verdict = deliver(SUMMARY)
print("verdict:", verdict)